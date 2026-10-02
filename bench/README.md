# Bench tooling (phase 1 only)

**Not product firmware.** Everything here exists to answer hardware questions
quickly ([ADR-0004](../docs/decisions/0004-native-firmware-over-esphome.md)).
It is never shipped and will drift from the product protocol.

| Dir | What |
|---|---|
| [esphome/](esphome/) | ESPHome configs for Olimex ESP32-POE-ISO: relays, ringer (Ag1171 and Black Magic) |
| [osc-proxy/](osc-proxy/) | Runs on the show Mac: receives protocol.md OSC from QLab, calls ESPHome's REST API |
| `results/` | Bench results logs (create per test session) |

License: **MIT-0** (see [LICENSE](LICENSE)). Copy freely into your own projects.

Follow [docs/phase1-bench-plan.md](../docs/phase1-bench-plan.md).
