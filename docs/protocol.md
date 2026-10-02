# Control protocol

**This document is the single source of truth for every OSC address and HTTP
endpoint.** Firmware, web UI, example show files, and user docs follow it. If
they disagree with this file, they are wrong. Changes here go through review
and bump `api_version` when they break compatibility.

`api_version`: **0.1 (draft)**. Nothing is frozen until 1.0.

## Contents

- [Transport](#transport)
- [Conventions](#conventions)
- [Command reference](#command-reference)
  - [System](#system) · [Relays](#relays) · [Digital outputs](#digital-outputs) · [Inputs](#inputs) · [Ringer](#ringer) · [Configuration](#configuration)
- [Status document](#status-document)
- [HTTP specifics](#http-specifics)
- [Outbound messages (inputs)](#outbound-messages-inputs)
- [Timing and state semantics](#timing-and-state-semantics)
- [Network loss and boot behavior](#network-loss-and-boot-behavior)
- [QLab quick reference](#qlab-quick-reference)
- [Reserved / future](#reserved--future)

## Transport

| | OSC | HTTP |
|---|---|---|
| Role | Primary (what QLab sends) | Secondary (scripts, web UI, curl, other tools) |
| Transport | UDP | TCP |
| Default port | **8000** (configurable) | **80** (fixed) |
| Bundles | Accepted; messages applied in order, timetags ignored (executed immediately) | n/a |
| Replies | To the packet's source IP and source port, at `/reply` + the request address (QLab's convention) | HTTP response body |

Both are always enabled. There is no MIDI or RTP-MIDI
([ADR-0002](decisions/0002-osc-and-http-not-midi.md)).

**Addressing.** Static IP or DHCP (default DHCP). The box advertises itself
over mDNS as `showbox-XXXX.local`, where `XXXX` is the last four hex digits of
its Ethernet MAC (also printed on the label). The hostname is configurable. mDNS
service records: `_osc._udp` (port 8000) and `_http._tcp` (port 80).

> Recommendation for shows: use static IPs. mDNS is convenient for setup but
> QLab network patches resolve hostnames, and name resolution is one more thing
> that can fail on a show network.

**Security.** None in v0.x: anyone on the network segment can command the box.
Put show-control gear on its own network. See [Reserved / future](#reserved--future).

## Conventions

- **Channels are numbered from 1**, matching the labels on the box.
  `/relay/1` is the relay labeled "1".
- **All addresses are lowercase.** Matching is case-sensitive; `/Relay/1/On` is
  an unknown address.
- **One action per address.** The verb is the last path element
  (`on`, `off`, `toggle`, `pulse`, ...).
- **Latching vs momentary is chosen per command, not per channel**
  ([ADR-0005](decisions/0005-per-command-latch-or-pulse.md)). `on` latches,
  `pulse` is momentary. Any relay can do either at any time.
- **Arguments are optional unless marked required.** Numeric arguments are
  accepted as OSC int32, float32 (truncated toward zero), or a string containing
  a decimal number, because different senders type the same text differently.
  Durations are integer milliseconds.
- **Extra arguments on verbs that take none are ignored.** This lets
  controllers that send `1.0` on press / `0.0` on release (TouchOSC, etc.) use
  `on`/`off`/`pulse` buttons. Use [`set`](#relays) for value-driven controls.
- **Invalid commands do nothing.** An unknown address, an out-of-range channel,
  or an out-of-range argument changes no state. The error is logged, counted in
  `/status` (`last_error`), and returned as HTTP 4xx. OSC has no per-message
  error reply (fire-and-forget senders like QLab would ignore it anyway).
  We **reject rather than clamp** so a typo in a cue fails visibly in tech
  instead of doing something different from what was written.
- Channel `all` is accepted wherever a channel number is, meaning every channel
  of that type on this box.

## Command reference

Notation: `<n>` = channel number (1-based) or `all`. `[ms]` = optional
duration argument. Ranges are inclusive.

### System

| OSC address | Args | HTTP | Effect |
|---|---|---|---|
| `/status` | — | `GET /status` | Reply with the [status document](#status-document). OSC reply goes to the sender as `/reply/status` with one string argument containing the JSON. |
| `/all/off` | — | `POST /all/off` | **Panic.** Every relay off, every output off, ringer stopped, pending pulses cancelled. Idempotent. |
| `/identify` | `[seconds]` 1–60, default 10 | `POST /identify` | Blink the status LED (if fitted) and highlight the box in the web UI. **Never actuates a relay, output, or the ringer.** |
| `/ping` | — | `POST /ping` | Reply `/reply/ping` (OSC) / `{"ok":true}` (HTTP). Also resets the [heartbeat timer](#network-loss-and-boot-behavior) if enabled. |

### Relays

Present on General Purpose (2–4) and Relay (8) SKUs. On the Ringer, the
internal ring-generator gate relay is **not** exposed here; use `/ring/*`.

| OSC address | Args | HTTP | Effect |
|---|---|---|---|
| `/relay/<n>/on` | — | `POST /relay/<n>/on` | Close the contact and leave it closed (latch). Cancels a pending pulse. |
| `/relay/<n>/off` | — | `POST /relay/<n>/off` | Open the contact. Cancels a pending pulse. |
| `/relay/<n>/toggle` | — | `POST /relay/<n>/toggle` | Invert the current state. Cancels a pending pulse. If a pulse was active, the relay was on, so it turns off. |
| `/relay/<n>/pulse` | `[ms]` 20–600000 | `POST /relay/<n>/pulse?ms=` | Close now, open after `ms` (or this channel's default pulse length). |
| `/relay/<n>/set` | `state` **required**, 0 or 1 | `POST /relay/<n>/set?state=` | Set state from a value. For faders/toggles that send 0/1. Nonzero = on. |

### Digital outputs

Low-voltage logic outputs (General Purpose SKU). Same verbs and semantics as
relays.

| OSC address | Args | HTTP |
|---|---|---|
| `/out/<n>/on` · `/off` · `/toggle` · `/set` · `/pulse [ms]` | as relays | `POST /out/<n>/...` |

### Inputs

Contact-closure inputs (General Purpose, Input SKUs). States are named for what
the switch is doing: **`closed`** (contact made, input active) or **`open`**.

| OSC address | Args | HTTP | Effect |
|---|---|---|---|
| `/in/<n>/status` | — | `GET /in/<n>/status` | Reply `/reply/in/<n>/status` with one int: 1 = closed, 0 = open. |
| `/in/<n>/test` | `state` **required**: `closed` or `open` | `POST /in/<n>/test?state=` | Fire this input's outbound messages as if it changed, without touching the hardware. For programming cues without walking to the prop. |

Inputs send messages *out* when they change; see [Outbound messages](#outbound-messages-inputs).

### Ringer

Ringer SKU only. Every ring command accepts an optional cadence name; without
it, the box's current default cadence is used. Cadence names are listed in
[ringer.md](ringer.md#cadence-presets).

| OSC address | Args | HTTP | Effect |
|---|---|---|---|
| `/ring/start` | `[cadence]` | `POST /ring/start?cadence=` | Ring continuously until `/ring/stop`, `/all/off`, or the safety time limit. |
| `/ring/once` | `[cadence]` | `POST /ring/once?cadence=` | Ring one full cadence cycle, then stop. |
| `/ring/count` | `n` **required** 1–100, `[cadence]` | `POST /ring/count?n=&cadence=` | Ring `n` full cadence cycles, then stop. |
| `/ring/stop` | — | `POST /ring/stop` | Stop immediately (ring voltage removed within one control tick, see [timing](#timing-and-state-semantics)). |
| `/ring/cadence` | `name` **required** | `POST /ring/cadence?name=` | Set the **default** cadence (persisted). Does not start ringing. If ringing, the current ring continues with its original cadence. |

The built-in cadence **`steady`** is "on with no off-phase." It exists so a
hold-to-ring button and `/ring/start steady` + `/ring/stop` give manual timing
control, exactly like the push-button ringers this replaces.

> For determinism in a show file, name the cadence in each cue
> (`/ring/start us`) rather than relying on the persisted default.

**Lid button (Ringer).** The physical button calls the same internal functions
as the network commands. Its behavior is a setting (`ring.button_mode`):

| Mode | Press | Release |
|---|---|---|
| `hold` (default, proposed) | same as `/ring/start steady` | same as `/ring/stop` |
| `once` | same as `/ring/once` | — |
| `toggle` | `/ring/start` if idle, `/ring/stop` if ringing | — |

### Configuration

Settings are normally changed in the web UI. These addresses exist so a show
file can set up a box from scratch. Every value written here is **persisted**
(see [timing](#timing-and-state-semantics) for when flash is written).

| OSC address | Args | HTTP | Effect |
|---|---|---|---|
| `/config/relay/<n>/pulse_ms` | `ms` 20–600000 | `POST /config/relay/<n>/pulse_ms?ms=` | Default pulse length for this relay. Factory default 500. |
| `/config/out/<n>/pulse_ms` | `ms` 20–600000 | `POST /config/out/<n>/pulse_ms?ms=` | Same, for outputs. |
| `/config/save` | — | `POST /config/save` | Force pending settings to flash now. |

The full settings document is `GET /config` / `PUT /config` (JSON), used by the
web UI. Its schema will be documented in `firmware/` alongside the code;
network, outbound targets, and anything that could make the box unreachable are
HTTP-only by design.

## Status document

`GET /status` and the `/reply/status` string both return this JSON. Fields for
hardware the SKU doesn't have are omitted.

```json
{
  "api_version": "0.1",
  "product": "showbox",
  "sku": "ringer",
  "firmware": "0.1.0+abc1234",
  "hostname": "showbox-1a2b",
  "mac": "AA:BB:CC:DD:1A:2B",
  "ip": "192.168.1.50",
  "uptime_ms": 123456,
  "relays":  [ {"n": 1, "on": false, "pulse_remaining_ms": 0} ],
  "outputs": [ {"n": 1, "on": false, "pulse_remaining_ms": 0} ],
  "inputs":  [ {"n": 1, "closed": true} ],
  "ring": {
    "active": true,
    "cadence": "us",
    "default_cadence": "us",
    "mode": "continuous",
    "cycles_remaining": null,
    "phase": "on",
    "elapsed_ms": 4210
  },
  "last_error": {"uptime_ms": 120001, "message": "relay 5: no such channel"}
}
```

`ring.mode` is one of `idle`, `once`, `count`, `continuous`.

## HTTP specifics

- Commands are **`POST` only** (browsers and link-preview bots issue `GET`s
  speculatively; a `GET` must never click a relay). Read-only endpoints are `GET`.
- Arguments come from the **query string** or a **JSON body** with the same
  names (`{"ms": 250}`). If both are present, the body wins.
- Responses are JSON. Success: `200 {"ok": true, "status": {...}}` (the full
  status document, so a script can confirm the result in one round trip).
- Errors: `400` bad argument, `404` unknown path or channel, `409` command not
  valid on this SKU (e.g. `/ring/start` on a relay box). Body:
  `{"ok": false, "error": "human readable message"}`.
- The web UI is served from `/` and `/ui/*`. Those paths are not part of the API.
- CORS: `Access-Control-Allow-Origin: *` on API responses, so a browser-based
  show tool can call the box. (Revisit if/when auth is added.)

Example:

```sh
curl -X POST "http://showbox-1a2b.local/relay/1/pulse?ms=250"
curl -X POST http://192.168.1.50/ring/count -H 'Content-Type: application/json' -d '{"n":3,"cadence":"uk"}'
```

## Outbound messages (inputs)

Each input can send up to **two targets** on each edge (`closed` and/or `open`).
A target is one of:

- **OSC**: host, port, address, arguments (e.g. QLab at `192.168.1.10:53000`,
  `/cue/12/start`).
- **HTTP**: method (GET/POST), URL, optional body.

Templates available in the address, arguments, URL, and body:

| Token | Value |
|---|---|
| `{n}` | input number |
| `{state}` | `closed` or `open` |
| `{value}` | `1` (closed) or `0` (open) |
| `{host}` | this box's hostname |

Factory default per input: no targets configured (nothing is sent). The web UI
offers a "QLab: start cue" preset that fills in `/cue/{cue_number}/start` and
port 53000.

**Debounce:** default 20 ms per input, configurable 0–1000 ms. An edge is only
reported after the input has been stable for the debounce time. Reed switches
with magnets near the threshold may need more.

**Delivery:** OSC is UDP: one packet, no retry, no acknowledgement. HTTP is
attempted once with a 1 s timeout. Outbound sends never block input sampling or
command handling; if a send is still in flight when the next edge arrives, the
next edge is queued (queue depth 8 per box; overflow drops the oldest and sets
`last_error`).

## Timing and state semantics

These rules make behavior predictable when commands overlap.

**Relays and outputs**

- `pulse` turns the channel on now and schedules an off after `ms`, regardless
  of prior state. A relay that was latched on and is then pulsed turns off when
  the pulse ends.
- A `pulse` during a pulse **restarts** the timer from now with the new length.
- `on`, `off`, `toggle`, `set`, and `/all/off` cancel any pending pulse-off.
- Pulse timing resolution target: ±2 ms of the requested length, measured at
  the GPIO. (Relay mechanical operate/release time adds ~5–15 ms and is not
  compensated. Verify on the bench.)

**Ringer**

- Any new `start`, `once`, or `count` **replaces** the current ring program and
  restarts the cadence at the beginning of its first on-phase.
  **Exception:** `/ring/start` with the same cadence while already ringing
  continuously is a no-op, so a double-fired GO doesn't stutter.
- `/ring/stop` removes ring voltage immediately (within one control tick,
  target ≤ 10 ms from packet arrival to gate open; verify on bench).
- **Safety time limit:** continuous ringing stops automatically after
  `ring.max_seconds` (default 120, range 5–600). This protects the generator and
  the bell. `count` and `once` are also bounded by it.
- A cycle is one full pass through the cadence's on/off pattern, including the
  trailing off-phase. `once` therefore ends with silence of the final
  off-phase length before `ring.active` goes false (the bell itself is silent
  as soon as the on-phase ends).

**Persistence**

- Writing flash on the ESP32 briefly stalls code running from flash. To keep
  show-time timing deterministic, persisted settings are written **2 s after the
  last change**, and only if the value actually changed. `/config/save` forces
  an immediate write.
- Timing-critical paths (pulse-off, ring gate) run from timers that are
  unaffected by flash writes (see [architecture.md](architecture.md)). Verify on
  bench by writing config while pulsing.

## Network loss and boot behavior

**Boot:** every relay off, every output off, ringer off. Always. No state is
restored from before power loss. (Settings are restored; output *states* are not.)

**Network loss** is defined as either:

1. Ethernet **link down** (cable unplugged, switch dead, PoE source lost while
   on DC fallback), or
2. optional **heartbeat timeout**: if `heartbeat_s` is nonzero, no OSC/HTTP
   command or `/ping` received for that many seconds. Disabled by default
   (QLab doesn't send heartbeats without extra cues).

On network loss, each channel follows its own `on_network_loss` setting:

| Channel type | Options | Default |
|---|---|---|
| Relay / output | `hold` (keep current state) or `off` | `hold` (proposed, see open questions) |
| Ringer | `stop` or `continue` | **`stop`** |

Pending pulses always complete normally regardless of network state.

## QLab quick reference

QLab 5 Network cue, destination patched to the box's IP and port 8000, type
"OSC message":

| Want | QLab message |
|---|---|
| Momentary contact closure (default length) | `/relay/1/pulse` |
| 250 ms closure | `/relay/1/pulse 250` |
| Latch a relay on / off | `/relay/1/on` · `/relay/1/off` |
| Ring like a US phone until stopped | `/ring/start us` |
| Ring twice, UK style | `/ring/count 2 uk` |
| Stop ringing (actor answers) | `/ring/stop` |
| Panic | `/all/off` |

Inputs firing QLab: set the input's OSC target to the QLab machine, port
53000, address `/cue/<number>/start` (or `/go`). If the QLab workspace has an
OSC passcode, see the open question in the phase 1 plan.

## Reserved / future

Not implemented; addresses reserved so they don't get used for something else.

- `/feedback/*`: push state changes to a subscribed client (TouchOSC, Companion).
- `/auth/*`: optional passcode, in the style of QLab's OSC passcode.
- `/ring/hook/*`: off-hook detection on the Ringer (auto-stop on pickup, outbound "answered" message). See [ringer.md](ringer.md#opportunity-off-hook-detection).
- `/config/ring/freq_hz`: ring frequency, if the chosen ring module allows software frequency.
- `/audio/*`: the someday audio box.
- `/sys/reboot`, `/sys/update`: HTTP-only maintenance, documented with the OTA work.
