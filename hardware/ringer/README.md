# Ringer box: wiring notes (draft)

Read [docs/ringer.md](../../docs/ringer.md) and [docs/safety.md](../../docs/safety.md) first.

## Option 1: Silvertel Ag1171 (primary bench candidate)

```
LOGIC SIDE                           ║  RING SIDE (isolated island)
board 5 V ─▶ isolated DC/DC 5→5 V ══╬══▶ Ag1171 VCC/GND
GPIO4  ─▶ isolator ch1 ═════════════╬══▶ Ag1171 RM   (ring mode)
GPIO32 ─▶ isolator ch2 ═════════════╬══▶ Ag1171 F/R  (toggled at 20/25 Hz)
GPIO?  ◀─ isolator ch3 ◀════════════╬═══ Ag1171 SHK  (hook detect) [optional, verify]
                                    ║    Ag1171 TIP/RING ─▶ fuse/PTC ─▶ [series R?] ─▶ speakON ─▶ prop phone
lid button ─▶ GPIO36 (pull-up, RC)  ║
```

Ag1171 pin names and the exact ringing procedure come from the datasheet
**[verify]**. Its remaining pins (audio, power-denial, etc.) are strapped per
the datasheet's minimal application circuit.

## Option 2: Cambridge Electronics Labs "Black Magic" 12 V (fallback)

```
LOGIC SIDE                            ║  RING SIDE
12 V rail ─▶ isolated DC/DC 12→12 V ══╬══▶ gate relay contact ─▶ Black Magic +12 V
GPIO4 ─▶ driver ─▶ gate relay coil    ║    Black Magic out ─▶ ≥300 Ω series R ─▶ fuse ─▶ speakON
```

The relay switches the module's DC **input**, so the generator is off (no idle
draw, no HV present) whenever not ringing. Cadence = toggling the relay.
Measure start-up delay; if too slow, keep it powered and switch the output
with a relay rated for the voltage instead.

## Layout rules

- Ring side physically separated, with a barrier if spacing is tight. Target
  ≥ 3 mm creepage/clearance as a working figure [verify against IEC 62368-1].
- Warning label at the output connector:
  **"RINGING VOLTAGE: prop telephone only. DO NOT connect to a live telephone line."**

## Per-unit test checklist (draft)

- [ ] Unpowered: ring output pins to Ethernet shield, logic GND, DC input GND: > 10 MΩ.
- [ ] Boot: no ring voltage on output (scope/DMM) during and after boot.
- [ ] `/ring/once us`: one 2 s ring on the reference phone. True-RMS voltage at the phone ≥ 60 Vrms (target, [verify]).
- [ ] `/ring/start uk` / `/ring/stop`: stop latency ≤ 10 ms (scope).
- [ ] Lid button in default mode works with network unplugged.
- [ ] Safety limit: `/ring/start` stops by itself at `ring.max_seconds`.
- [ ] Output short for 120 s: no damage, recovers.
- [ ] Unplug Ethernet while ringing: ringing stops (default policy).
- [ ] Label present.
