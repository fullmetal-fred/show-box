# Product firmware

**Status: skeleton.** Builds per-SKU targets; does nothing useful yet. Real
firmware starts after phase 1 ([bench plan](../docs/phase1-bench-plan.md)).

- Behavior contract: [docs/protocol.md](../docs/protocol.md)
- Structure, boot sequence, timing: [docs/architecture.md](../docs/architecture.md#firmware-architecture)
- Why not ESPHome: [ADR-0004](../docs/decisions/0004-native-firmware-over-esphome.md)

## Build

```sh
pip install platformio
pio run -e gp          # or relay8, input, ringer
pio run -e gp -t upload
```

| Env | SKU header |
|---|---|
| `gp` | `skus/gp.h` |
| `relay8` | `skus/relay8.h` |
| `input` | `skus/input.h` |
| `ringer` | `skus/ringer.h` |

## Pinning

Platform, core, and libraries are pinned to exact versions in `platformio.ini`.
Never use `stable`, `latest`, or `^` ranges.

## Recovery / reflash

USB + `esptool` (documented in full with phase 2). **On non-isolated boards
(ESP32-POE, ESP32-POE2) never connect USB to a computer while the board is
powered from PoE**: per Olimex, this can damage the board, the computer, or
both. The ESP32-POE-ISO is safe.

License: MPL-2.0 (proposed, [ADR-0008](../docs/decisions/0008-licensing.md)).
