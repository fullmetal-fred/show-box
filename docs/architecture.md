# Architecture

Status: draft for phase 1. Items marked **[verify]** need bench confirmation;
**[open]** items are listed in [open questions](#open-questions).

## System view

```
  Show computer (QLab)                         Each box is independent (ADR-0001)
  ┌──────────────────┐   OSC/UDP :8000   ┌──────────────────────────────────┐
  │ Network cues     │ ────────────────▶ │ showbox (ESP32 + Ethernet + PoE) │
  │ OSC in :53000    │ ◀──────────────── │  relays / outputs / ringer       │
  └──────────────────┘  OSC from inputs  │  inputs → outbound OSC/HTTP      │
          │                              └──────────────────────────────────┘
          │  PoE switch (dedicated show network recommended)
```

No hub, no cloud, no box-to-box traffic. Boxes are clients only when an input
fires an outbound message.

## Hardware platform

### Controller board

Baseline: **Olimex ESP32-POE-ISO** (ESP32-WROOM-32E, LAN8720A PHY, 802.3af
PoE, 3000 VDC isolation between the PoE/Ethernet side and the board).
Source: Olimex ESP32-POE user manual rev 2.7
(<https://raw.githubusercontent.com/OLIMEX/ESP32-POE/master/DOCUMENTS/ESP32-POE-user-manual.pdf>).

Ethernet pin map (from the manual, high confidence):

| Signal | GPIO |
|---|---|
| PHY | LAN8720A, address 0 |
| MDC / MDIO | GPIO23 / GPIO18 |
| PHY power / reset | GPIO12 (hold PHY in reset until clock runs) |
| RMII clock | GPIO17 output (WROOM variants). GPIO0 on WROVER variants, so don't buy WROVER. |

Arduino-ESP32 3.x: `ETH.begin(ETH_PHY_LAN8720, 0, 23, 18, 12, ETH_CLOCK_GPIO17_OUT);`

#### The power budget problem

The ESP32-POE-ISO's isolated converter is 2 W total. Olimex's FAQ gives about
**1.5 W for user circuits** (~300 mA at 5 V). Implications (high confidence on
the number; relay coil current ~70–90 mA each is typical for SRD-05VDC parts,
**[verify]**):

| SKU | Load | Fits in ISO budget? |
|---|---|---|
| General Purpose (4 relays) | 4 × ~0.4 W with all on | **Borderline / no.** 2 relays OK. |
| Relay (8 relays) | ~3 W | **No** |
| Input | Pull-ups, LEDs | Yes |
| Ringer | Ring generator, several W while ringing | **No** |

So "PoE-only" for the Relay and Ringer SKUs needs more power than the ISO board
supplies. Candidate architectures **[open], decided on the bench**:

| Option | How | Pros | Cons |
|---|---|---|---|
| **A. Olimex ESP32-POE2** | 802.3at, up to 25 W, jumper-selectable 12 V/1.5 A or 24 V/0.75 A rail, plus 5 V/1.5 A | One board, 12 V rail drives relay coils and ring generator directly | **Not isolated** (PoE side to board ground); WROVER-E module, so the RMII clock is on GPIO0 **[verify]**; needs an 802.3at switch or injector for >13 W; no USB while on PoE |
| B. ESP32-POE-ISO + external DC supply for loads | Wall-wart / DIN PSU for coils and ringer | Keeps ISO board; isolation easy to reason about | Two power cords, so the box is no longer "PoE powered" |
| C. Isolated 802.3at PoE splitter (12 V out) + non-PoE ESP32 Ethernet board | Splitter feeds everything | Off-the-shelf isolated PoE; plenty of power | Extra module, more wiring; splitter quality varies |
| D. **Waveshare ESP32-S3-POE-ETH-8DI-8RO** (Relay SKU) | All-in-one: 802.3af PoE, 8 relays, 8 opto inputs, DIN case, ~$50 | Nearly the whole Relay SKU off the shelf; DIN look for free | Different MCU (ESP32-S3) and Ethernet chip (W5500 over SPI), so a second board port; 8 coils on 802.3af and PoE isolation **[verify]**; no board-level FCC found; less of our own value-add in the hardware |

Current lean: **ISO for Input and 2-relay General Purpose; A for the Ringer;
A or D for Relay (bench both)**, with an isolated DC/DC module on the ringer's high-voltage side
regardless (see [safety.md](safety.md)). Medium confidence. The firmware
doesn't care: board choice is a per-SKU pin map.

**DC barrel fallback:** the ESP32-POE-ISO has **no barrel jack** (power is PoE,
micro-USB, Li-Po, or 5 V on EXT1 pin 1, which is tied to USB 5 V). POE2
barrel input **[verify]**. A fallback input will need an ORing arrangement
(ideal-diode module or Schottky) so PoE and DC can't fight. **[open]**

#### GPIO

From the manual: GPIO2, 4, 5, 13, 14, 15, 16, 36 are broken out on the UEXT/EXT
headers (each pin is shared between the two, so use it on only one). GPIO2/14/15
also go to the SD card slot. Input-only: GPIO34 (on-board button), 35 (battery
sense), 36, 39 (external power sense).

Rules for output pins (relays, ring gate):

- Avoid strapping pins (GPIO0, 2, 5, 12, 15) and pins that toggle during boot
  (GPIO14 and 15 commonly output a PWM/log signal at reset **[verify]**).
- Preferred direct outputs: **GPIO4, 13, 16**, and 32/33 if broken out
  **[verify on schematic]**.
- Not enough boot-safe GPIO even for the General Purpose box (4 relays + 2
  inputs + 2 outputs), let alone 8 relays or 12 inputs. **Proposal: every SKU
  uses an off-the-shelf I2C GPIO expander module** (e.g. MCP23017, 16 I/O) on
  the UEXT I2C pins, so all SKUs share one I/O driver. Direct GPIO is kept for
  timing-sensitive or safety signals: ring gate / `F/R`, lid button, status LED.
  An expander An expander powers up with all
  pins as inputs (high-Z), so active-low relay modules with pull-ups stay
  **off** through ESP32 boot, which is better than direct GPIO.
- Inputs: GPIO36/39 need external pull-ups (no internal pull on input-only pins).

Proposed per-SKU pin maps live in `firmware/skus/*.h` and `hardware/<sku>/`.
All are **[verify]** until the boot-glitch test in the
[bench plan](phase1-bench-plan.md) passes.

### Relay modules

Common 5 V Songle-based opto relay modules are **active-low**. Driven from
3.3 V logic with VCC = 5 V, "high" may not fully turn the opto off. Standard
fix: remove the JD-VCC jumper, feed 5 V (or the coil voltage) to JD-VCC, 3.3 V
to VCC, so the opto LED side runs from 3.3 V. Firmware treats relays as
active-low and drives the pin high before switching it to output mode. Prefer
12 V-coil modules on POE2-based SKUs. **[verify]**

### Ringer subsystem

See [ringer.md](ringer.md) and [safety.md](safety.md). Summary:
ESP32 → (isolation barrier) → ring generator module → current limiting + fuse
→ shrouded output connector → prop phone.

## Firmware architecture

Native Arduino-ESP32 on PlatformIO ([ADR-0004](decisions/0004-native-firmware-over-esphome.md)).

### Toolchain and pinning

- **Arduino-ESP32 3.3.x** (3.3.12 latest stable as of 2026-09-18, IDF 5.5.5).
  Not 4.0 (RC as of 2026-09-23); re-evaluate after it stabilizes.
- PlatformIO's official platform does not ship Arduino 3.x. Use the community
  **pioarduino** platform, **pinned to a specific release URL**, not `stable`.
- Libraries pinned to exact versions in `platformio.ini`.
- Candidate libraries (all **[verify]** in phase 2): CNMAT OSC (or hideakitai
  ArduinoOSC / MicroOsc), ESP32Async/ESPAsyncWebServer, ArduinoJson 7, LittleFS.
  The OSC subset we need is small; an in-house parser of ~300 lines is
  acceptable if libraries are awkward.

### Module layout

```
firmware/
  platformio.ini        one env per SKU (gp, relay8, input, ringer)
  include/product.h     product name, hostname prefix, version
  skus/<sku>.h          pin maps + feature flags (relay count, inputs, ringer)
  src/
    main.cpp            boot sequence
    outputs.*           relays + digital outputs: state, pulse timers
    inputs.*            sampling, debounce, edge events
    ringer.*            cadence engine, gate control, safety limit, lid button
    dispatch.*          protocol-agnostic command table (from protocol.md)
    osc_server.*        UDP → dispatch
    http_server.*       REST → dispatch, web UI static files
    outbound.*          input-edge messages (OSC/HTTP) with send queue
    settings.*          JSON settings in LittleFS, debounced writes
    netmgr.*            Ethernet, DHCP/static, mDNS, link-loss events
    ota.*               OTA updates
```

`dispatch` is the core: one table of commands with argument validation,
shared by OSC, HTTP, and the ringer's lid button. That gives one code path
([ADR-0006](decisions/0006-ringer-lid-button.md)).

### Boot sequence (target: commands accepted < 3 s after power with static IP **[verify]**)

1. First instructions: drive every output pin to its inactive level, set as output.
2. Start the hardware watchdog.
3. Mount LittleFS, load settings (fall back to defaults on parse error; never
   block boot on bad settings).
4. Start Ethernet. Static IP if configured, else DHCP.
5. Start OSC and HTTP listeners as soon as the interface has an address.
6. mDNS, OTA, and web UI assets come after the listeners.

### Timing

- Pulse-off and ring cadence edges use `esp_timer` callbacks (IDF high-resolution
  timer), dispatched from a dedicated high-priority task. The callbacks and the
  GPIO writes they make must not depend on flash-resident code during flash
  writes (place them in IRAM, or defer flash writes while a timer is armed).
  **[verify]** with the "write config while pulsing" bench test.
- Network handling runs on a lower-priority task than the timing task.
- Settings writes are debounced 2 s and skipped if unchanged ([protocol.md](protocol.md#timing-and-state-semantics)).

### Settings

A single JSON document in LittleFS (`/settings.json`), versioned with a
`schema` integer and migrated on load. Writes go to a temp file followed by an
atomic rename, so a power cut mid-write keeps the old file.

### Updates and recovery

- **OTA** via the web UI (upload a `.bin`) using the dual app partition scheme.
  A new image must call "mark valid" after it boots and brings up the network,
  or the bootloader rolls back (IDF app rollback).
- **Recovery / reflash:** USB (micro-USB on Olimex boards) with `esptool`.
  Documented in `firmware/README.md`, not advertised. On the ISO board, USB is
  safe while on PoE; on non-isolated boards (POE2) it is **not**. The docs must
  say so prominently.
- **Factory reset:** hold the on-board button (GPIO34) during power-up for 5 s.
  **[open]** Should this be reachable on the enclosure?

## Future audio box

Not designed. Constraints we keep so it stays possible:

- The protocol reserves `/audio/*`.
- The firmware license choice (MPL-2.0 proposed) doesn't block linking a
  vendor SDK ([ADR-0008](decisions/0008-licensing.md)).
- `dispatch` is protocol-agnostic and per-SKU feature flags gate modules, so
  an audio SKU is a new feature module, not a fork. Its board will likely
  differ (I2S DAC, or a Dante module with its own Ethernet port).

## Open questions

Tracked centrally in [phase1-bench-plan.md](phase1-bench-plan.md#open-questions-for-owner).
