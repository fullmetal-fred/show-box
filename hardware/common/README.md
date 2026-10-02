# Common platform

## Controller

| Use | Board | Why |
|---|---|---|
| Input, General Purpose (≤ 2 relays energized at once) | Olimex ESP32-POE-ISO (WROOM-32E, **not** WROVER) | Isolated PoE; ~1.5 W spare is enough |
| Relay (8), Ringer, GP with 4 relays | **[open]** Olimex ESP32-POE2 (25 W, 12 V rail, not isolated) vs ISO + external supply | Power budget, see [architecture](../../docs/architecture.md#the-power-budget-problem) |

### ESP32-POE-ISO notes (from Olimex user manual rev 2.7)

- PoE: IEEE 802.3af Class 0. Needs ≥ ~37 V. **24 V passive PoE won't work.**
- 3000 VDC isolation between PoE and the board.
- Power inputs: PoE, micro-USB, Li-Po, 5 V on EXT1 pin 1 (tied to USB 5 V). **No barrel jack.**
- USB while on PoE: safe on ISO. **Not safe on non-ISO ESP32-POE / POE2.**
- Ethernet: LAN8720A addr 0, MDC 23, MDIO 18, PHY power 12, clock GPIO17 out.
- Header GPIO: 2, 4, 5, 13, 14, 15, 16, 36 (shared UEXT/EXT; 2/14/15 shared with SD card).
  Input-only: 34 (button), 35 (battery sense), 36, 39 (ext power sense).

## I/O expander (proposed for all SKUs)

Off-the-shelf MCP23017 breakout on the UEXT I2C pins. UEXT SDA/SCL GPIO
assignment **[verify on schematic]**. The expander powers up with all pins
high-Z, so active-low relay inputs stay off through boot (verify with the
boot-glitch test).

## Proposed direct-GPIO allocation

| GPIO | Use | Notes |
|---|---|---|
| UEXT SDA / SCL | I2C to expander | [verify] pins |
| 4 | Ring gate (`RM` on Ag1171, or gate relay) | Boot-safe [verify] |
| 32 or 33 | Ring `F/R` (Ag1171) | Only if broken out [verify]; else use 4/13/16 per final I2C pins |
| 36 | Lid button (Ringer) | Input-only, external pull-up, RC filter |
| 34 | On-board button: factory reset at boot | Fixed by board |

## Relay modules

Active-low Songle-style opto modules: remove the JD-VCC jumper, feed coil
voltage to JD-VCC and 3.3 V to VCC. Prefer 12 V-coil modules on 12 V-rail SKUs.
