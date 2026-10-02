# General Purpose box: wiring notes (draft)

2–4 dry-contact relays, 2 contact-closure inputs, 2 low-voltage digital outputs.

```
PoE ──▶ ESP32-POE-ISO ──UEXT I2C──▶ MCP23017 ──▶ 4-ch relay module ──▶ pluggable terminals (C/NO/NC ×4)
                                       │──────▶ inputs ×2 (pull-up, to terminals, contact to GND)
                                       └──────▶ outputs ×2 (3.3 V logic via series R, to terminals)
```

| Expander pin | Function | Terminal |
|---|---|---|
| GPA0–GPA3 | Relay 1–4 (active-low) | RLY1–4 C/NO/NC |
| GPB0–GPB1 | Input 1–2 (internal pull-up, closed = low) | IN1–2 + GND |
| GPB2–GPB3 | Output 1–2 | OUT1–2 + GND |

Open: are 3.3 V logic outputs useful, or should "outputs" be open-collector
(sink up to e.g. 100 mA at 24 V) so they can drive LEDs, buzzers, maglock
relays? Open-collector is more useful to props people. **[open]**

Power: 4 relays energized at once is about the ISO board's entire user budget
([architecture](../../docs/architecture.md#the-power-budget-problem)). Measure
on the bench; fall back to 2 relays or a different board.

Proposed rating to advertise: low-voltage loads only, ≤ 30 VDC / 24 VAC, ≤ 2 A
([safety.md](../../docs/safety.md#relay-boxes)).

## Per-unit test checklist (draft)

- [ ] Boot with PoE: all relays off, no click during boot (listen + LED).
- [ ] Each relay: `/relay/n/on`, `/off`, `/pulse 100`; continuity on C–NO.
- [ ] Each input: short to GND, `/in/n/status` reports closed, outbound message received.
- [ ] Each output: measured level on/off.
- [ ] `/all/off` clears everything.
- [ ] Label: hostname/MAC, serial, ratings.
