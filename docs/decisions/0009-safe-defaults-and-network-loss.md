# 0009. Everything off at boot; configurable network-loss behavior

- Status: Accepted (relay network-loss default: Proposed)
- Date: 2026-10-02

## Context

A box can reboot mid-show (power blip, PoE switch restart, watchdog). It can
also lose the network while running. What it does in those moments determines
whether a glitch becomes a safety incident (a motor runs, a phone rings forever)
or a non-event.

## Decision

1. **Boot:** all relays, outputs, and the ringer are off. Output states are
   never restored after reset; settings are. Firmware drives every output GPIO
   to its inactive level as the first thing it does, and hardware pin selection
   avoids ESP32 pins that glitch high during reset or boot (verified on bench
   with a scope or logic analyzer).
2. **Network loss** (link down, or optional heartbeat timeout) is handled per
   channel via `on_network_loss`:
   - Ringer: `stop` (default) or `continue`.
   - Relays/outputs: `hold` (proposed default) or `off`.
3. **Pending pulses always complete** (turn off on schedule) regardless of
   network state.
4. A hardware or task **watchdog** resets a hung box; per rule 1, a reset is
   always safe.

Details: [protocol.md](../protocol.md#network-loss-and-boot-behavior).

## Consequences

- A reboot is visible (things turn off) rather than silent. Operators may need
  to re-fire latching cues after a box reboots; docs must say this.
- `hold` as the relay default means a latched relay stays on through a
  network outage. That's right for e.g. a practical light, wrong for e.g. a
  motor without limit switches. Users must configure `off` for loads that are
  unsafe to leave on. Open question for owner whether to default `off` instead.
