# Compliance notes

> **Not legal advice.** These are engineering notes to frame questions for a
> compliance consultant or test lab. Nothing here has been confirmed by one.

## Summary

| Regime | Applies? | Our position | Confidence |
|---|---|---|---|
| FCC Part 68 (terminal equipment connected to the telephone network) | Probably **not** | Ringer drives a closed loop to a prop phone and never connects to the PSTN | Medium |
| FCC Part 15 (unintentional / intentional radiators) | **Yes** | Digital device; use pre-certified radio module; verify unintentional-emitter obligations | Medium |
| Product liability / general safety | **Yes** | Main real-world exposure; addressed by isolation design ([safety.md](safety.md)) | High |
| EU CE (EMC, LVD, RED, RoHS) | If sold to EU | Open question | — |
| UK UKCA | If sold to UK | Open question | — |
| Canada ISED | If sold to Canada | Open question | — |

## FCC Part 68

Part 68 governs equipment connected to the public switched telephone network.
The Ringer box generates ringing voltage for a phone that is connected only to
the box. It never connects to the network.

- Design so that it **can't plausibly be connected to a phone line**: no RJ11 on
  the box (see [safety.md](safety.md#3-touch-safe-output-connector)), plus
  label and manual warnings.
- The FCC Part 68 text is at <http://www.tscm.com/FCC47CFRpart68.pdf> (secondary
  copy; use eCFR for the current text). Not reviewed in detail.
- Open: does including an RJ11 *adapter cable* (phone side) change anything? We
  think not, because it doesn't connect to the network, but ask.

## FCC Part 15

- The ESP32 has Wi-Fi/Bluetooth radios, so it's an intentional radiator even
  if we only use Ethernet.
  - Plan: **disable Wi-Fi and Bluetooth in firmware** (never initialize the radio).
  - Use a board built on a **pre-certified module**: the ESP32-WROOM-32E has FCC ID
    **2AC7Z-ESP32WROOM32E** (<https://fccid.io/2AC7Z-ESP32WROOM32E>, high
    confidence). The final product label then carries
    "Contains FCC ID: 2AC7Z-ESP32WROOM32E".
  - Open: modular approval has conditions (antenna, host integration,
    labeling). Using the module's certification when the radio is disabled is
    a question for a lab. Some host-product testing may still be required.
- The **unintentional radiator** side (the ESP32 clock, Ethernet, the ring
  generator's switch-mode converter, the isolated DC/DC) is a "digital device".
  Class A (commercial/industrial) vs Class B (residential) matters: theatres and
  escape rooms are commercial, but a hobbyist could use it at home.
  - Open: which class, and does a small manufacturer need verification
    testing or a Supplier's Declaration of Conformity (SDoC)? SDoC still
    requires testing to show compliance. Budget for a pre-scan at a lab.
- Whether the Olimex boards carry their own FCC authorization: **unverified**.

## Product liability

The realistic risk for a small seller is a shock or fire claim, not an FCC
enforcement action. Mitigations:

- The isolation, current-limiting, connector, and labeling design in
  [safety.md](safety.md).
- A documented per-unit test, with records kept per serial number.
- Clear intended-use statements: prop phones only; relay boxes for low-voltage
  loads (if adopted).
- Open: product liability insurance for a Tindie-scale seller. Cost and
  availability.

## International

Out of scope for phase 1, listed so they aren't forgotten:

- **EU CE marking:** likely EMC Directive; the Low Voltage Directive applies to
  50–1000 VAC / 75–1500 VDC. The ringing output (~60–90 Vrms) sits in that
  range (generated internally, not the supply), so it's an open question
  whether LVD applies. RED applies if the radio is present (even if disabled?
  open). RoHS for all parts. WEEE registration per country.
- **UK UKCA:** parallel to CE for GB.
- **Canada ISED:** ICES-003 for digital devices; module IC ID for the radio.
- Tindie and similar platforms sell internationally by default. Decide
  whether to restrict shipping destinations until compliance is understood.

## Open questions (for owner / consultant)

1. Confirm FCC Part 68 doesn't apply to a closed-loop ring generator sold for
   prop use.
2. FCC Part 15: Class A or B? SDoC path and expected test cost for each SKU
   (Ringer separately, since it has extra switch-mode converters).
3. Does using a pre-certified module carry over when the radio is disabled, and
   what label text is required?
4. Does IEC 62368-1 Annex H (ES2 ringing limits) apply as a design target, and
   what are its exact limits?
5. CE/UKCA: which directives apply? Is LVD triggered by an internally generated
   60–90 Vrms output?
6. Do we restrict sales to the US (and maybe Canada) until the above is resolved?
7. Product liability insurance.
