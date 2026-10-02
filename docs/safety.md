# Safety and isolation

This page covers the design intent. It is not a certification and not legal
advice. The Ringer box is the main concern because it generates voltages well
above safe-to-touch limits. Relay boxes switch whatever the customer connects,
which can include mains.

## Hazard summary

| Hazard | Where | Mitigation (below) |
|---|---|---|
| Ringing voltage, ~60–90 Vrms AC (~85–127 V peak) | Ringer output | Isolation, current limiting, touch-safe connector, enclosure |
| Customer-connected voltage on relay contacts (possibly mains) | Relay and GP boxes | Relay ratings, creepage, terminal blocks, labeling, manual |
| Box connected to a real phone line | Ringer | Connector choice, label, manual |
| Unexpected actuation (motor, maglock, ringer) | All | Off at boot, network-loss policy, ring time limit ([ADR-0009](decisions/0009-safe-defaults-and-network-loss.md)) |
| PoE / Ethernet ground loops, USB damage | All | ISO board where practical; USB-while-PoE warnings for non-isolated boards |

### How dangerous is ringing voltage?

90 Vrms is about 127 V peak, superimposed on −48 VDC on a real line. That's
well above SELV (42.4 V peak / 60 VDC). Under IEC 60950-1 such circuits were
TNV. Under IEC 62368-1, a circuit carrying telephone ringing signals that meets
the limits in **Annex H** is classified **ES2**; beyond those limits it is
**ES3**. Medium confidence:
[ETSI EG 201 212](https://www.etsi.org/deliver/etsi_eg/201200_201299/201212/01.02.01_60/eg_201212v010201p.pdf),
[IEC 62368-1 preview](https://cdn.standards.iteh.ai/samples/23618/92449acef5b2481da95e6e59387999ad/IEC-62368-1-2018.pdf).
**The exact Annex H voltage/current/cadence limits were not retrievable from
free sources and must be checked in the standard itself.** Goal: design the
ringing output to meet ES2 per Annex H (a normal phone line's regime), and
treat it as if it were ES3 anyway for enclosure and connector choices.

## Ringer design requirements

### 1. Galvanic isolation (verified, not assumed)

The likely ring modules (Silvertel Ag1171, Cambridge "Black Magic") **share
ground** between their input and output ([ringer.md](ringer.md#key-finding-neither-front-runner-is-isolated)).
So the isolation barrier is ours:

```
 LOGIC SIDE (SELV, Ethernet-referenced)  ║  RING SIDE (floating HV island)
                                         ║
 board 5V/12V ──▶ [isolated DC/DC] ═════╬════▶ ring module supply
                                         ║
 ESP32 GPIO ───▶ [opto / digital isolator ╬════▶ RM, F/R (Ag1171)
                  or gate relay coil]    ║       or module DC input via relay contact
                                         ║
                                         ║   ring module ─▶ series R ─▶ fuse ─▶ shrouded jack
```

- Isolated DC/DC module rated ≥ 1.5 kV isolation (3 kV preferred). Part TBD
  ([BOM](../hardware/bom/README.md)).
- Control crossing: optocoupler / digital isolator rated ≥ 2.5 kVrms, or the
  gate relay (coil on logic side, contact on ring side; check the relay's
  coil-contact isolation rating).
- **Verification per unit:** with the box unpowered, measure resistance between
  each ring output pin and (a) the Ethernet shield, (b) logic ground, (c) DC
  input ground. Expect open circuit (> 10 MΩ on a DMM's top range). Phase 2:
  hipot test at a voltage chosen from the DC/DC rating.
- On the ESP32-POE-ISO board, the Ethernet/PoE side is also isolated from the
  logic (3000 VDC per Olimex). The ring output is then two barriers away from
  the network.

### 2. Current limiting

- **Series resistance** on the ring output so a short (or a finger) sees a
  current comparable to a real phone line. Value chosen on the bench: high
  enough to limit short-circuit current, low enough that the bell still gets
  ≥ 40–60 Vrms. The Black Magic LR12 datasheet requires ≥ 300 Ω series anyway
  (no internal short protection). The Ag1171's SLIC drivers are current-limited
  internally **[verify]**; add series R only if testing shows it's needed.
- **Fuse:** a resettable PTC or small fast-blow fuse in the ring output,
  sized above normal ring current and below the module's damage threshold.
  Value **[TBD on bench]**.
- **Short-circuit test** on the bench: dead short across the output for the
  maximum ring time (120 s). Nothing overheats, the fuse/PTC behaves, the box
  recovers.

### 3. Touch-safe output connector

Not an open screw terminal. Not RJ11. Candidates:

| Option | Part | Rating | Pros | Cons | Source |
|---|---|---|---|---|---|
| **Neutrik speakON NL4MPXX** (panel) | NL4MPXX | 250 VAC; contacts make only when locked; Neutrik says IEC 62368-1 compliant | Locking, finger-safe, nobody mistakes it for a phone jack, theatre crews own the cables | Prop phone needs an adapter cable (speakON → bare wires / RJ11 plug on phone side) | [Neutrik](https://www.neutrik.com/en/product/nl4mpxx) |
| 4 mm shrouded safety sockets | Hirschmann SEB 2620 (972356101 red / 972356100 black), or Stäubli SLB4-F | CAT III 1000 V, 32 A | Very cheap, test-lead-compatible | Not locking; easy to pull out mid-show; invites test leads | [Newark](https://www.newark.com/hirschmann-testmeasurement/972356101/socket-4mm-shrouded-red-pk5-seb/dp/72C1535), [Stäubli](https://www.staubli.com/global/en/electrical-connectors/products/t-m-products/products-for-test-accessories/sockets-2-mm-and-4-mm/panel-mount-socket-slb4-f.html) |
| RJ11 | — | — | Phone plugs straight in | **Rejected:** invites connecting to a real phone line, or a real line into the box; contacts not finger-safe | — |

**Proposed: speakON**, with a supplied adapter cable to the phone (RJ11 socket
or spade lugs on the far end, where a phone line can't reach the box side).
**[open]**

### 4. Physical separation and creepage

- Ring side (isolated DC/DC output, ring module, series R, fuse, output jack)
  in its own zone of the enclosure, separated from logic by distance and,
  where they would otherwise be close, an insulating barrier (e.g. polycarbonate
  sheet).
- High-voltage wiring routed and tied so it can't move into the logic zone if a
  wire comes loose.
- Creepage/clearance: target ≥ 3 mm between ring-side and logic-side conductors
  as a working figure. Real figures depend on the working voltage and
  pollution degree under IEC 62368-1. **[verify]** against the standard.
- Use only modules whose own isolation ratings are documented.

### 5. Labeling and manual

On the box, next to the output connector:

> **⚠ RINGING VOLTAGE. Connect to a prop telephone only.
> DO NOT connect to a live telephone line.**

The manual repeats this in the first section, explains why (it can damage
the exchange equipment and the box, and connecting to a live line is a
safety issue for telco workers), and says not to open the box while it's powered.

### 6. Firmware safety

- Ringer off at boot and on reset. Stop on network loss (default).
- `ring.max_seconds` hard limit (default 120 s).
- Watchdog resets a hung CPU, and a reset turns the ringer off.
- The lid button goes through firmware (no hardware bypass), so all limits apply
  ([ADR-0006](decisions/0006-ringer-lid-button.md)).

## Relay boxes

- Relay modules and terminal blocks rated for the voltage and current we
  advertise. **Proposed:** advertise relay boxes for **low-voltage loads only
  (≤ 30 VDC / 24 VAC, ≤ 2 A)** in v1 even if the relays are mains-rated. That
  avoids mains-safety claims (creepage, enclosure ratings, strain relief,
  protective earth) for an indie product. Users needing mains switching use the
  box to drive a contactor or a listed relay module. **[open]** This is a
  business decision as much as a safety one.
- Inputs are for dry contacts only. Document max cable length and suggest
  shielded cable near dimmers.

## Assembly and test

Every shipped unit gets a per-SKU test checklist (isolation resistance, ring
voltage, relay function, boot state, label present). Phase 1 drafts it:
[phase1-bench-plan.md](phase1-bench-plan.md).
