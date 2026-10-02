# OSC → ESPHome proxy (bench only)

ESPHome has no OSC receiver. During phase 1 this script runs on the show Mac,
accepts the [protocol.md](../../docs/protocol.md) addresses from QLab, and calls
the ESPHome web server's REST API on the bench box.

```sh
python3 osc_proxy.py --box 192.168.1.50            # listens on udp/8000
```

QLab: create a network patch to `127.0.0.1` port `8000`, then Network cues
with OSC messages.

| OSC in | ESPHome call |
|---|---|
| `/relay/<n>/on` · `off` · `toggle` | `POST /switch/relay_<n>/turn_on` · `turn_off` · `toggle` |
| `/relay/<n>/set <0/1>` | `turn_on` / `turn_off` |
| `/relay/<n>/pulse [ms]` | `turn_on`, then `turn_off` after `ms` (timer in the proxy) |
| `/relay/all/<verb>` | each relay |
| `/ring/start [us\|uk\|short\|us-double\|steady]` | `POST /button/ring_start_<cad>/press` |
| `/ring/once [us\|uk]` | `POST /button/ring_once_<cad>/press` |
| `/ring/stop` | `POST /button/ring_stop/press` |
| `/all/off` | all relays off + ring stop |

Not supported: `/ring/count`, `/status`, config, inputs. Pulse timing runs on
the Mac, so it includes network jitter. It's fine for proving hardware but not
representative of product timing.

Python 3.8+, standard library only. License MIT-0.
