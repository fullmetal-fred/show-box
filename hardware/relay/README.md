# Relay box: wiring notes (draft)

8 dry-contact relays for motorized screens, curtains, effects.

- Controller: ESP32-POE2 (12 V rail) or ESP32-POE-ISO + external supply **[open]**.
  8 coils ≈ 3 W, more than the ISO board's ~1.5 W budget.
- MCP23017 GPA0–GPA7 → 8-ch relay module (12 V coils preferred on POE2).
- Pluggable terminals per channel: C / NO / NC.

**Motor loads:** screens and curtain motors are usually driven through their
own controller's dry-contact inputs (pulse up / pulse down / stop). Advise users
to use those, not to switch motor power directly. Interlocking (never close up
and down together) is the motor controller's job; we could add an optional
firmware interlock pair setting later. **[open]**

Per-unit test: as General Purpose, for 8 relays, plus a run with all 8 on for
10 minutes, measuring supply temperature and voltage sag.
