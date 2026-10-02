# Architecture Decision Records

One file per decision, numbered, never renumbered. To change a decision, write
a new ADR that supersedes the old one and update the old one's status line.

Statuses: **Proposed** (awaiting owner sign-off) · **Accepted** · **Superseded by NNNN** · **Rejected**.

| # | Decision | Status |
|---|---|---|
| [0001](0001-standalone-devices.md) | Standalone devices, no inter-device communication | Accepted |
| [0002](0002-osc-and-http-not-midi.md) | OSC (primary) + HTTP (secondary); no MIDI / RTP-MIDI | Accepted |
| [0003](0003-off-the-shelf-parts.md) | Off-the-shelf modules, no custom PCB in early phases | Accepted |
| [0004](0004-native-firmware-over-esphome.md) | Native Arduino-ESP32 product firmware; ESPHome only for bench proof | Accepted |
| [0005](0005-per-command-latch-or-pulse.md) | Latch vs momentary chosen per command, not per channel | Accepted |
| [0006](0006-ringer-lid-button.md) | Ringer lid button uses the same code path as network commands | Accepted (button mode default Proposed) |
| [0007](0007-open-source.md) | Open hardware and open firmware; sell the assembled unit | Accepted |
| [0008](0008-licensing.md) | License choices: CERN-OHL-S-2.0 / MPL-2.0 / CC BY-SA 4.0 | **Proposed** |
| [0009](0009-safe-defaults-and-network-loss.md) | Everything off at boot; configurable network-loss behavior | Accepted (relay default Proposed) |
| [0010](0010-defer-custom-pcb.md) | Defer custom PCB; DIN-rail modules as the polish path | Accepted (deferred, not rejected) |
| [0011](0011-no-custom-protocol.md) | Plain OSC and HTTP only; no custom protocol or OSC extension | Accepted |

Template: [0000-template.md](0000-template.md).
