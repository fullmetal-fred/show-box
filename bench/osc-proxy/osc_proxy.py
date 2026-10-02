#!/usr/bin/env python3
# SPDX-License-Identifier: MIT-0
"""Phase 1 bench bridge: QLab OSC (docs/protocol.md subset) -> ESPHome REST.

Runs on the show machine. Python 3.8+, standard library only.

    python3 osc_proxy.py --box 192.168.1.50 [--listen 8000] [--relays 3]

Then point a QLab network patch at 127.0.0.1:8000.
Bench tooling only: not product firmware, no guarantees about timing.
"""
import argparse
import socket
import struct
import threading
import urllib.error
import urllib.request

RING_CADENCES = {"us", "uk", "short", "us-double", "steady"}
RING_ONCE_CADENCES = {"us", "uk"}  # what ringer-cadences.yaml exposes as "once" buttons


def _osc_string(data, i):
    end = data.index(b"\0", i)
    s = data[i:end].decode("utf-8", "replace")
    return s, (end + 4) & ~3


def parse_osc(data):
    """Yield (address, args) for a message or bundle."""
    if data.startswith(b"#bundle\0"):
        i = 16  # "#bundle\0" + 8-byte timetag (ignored, run immediately)
        while i + 4 <= len(data):
            (size,) = struct.unpack(">i", data[i:i + 4])
            yield from parse_osc(data[i + 4:i + 4 + size])
            i += 4 + size
        return
    address, i = _osc_string(data, 0)
    args = []
    if i < len(data) and data[i:i + 1] == b",":
        tags, i = _osc_string(data, i)
        for t in tags[1:]:
            if t == "i":
                args.append(struct.unpack(">i", data[i:i + 4])[0]); i += 4
            elif t == "f":
                args.append(struct.unpack(">f", data[i:i + 4])[0]); i += 4
            elif t == "s":
                s, i = _osc_string(data, i); args.append(s)
            elif t in "TF":
                args.append(t == "T")
            else:
                raise ValueError(f"unsupported OSC type tag {t!r}")
    yield address, args


def as_int(v):
    """protocol.md: numeric args may arrive as int, float, or numeric string."""
    if isinstance(v, bool):
        raise ValueError("bool is not a number")
    return int(float(v)) if isinstance(v, str) else int(v)


class Bridge:
    def __init__(self, box, relays, default_pulse_ms):
        self.base = f"http://{box}"
        self.relays = relays
        self.default_pulse_ms = default_pulse_ms
        self.pulse_timers = {}
        self.lock = threading.Lock()

    def post(self, path):
        req = urllib.request.Request(self.base + path, data=b"", method="POST")
        try:
            with urllib.request.urlopen(req, timeout=2) as r:
                print(f"  POST {path} -> {r.status}")
        except urllib.error.HTTPError as e:
            print(f"  POST {path} -> HTTP {e.code}")
        except OSError as e:
            print(f"  POST {path} -> FAILED: {e}")

    def _cancel_pulse(self, n):
        t = self.pulse_timers.pop(n, None)
        if t:
            t.cancel()

    def relay(self, n, verb, args):
        if verb == "pulse":  # validate before touching state: invalid commands do nothing
            ms = as_int(args[0]) if args else self.default_pulse_ms
            if not 20 <= ms <= 600000:
                raise ValueError(f"pulse {ms} ms out of range 20-600000")
        elif verb == "set":
            state = as_int(args[0])
        elif verb not in ("on", "off", "toggle"):
            raise ValueError(f"unknown relay verb {verb!r}")
        with self.lock:
            self._cancel_pulse(n)
            if verb in ("on", "off", "toggle"):
                self.post(f"/switch/relay_{n}/{ {'on': 'turn_on', 'off': 'turn_off', 'toggle': 'toggle'}[verb] }")
            elif verb == "set":
                self.post(f"/switch/relay_{n}/{'turn_on' if state else 'turn_off'}")
            else:  # pulse
                self.post(f"/switch/relay_{n}/turn_on")
                t = threading.Timer(ms / 1000, self.post, (f"/switch/relay_{n}/turn_off",))
                self.pulse_timers[n] = t
                t.start()

    def handle(self, address, args):
        parts = address.strip("/").split("/")
        if parts[0] == "relay" and len(parts) == 3:
            chans = range(1, self.relays + 1) if parts[1] == "all" else [as_int(parts[1])]
            for n in chans:
                if not 1 <= n <= self.relays:
                    raise ValueError(f"relay {n}: no such channel")
                self.relay(n, parts[2], args)
        elif address == "/all/off":
            for n in range(1, self.relays + 1):
                self.relay(n, "off", [])
            self.post("/button/ring_stop/press")
        elif address == "/ring/stop":
            self.post("/button/ring_stop/press")
        elif address in ("/ring/start", "/ring/once"):
            cad = str(args[0]) if args else "us"
            allowed = RING_CADENCES if address == "/ring/start" else RING_ONCE_CADENCES
            if cad not in allowed:
                raise ValueError(f"{address}: cadence {cad!r} not available on bench config")
            verb = address.rsplit("/", 1)[1]
            self.post(f"/button/ring_{verb}_{cad.replace('-', '_')}/press")
        else:
            raise ValueError("not supported by the bench proxy")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--box", required=True, help="ESPHome box IP or hostname")
    ap.add_argument("--listen", type=int, default=8000, help="UDP port to receive OSC on (default 8000)")
    ap.add_argument("--bind", default="0.0.0.0")
    ap.add_argument("--relays", type=int, default=3)
    ap.add_argument("--pulse-ms", type=int, default=500, help="default pulse length")
    a = ap.parse_args()

    bridge = Bridge(a.box, a.relays, a.pulse_ms)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((a.bind, a.listen))
    print(f"OSC on udp/{a.listen} -> ESPHome at {bridge.base}")
    while True:
        data, src = sock.recvfrom(65535)
        try:
            for address, args in parse_osc(data):
                print(f"{src[0]}: {address} {args}")
                try:
                    bridge.handle(address, args)
                except (ValueError, IndexError) as e:
                    print(f"  ignored: {e}")
        except (ValueError, struct.error) as e:
            print(f"{src[0]}: malformed OSC packet: {e}")


if __name__ == "__main__":
    main()
