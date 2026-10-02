# Phase 1 bench plan

**Goal:** prove the hardware assumptions cheaply, before writing product firmware.

Two questions must be answered **yes**:

- **(A)** Can QLab click a relay on an Ethernet/PoE ESP32 reliably and quickly,
  over OSC and HTTP?
- **(B)** Can an off-the-shelf ring generator module, gated by the ESP32 behind
  an isolation barrier we add, ring a vintage telephone convincingly?

Phase 1 also settles the questions only a bench can answer: power budget
(ISO vs POE2), boot-time GPIO glitches, ring voltage and frequency per phone,
and gate latency.

Phase 1 uses **ESPHome** for speed ([ADR-0004](decisions/0004-native-firmware-over-esphome.md)).
Nothing built here ships.

## 0. Shopping list

From [bom.csv](../hardware/bom/bom.csv), `bench` and candidate rows:

- [ ] 2× Olimex ESP32-POE-ISO (**WROOM**, not WROVER), 1× Olimex ESP32-POE2
- [ ] 802.3at PoE switch or injector (for POE2 at full power); a plain 802.3af one is fine for ISO
- [ ] 4-ch 5 V relay module (Songle type) + 1-ch 12 V relay module
- [ ] MCP23017 breakout (optional in phase 1; needed for the boot-glitch comparison)
- [ ] Silvertel Ag1171 ×2 (one spare, they're cheap)
- [ ] Cambridge Electronics Labs Black Magic 12 V square (or LR12 sine)
- [ ] Isolated DC/DC: 5→5 V and 12→12 V, ≥ 1.5 kV, sized from datasheets
- [ ] Digital isolator / optos for Ag1171 control lines
- [ ] Power resistors (330 Ω, 1 kΩ, several watts), PTC/fuses, speakON panel + cable parts
- [ ] Vintage phones: at least one WE 500-series (C4A ringer); a second make; a UK phone if obtainable; a harmonic-ringer set if you can find one cheaply
- [ ] True-RMS DMM, logic analyzer, (ideally) a scope; 12 V bench supply; protoboard
- [ ] A Mac with QLab 5 (a free licence is enough for Network cues **[verify]**)

## 1. Network bring-up (ESP32-POE-ISO)

1. Install ESPHome **pinned** (`pip install esphome==<version>`). Avoid 2026.4.1:
   [esphome#15956](https://github.com/esphome/esphome/issues/15956) reports a
   boot loop on POE-ISO Ethernet setup. Record the version used in the
   results log.
2. Flash `bench/esphome/gp-bench.yaml` over USB (ISO board: USB + PoE together is OK).
3. Plug into PoE. Record: time from power-on to first ping reply (stopwatch +
   `ping -i 0.2`), with DHCP and with a static IP.
4. Open `http://<ip>/`: ESPHome web UI shows the relay switches.

## 2. Relay control (question A)

### 2a. HTTP

```sh
curl -X POST http://<ip>/switch/relay_1/turn_on
curl -X POST http://<ip>/switch/relay_1/turn_off
curl -X POST http://<ip>/button/relay_1_pulse/press
```

ESPHome's REST URL format has changed between versions (object id vs entity
name). If these 404, check the ESPHome web API docs for the pinned version.
**[verify]**

### 2b. OSC from QLab via proxy

ESPHome has no OSC receiver, so on the show Mac run:

```sh
python3 bench/osc-proxy/osc_proxy.py --box <ip> --listen 8000
```

It translates the [protocol.md](protocol.md) relay addresses to ESPHome REST
calls (see `bench/osc-proxy/README.md`). In QLab 5:

1. Settings → Network: add a patch "bench" → destination `127.0.0.1`, port `8000`, OSC.
2. Network cues: `/relay/1/on`, `/relay/1/off`, `/relay/1/pulse`, `/relay/1/pulse 250`.
3. GO each and watch the relay.

### 2c. QLab receiving (for input boxes later)

1. In QLab workspace settings → Network/OSC access, check what the
   "No Passcode" row allows. By default View/Edit/Control are unchecked, so
   inbound OSC without a passcode won't run cues. Enable **Control** for the bench.
2. Wire a pushbutton to an ESP32 input. Configure ESPHome to send
   `/cue/1/start` to `<mac-ip>:53000` on press (`bench/esphome/gp-bench.yaml`,
   `udp` component). **[verify]** that ESPHome's `udp` component can emit a raw
   OSC packet. If not, use an HTTP → OSC path via the proxy, or skip until
   product firmware.
3. Press: cue 1 starts.

## 3. Power budget (decides ISO vs POE2)

1. ISO board on 802.3af PoE. Energize 1, 2, 3, 4 relays. At each step measure
   the 5 V rail at the relay module (DMM) and watch for brownout resets
   (serial log / uptime). Record coil current per relay (DMM in series).
2. Same with the Ag1171 ringing a phone continuously (after section 5 works):
   board 5 V current during ring.
3. POE2 on 802.3at: 8 relays on the 12 V rail + Black Magic ringing.
   Record rail sag and board temperature after 10 min.

Pass/fail: no resets, rail ≥ 4.75 V (5 V) / ≥ 11.4 V (12 V) under worst case.

## 4. Boot-glitch test (safety-critical)

Every relay must stay off through power-on, reset, OTA reboot, and brownout.

1. Logic analyzer on every candidate output GPIO (4, 13, 16, 32, 33, and 2, 5,
   14, 15 for comparison) and on the MCP23017 outputs.
2. Power-cycle 10× via PoE; press reset 10×; trigger a software reboot 10×.
3. Record any pulse > 1 µs on any pin. Also listen for relay clicks.

Pass: chosen output pins show no pulse that would drive a relay input. The
result decides the pin maps in `firmware/skus/` and `hardware/`.

## 5. Ringing a vintage phone (question B)

> ⚠ This section works with 60–90 Vrms. Build the ring side on a separate
> protoboard, keep a hand out of the circuit while powered, and use insulated
> clip leads. **Never connect the test rig to a phone line.**

### 5a. Phone characterization (no electronics)

For each test phone: model, ringer type (look for "C4A" or harmonic ringer
markings), DC resistance across ringer leads, and whether it's wired for bell
on the line (some props have had the ringer disconnected).

### 5b. Ag1171 (primary)

1. Build per [hardware/ringer](../hardware/ringer/README.md) option 1:
   isolated DC/DC → Ag1171, isolator on `RM` and `F/R`. Before connecting
   anything to the ESP32, run **isolation check**: DMM between Ag1171 GND and
   ESP32 GND reads open.
2. Flash `bench/esphome/ringer-bench.yaml` (Ag1171 profile).
3. Ring one phone continuously (`steady`). Measure with a true-RMS DMM across
   the phone's line terminals: **Vrms under load**, at 20 Hz and 25 Hz.
4. Subjective: does it sound like a real ring? Full, or weak/buzzy? Record
   audio on a phone at 1 m for comparison.
5. Try every test phone. Then two phones in parallel.
6. Try 16–30 Hz in steps (if F/R allows) on any phone that rings weakly.
7. **Hook detect:** with ringing stopped and with ringing active, lift the
   handset. Does `SHK` change state? (Leads to the auto-stop feature.)

### 5c. Black Magic (fallback / comparison)

1. Build per option 2: 12 V → isolated DC/DC → gate relay → module → 330 Ω →
   phone. Isolation check as above.
2. Same measurements as 5b steps 3–5.
3. **Gate latency:** scope on gate relay coil and on the ring output. Measure
   time from GPIO high to output at full amplitude, and from GPIO low to output
   < 10 V. This decides input-gating vs output-gating.

### 5d. Cadence

1. With the better module, run `us`, `uk`, `short`, `us-double` from QLab
   (via proxy → ESPHome buttons).
2. Logic analyzer on the gate/RM line: measure each on/off segment over 10 cycles.
3. Does each one *sound* right to someone who knows the real thing?

### 5e. Abuse

- Dead-short the output during continuous ring for 120 s. Watch temperatures
  (finger test on DC/DC and resistor after power-off, or IR thermometer).
- Disconnect and reconnect the phone during ring.
- Unplug Ethernet during ring (ESPHome: verify what it does; product firmware
  will stop).

## 6. Results log

Record results in `bench/results/YYYY-MM-DD-<topic>.md`: versions, wiring,
measurements, photos, and pass/fail against the checklist below.

## Test checklist

**A: relay control**

- [ ] A1. ISO board boots on PoE; power-on → ping time recorded (DHCP and static).
- [ ] A2. HTTP: relay on/off/pulse via curl works 50/50 times.
- [ ] A3. QLab → proxy → box: `/relay/1/on`, `/off`, `/pulse`, `/pulse 250` each work 50/50 times.
- [ ] A4. GO → relay click latency measured (QLab GO to contact closure, logic analyzer + QLab timestamp or audio-click method): < 50 ms target via proxy.
- [ ] A5. Pulse length accuracy at 100 ms and 1000 ms measured at the contact.
- [ ] A6. Input → QLab `/cue/1/start` works with Control permission enabled (or documented why not in ESPHome).
- [ ] A7. 4 relays on: no brownout on ISO board (or documented failure → POE2).
- [ ] A8. Boot-glitch: chosen pins clean over 30 resets.
- [ ] A9. Pull Ethernet with a relay latched: behavior recorded.

**B: ringing**

- [ ] B1. Isolation: ring side open-circuit to logic GND and Ethernet shield (DMM, > 10 MΩ).
- [ ] B2. Ag1171 rings a WE 500 at 20 Hz. Vrms under load recorded.
- [ ] B3. Ag1171 at 25 Hz rings the same phone. Vrms recorded.
- [ ] B4. Every test phone rings with at least one module. Table of phone × module × frequency × Vrms × sound quality.
- [ ] B5. Black Magic rings the WE 500; Vrms recorded; gate latency measured.
- [ ] B6. Cadences `us`, `uk`, `short`, `us-double`: segment timing within ±20 ms (ESPHome) over 10 cycles.
- [ ] B7. QLab cue → bell sounding latency measured.
- [ ] B8. Stop latency: `/ring/stop` → output < 10 V.
- [ ] B9. Output short for 120 s: no damage, no excessive heat.
- [ ] B10. Hook detect (Ag1171) works / doesn't (recorded either way).
- [ ] B11. Ring-side supply current during ring recorded (sizes the DC/DC and decides board choice).
- [ ] B12. Subjective: a theatre person agrees it sounds like a real phone.

**Exit criteria for phase 1:** A1–A8 and B1, B2 (or B5), B4, B6, B8, B9 pass;
ring module and controller board chosen per SKU; pin maps updated; open
questions below answered or deferred with a reason.

## Open questions for owner

Decisions the bench can't make. Collected from all docs.

1. **Licensing** ([ADR-0008](decisions/0008-licensing.md)): CERN-OHL-S-2.0 /
   MPL-2.0 / CC BY-SA 4.0 as proposed, or W/P + MIT?
2. **Power architecture:** POE2 (non-isolated, 25 W) for Relay/Ringer, or keep
   ISO + a second power input? Is "PoE only" a hard requirement for every SKU?
3. **DC barrel fallback:** required on every SKU? ISO has no barrel jack, so it
   needs an ORing add-on.
4. **Ringer lid button default:** `hold` (drop-in manual ringer) vs `once`.
5. **Relay network-loss default:** `hold` vs `off`.
6. **Relay ratings to advertise:** low-voltage only (≤ 30 VDC / 24 VAC) in v1?
7. **Ringer output connector:** speakON + adapter cable, or 4 mm shrouded sockets?
8. **Off-hook detection** (auto-stop + "answered" message to QLab): in scope for v1 if the bench shows it works?
9. **GP "outputs":** 3.3 V logic vs open-collector (more useful for LEDs/buzzers/maglock relays)?
10. **Input box:** opto-isolated inputs vs plain pull-ups?
11. **"1 s on / 2 s off":** where did this come from? No NA standard was found
    (it matches Japan's ringback). Shipping it as `short`, not `us-*`.
12. **OSC default port** 8000 (proposed) OK?
13. **Security:** v1 has no auth on the show network. Acceptable, or add an optional passcode before v1?
14. **Sales regions** until CE/UKCA is understood: US-only? ([compliance.md](compliance.md))
15. **Name:** replace `showbox` before anything public (trademark search).
