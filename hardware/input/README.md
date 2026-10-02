# Input box: wiring notes (draft)

8–12 contact-closure inputs (reed switches, buttons, microswitches) that send
OSC/HTTP to configurable targets ([protocol](../../docs/protocol.md#outbound-messages-inputs)).

- Controller: ESP32-POE-ISO (low power; isolation helps with long field wiring).
- MCP23017 (16 I/O) with internal pull-ups; closed contact pulls to GND.
- Per input: series resistor (~1 kΩ) + small cap to GND at the terminal for
  ESD/noise, plus a TVS or clamp diodes **[TBD]**. Escape rooms run long,
  unshielded cable past maglocks and dimmers.
- Polling the expander at ≥ 500 Hz over I2C, or the MCP23017 INT pin to a GPIO.
  Debounce in firmware (default 20 ms).

Open: opto-isolated inputs (e.g. like Olimex MOD-IO's) vs plain pull-ups. Opto
isolation is more robust in rooms with long cable runs and odd grounding but
costs more and needs a wetting supply. **[open]**

Per-unit test: each input closed/open → correct `/status` and an outbound OSC
packet observed (e.g. in QLab's OSC log or `oscdump`).
