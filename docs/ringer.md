# Ringer box

The flagship SKU: rings a real analog telephone's bell from a network cue, or
from a button on the lid.

> **Source quality warning.** The research behind this page used web search
> summaries. Fetching most primary PDFs (Silvertel, ETSI, ITU, Olimex,
> manufacturer sites) was blocked in the research environment. Every number
> below has a source link and a confidence level. Anything marked
> medium or lower must be checked against the primary document before it goes
> in a product manual.

## Market gap

Existing theatrical phone ringers are manual push-button units:

| Product | Price (approx.) | Notes | Source |
|---|---|---|---|
| Old Phone Shop Telephone Ring Generator | $119.99 | 2×9 V or AC. Accessories: Ring Cadence Adapter ~$84.99, wireless remote ~$61 | [1](https://www.oldphoneshop.com/products/telephone-ring-generator-for-testing-displays-props.html), [2](https://www.oldphoneshop.com/products/ring-cadence-adapter-for-theater.html), [3](https://www.oldphoneshop.com/products/wireless-telephone-ring-adapter-theater-remote.html) |
| Oldphoneworks Ring Generator | $137.94 | Battery / AC / combo models | [link](https://oldphoneworks.com/products/oldphoneworks-ring-generator) |
| Tele-Q 70-9100 | — (discontinued) | 12–60 Hz adjustable, square wave, had a remote-control input on the jack | [link](http://www.tele-q.com/operating.php) |
| Precisiovision Stage Ringer (UK) | — | ~120 VAC, 25 Hz sine, preset cadences (3 or 6) | [link](http://www.precisiovision.freeuk.com/html/stage_ringer_specification.htm) |
| stagetelephone.co.uk Exchange in a Box | £128 | UK, ring + intercom, workshop-preset cadence | [link](https://stagetelephone.co.uk/product/exchange-in-a-box/) |
| theatertelephone.com Portable Ring Generator | — | specs not retrieved | [link](https://www.theatertelephone.com/portable-ring-generator/) |

Medium confidence on all of these. **None found takes OSC or any network cue.**
The closest are a wireless remote accessory and the Tele-Q's wired remote input.
The positioning claim holds, but cadence adapters and remotes exist, so "no
competitor has remote triggering" would be false. Say "no network/show-control
input" instead.

## Electrical requirements

| Region | Ringing voltage | Frequency | Confidence / source |
|---|---|---|---|
| North America | ~90 Vrms nominal (40–130 VAC range), superimposed on −48 VDC | 20 Hz | High (secondary source): [Sandman tech bulletin](https://www.sandman.com/knowledgebase/ring-voltage-tech-bulletin). Telcordia GR-57 / FCC 68 primary text **not read**. |
| UK (BT SIN 351) | 75 Vrms | 25 Hz | Medium (summary, not SIN text): [Wikipedia](https://en.wikipedia.org/wiki/British_telephone_socket) |
| Europe (ETSI) | ≥ 35 Vrms across load; ≤ 100 Vrms open circuit at the network termination point | 25 Hz ±8% recommended; 25 and 50 Hz common | Medium: [ETSI TR 101 188](https://www.etsi.org/deliver/etsi_tr/101100_101199/101188/01.01.01_60/tr_101188v010101p.pdf), [ETSI ES 201 970](https://www.etsi.org/deliver/etsi_es/201900_201999/201970/01.01.01_60/es_201970v010101p.pdf) |

**Minimum to ring a bell:** about 40 Vrms (US spec minimum into a 5 REN load).
Medium confidence: [epanorama](https://www.epanorama.net/circuits/telephone_ringer.html).

**REN:** US (FCC Part 68) 1 REN = 6930 Ω in series with 8 µF. Old European
definition: 1800 Ω + 1 µF. High confidence:
[accesscomms](https://www.accesscomms.com.au/ringer-equivalence-number-ren-explained/).
A mA-per-REN figure was **not verified**.

**Our design target (proposed):** ≥ 60 Vrms into 1 REN at 20 or 25 Hz,
selectable in software if the module allows it. One prop phone per output.
Short cable (< 10 m). No DC battery feed needed for a bell. (A real line's
−48 VDC matters for talk and hook detection, not for ringing a mechanical
bell.) **[verify]** that every test phone rings at 60 Vrms.

### Will one design ring "most phones"?

The brief assumes mechanical ringers tolerate the regional spread. Mostly
true, with one real exception:

- The Western Electric **C4A** (500-series set) ringer is optimized for 20 Hz
  with roughly flat response from just under 20 Hz to a bit over 30 Hz, so
  25 Hz should work. Medium confidence:
  [Bell Labs Record, Nov 1965](https://www.telephonecollectors.info/index.php/browse/catalogs-manuals-educational-docs-by-company/western-electric-bell-system/publications-and-educational-documents-by-date/blr/11586-65nov-blr-p395-designing-telephone-ringers/file),
  [classicrotaryphones forum](https://www.classicrotaryphones.com/forum/index.php?topic=11948.0).
- **Exception: party-line harmonic ringers** are deliberately frequency-selective,
  tuned to 16⅔, 25, 33⅓, 50, or 66⅔ Hz. A harmonic ringer tuned to another
  frequency **may not ring at 20 Hz**. Older props (e.g. some WE 300-series /
  317 sets) can have one. High confidence:
  [telephonecollecting.org WE317](http://www.telephonecollecting.org/Bobs%20phones/Pages/WE317/WE317.htm),
  [paul-f.com](http://www.paul-f.com/we300typ.htm).
  **Product implication:** software-selectable ring frequency (16–60 Hz) is
  worth having, and the manual should say how to spot a harmonic ringer.

## Cadence presets

A cadence is a list of on/off durations that repeats. One "cycle" = one pass
through the list.

| Name | Pattern (seconds, on/off/...) | Cycle | Source | Confidence |
|---|---|---|---|---|
| `us` | 2.0 on / 4.0 off | 6.0 s | Telcordia GR-506-CORE "Pattern 1", via [IETF draft-foster-mgcp-basic-packages-03](https://datatracker.ietf.org/doc/html/draft-foster-mgcp-basic-packages-03), [AudioCodes manual](https://techdocs.audiocodes.com/session-border-controller-sbc/mp-1288/user-manual/version-740/Content/UM/Distinctive%20Ringing.htm) | High |
| `us-double` | 0.8 on / 0.4 off / 0.8 on / 4.0 off | 6.0 s | GR-506 "Pattern 2" (distinctive ring), same sources | High |
| `uk` | 0.4 on / 0.2 off / 0.4 on / 2.0 off | 3.0 s | BT double ring, 25 Hz. [Wikipedia](https://en.wikipedia.org/wiki/British_telephone_socket), [sm0vpo](http://sm0vpo.altervista.org/_visitors/inst/ring-gen.htm) | Medium-high |
| `au` | 0.4 on / 0.2 off / 0.4 on / 2.0 off | 3.0 s | ITU national tones list (ringback) [ITU](https://www.itu.int/ITU-T/inr/forms/files/tones-0203.pdf) | Medium |
| `de` | 1.0 on / 4.0 off | 5.0 s | ITU national tones list (ringback) | Medium |
| `fr` | 1.5 on / 3.5 off | 5.0 s | ITU national tones list (ringback; 1.0/4.0 also listed) | Medium |
| `short` | 1.0 on / 2.0 off | 3.0 s | **No North American standard found.** Matches Japan ringing tone III in the ITU list. Kept as a stage-pacing preset. | — |
| `steady` | on, no off-phase | n/a | Built-in. Used by hold-to-ring and manual timing. | — |

Notes:

- **The brief's "1 s on / 2 s off" North American variant was not
  verified.** The only standard 1/2 pattern found is Japanese. It's still
  a useful stage preset (tighter pacing than 2/4), so it ships as `short`,
  without a claim that it's American. If a source turns up, rename it.
- The ITU list (Annex to ITU Operational Bulletin 781, and ITU-T E.180 Supp. 2:
  [link](https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-E.300SerSup2-199401-W%21%21PDF-E&type=items))
  gives **ringback tone** cadences heard by the caller. Usually the bell
  cadence matches, but the document doesn't specify the ringing current itself.
  Hence medium confidence on `au`, `de`, `fr`.
- No tolerances were found for any cadence. The firmware target is ±5 ms per
  segment, far tighter than anyone can hear.
- GR-506 patterns 3–5 exist; timings not verified, so they aren't included.
- Theatre rarely needs strict accuracy here. What matters is that the US preset
  sounds right to an American audience and the UK one to a British audience.

### User-defined cadences

Stored in settings: a name (lowercase, `[a-z0-9-]`, ≤ 16 chars) and 1–8 on/off
pairs, each 50–10000 ms, last off-phase may be 0. Up to 8 custom cadences.
Built-in names can't be overwritten.

## Ring generator candidates

Requirements: buy as a module; can be gated by the ESP32 (enable pin or by
switching its supply); ≥ 60 Vrms into 1 REN; known isolation status;
reasonable price and availability.

| Candidate | Input | Output | Control | Isolation | Price | Confidence | Sources |
|---|---|---|---|---|---|---|---|
| **Silvertel Ag1171** ringing SLIC (14-pin SIL module) | 3.3–5 V single supply (internal DC/DC) | ~60 Vrms into 1 REN; >40 Vrms into 3 tone-ringer REN | `RM` high + toggle `F/R` at ring frequency (datasheet: 20–25 Hz). **Cadence and frequency are in software.** Also has a switch-hook detect output (**[verify]** pin and behavior). | **Not isolated.** No transformer; line drivers powered from internal DC/DC referenced to supply ground (inference, medium confidence) | ~$8.76 (Newark, qty 1) | High (isolation: medium) | [Silvertel](https://silvertel.com/ag1171/), [datasheet](https://silvertel.com/images/datasheets/Ag1171-datasheet-Low-cost-ringing-SLIC-with-single-supply.pdf), [Newark](https://www.newark.com/silvertel/ag1171-s/subscriber-line-interface-circuit/dp/08AM1737) |
| Silvertel Ag1170 | 3.3/5 V | 3 REN square, or 2 REN at 40 Vrms sine | Same RM / F/R scheme | Same as Ag1171 (assumed) | — | Medium | [datasheet](https://www.mouser.com/datasheet/3/3726/1/Ag1170_datasheet_SLIC_module_onboard_ringing.pdf), [AN1170-41](https://www.silvertel.com/images/appsnotes/AN1170-41-Ag1170-Sine-Wave-Ringing-Explained.pdf) |
| **Cambridge Electronics Labs "Black Magic"** (e.g. LR12 sine, or square variants) | 5 / 12 / 24 / 48 V versions. LR12: 11.5–12.5 V, 150 mA idle | LR12: ~86 Vrms, 5 W intermittent, ~5 REN | Sine: driven by an external reference waveform (MCU PWM/DAC). Square: free-running, gate by supply. | **Not isolated.** Drive is referenced to COM, which "ordinarily" goes to system ground | ~$31 (12 V square), ~$39 (12 V sine), ~$29 (5 V square, eBay) | Medium-high | [camblab OEM list](https://www.camblab.com/oem_list/oem_list.htm), [LR12 datasheet](https://www.camblab.com/datashts/lr12.pdf), [app help](https://www.camblab.com/lit/bmrhelp1.pdf) |
| PowerDsine PCR-SIN03V12F20-C (surplus) | 12 VDC | 70 Vrms, 20 Hz, 3 W | Yellow INHIBIT wire | Unknown, no datasheet | ~$25 eBay | Medium (seller listings) | [eBay](https://www.ebay.com/itm/253414551080) |
| LT1684 DIY | Needs a separate HV supply | Sine, programmable | Capacitively isolated PWM input | Depends on design | IC only | High (it exists), but it's a custom design | [datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/1684f.pdf), [design note](https://www.analog.com/en/resources/design-notes/telephone-ring-tone-generation.html) |
| Viking RG-10A | 13.8 VAC adapter | 90 VAC | **Ring booster only.** Needs incoming ring voltage | — | — | High | [Viking](https://vikingelectronics.com/products/rg-10a/) |
| Viking DLE-200B line simulator | — | 2 REN | No enable input; rings on the other phone's off-hook | — | ~$106–122 | Medium | [link](https://www.thetelecomspot.com/products/viking-electronics-dle-200b-two-way-phone-line-simulator-with-dial-tone-dle-200b) |

Not found / unverified: Silvertel Ag2130, Teltone simulators as embeddable
modules, generic AliExpress "ring generator" modules.

### Key finding: neither front-runner is isolated

Both practical modules (Ag1171, Black Magic) share ground between their
low-voltage input and the high-voltage output, so **the isolation barrier must
be ours**. Off-the-shelf parts still cover it:

1. An **isolated DC/DC converter module** (rated isolation ≥ 1.5 kV, ideally
   3 kV) powers the ring module from the logic supply. This puts the ring
   module on its own floating island.
2. Control signals cross the barrier through an **optocoupler, digital
   isolator, or the coil-to-contact gap of the gate relay**. Never a shared wire.

Details: [safety.md](safety.md).

### Recommendation for the bench

Buy and test **both** (low cost, answers different questions):

- **Primary: Ag1171** behind an isolated 5 V→5 V DC/DC, with `RM` and `F/R`
  driven through a 2-channel digital isolator or optos.
  - Why: cheapest; ring frequency selectable in software (20 Hz US, 25 Hz UK/EU);
    cadence fully in software; SLIC drivers are inherently current-limited;
    switch-hook detection could enable **auto-stop when the actor lifts the handset**
    and send an "answered" OSC message to QLab (see below).
  - Risk: ~60 Vrms is at the low end. May be marginal for some old bells or
    long runs. That's the main bench question.
  - Risk: the isolated DC/DC must cover the Ag1171's peak input current during
    ringing (**[verify]** from datasheet; size the converter with margin).
- **Fallback: Black Magic 12 V square** (or LR12 sine) behind an isolated
  12 V→12 V DC/DC, gated by a relay on its DC input (the relay is also the
  control isolation).
  - Why: ~86–90 Vrms like a real line, rings up to ~5 REN.
  - Risks: frequency fixed (square) or needs a waveform drive (sine); idle draw
    150 mA (LR12) if left powered; **not short- or reverse-protected, needs
    ≥ 300 Ω series resistance** per its datasheet; needs a 12 V rail (POE2 or
    external supply, see [architecture](architecture.md#the-power-budget-problem)).

Gating the Black Magic by switching its **input** (not its output) avoids
switching high voltage and saves idle power, but adds start-up delay. Bench
test measures that delay ("time from GO to bell").

### Opportunity: off-hook detection

If the Ag1171's hook-detect works with a mechanical-bell phone on our short
loop, the Ringer can:

- stop ringing automatically when the handset is lifted (like a real phone line), and
- send a configurable outbound message (`/cue/answered/start` to QLab) so the
  voice-on-the-line cue fires on pickup, with no operator.

That's a strong differentiator and fits the Input-box outbound machinery.
Not in protocol v0.1. Addresses reserved (`/ring/hook`). Decision **[open]**.

## Command summary

See [protocol.md](protocol.md#ringer) for the authoritative list:
`/ring/start [cadence]`, `/ring/once [cadence]`, `/ring/count <n> [cadence]`,
`/ring/stop`, `/ring/cadence <name>`. Safety time limit `ring.max_seconds`
(default 120). Lid button modes `hold` / `once` / `toggle`.
