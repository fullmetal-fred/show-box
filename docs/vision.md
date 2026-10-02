# Vision

## The one-sentence version

A family of small, boring, reliable boxes that let a QLab cue click a relay,
read a switch, or ring a real telephone, without anyone writing code.

## Who it's for

- **Sound designers and show control operators** running QLab (primary), and
  later Isadora, Watchout, and similar tools.
- **Props people** who need a period phone to ring on cue and stop when the actor
  picks it up.
- **Escape room builders** wiring reed switches, buttons, and maglocks to a
  game controller or QLab.
- **Installation artists** who want a contact closure on the network.

Most of these people are not electrical engineers. They know what a cue is,
what an IP address is, and roughly what a relay does. Docs, labels, and the web
UI are written for them first.

## The problem

- Show control software speaks OSC and network messages fluently. Physical
  hardware mostly doesn't.
- The existing answers are either general-purpose controllers that need
  programming (Arduino, PLCs), big multi-function interfaces at a high price, or
  single-purpose manual gadgets.
- Theatrical phone ringers are a clear example: the common products are manual
  push-button boxes. As far as we have found (see [ringer.md](ringer.md)), none
  takes a network cue. Someone has to stand there and press the button.

## What we're building

Standalone, single-purpose-ish boxes:

| SKU | Core job |
|---|---|
| General Purpose | 2–4 relays, a couple of inputs and outputs. The "I need one contact closure" box. |
| Relay | 8 relays for screens, curtains, practicals via contactors, etc. |
| Input | 8–12 contact-closure inputs that send OSC/HTTP when they change. |
| Ringer | Rings a real analog phone from a cue, or from a lid button as a drop-in for manual ringers. |

Each box:

- Talks directly to the show computer. No hub, no mesh, no cloud, no app.
- Is powered by PoE, with a DC fallback.
- Boots fast into a known-safe state (everything off).
- Speaks OSC over UDP and HTTP, with human-readable addresses (`/relay/1/pulse`).
- Has a small built-in web page for setup and manual testing.
- Ships with an example QLab workspace with commented, ready-to-copy cues.

## Positioning

**We make appliances, not a platform.** One box, one job, plain OSC/HTTP, no
software to install. If you can type `/ring/start` into a QLab network cue, you
can use it. Competitors are building platforms (custom hardware + config
software + protocol extensions). We don't compete on breadth. See
[competitive-landscape.md](competitive-landscape.md).

- **No custom protocol.** Plain OSC and HTTP only ([ADR-0011](decisions/0011-no-custom-protocol.md)).
- **Launch order:**
  1. **Ringer** (flagship). Nobody who speaks show control makes one. The
     manual ringers are sold mostly to vintage phone collectors, with theater
     as a side market.
  2. **General Purpose** and **Input**, pitched as "same simple protocol, more I/O."
  3. **Relay** (8-ch), once the power architecture is settled.

  *Tradeoff:* the Ringer has the clearest market gap, but it's also the hardest
  SKU to ship: high-voltage isolation, the tightest power budget, the most
  compliance questions, and the most liability. Leading with it means the
  first product carries the most risk, and it gates revenue on the slowest
  path. Building GP units in parallel on the same firmware (which will exist
  anyway) is a cheap hedge.
- **Serviceable by design.** Known-vendor, documented modules that a theater
  can swap mid-run (low-voltage side only; [ADR-0010](decisions/0010-defer-custom-pcb.md)).

## Principles (in priority order)

1. **A dead box never takes down the show or another box.** Standalone devices,
   no inter-device dependencies. ([ADR-0001](decisions/0001-standalone-devices.md))
2. **Determinism over convenience.** Same input, same output, same timing, every
   night of the run. No framework auto-updates changing behavior in the field.
   ([ADR-0004](decisions/0004-native-firmware-over-esphome.md))
3. **Safe by default.** Outputs off at boot. The ringer is galvanically isolated,
   current-limited, and touch-safe. ([safety.md](safety.md))
4. **Off-the-shelf over custom.** Assemble proven modules by hand. Pay more per
   unit to design, test, and support less. ([ADR-0003](decisions/0003-off-the-shelf-parts.md))
5. **Open.** Wiring, BOMs, and firmware are published. What we sell is the
   assembled, tested, isolated, enclosed unit, plus docs and show files.
   ([ADR-0007](decisions/0007-open-source.md))
6. **Written for the person holding the cue sheet,** not the person holding the
   soldering iron.

## Business shape

- Low-volume indie hardware (Tindie-style). Every unit assembled and tested at a
  home bench.
- Pricing hypothesis: 3–4× parts cost. General Purpose ≈ $179; Ringer $199–$249
  (lean $199). Unvalidated.
- Differentiators: network-native ringer (market gap), example show files per
  SKU, docs for non-engineers, safety design you can read.

## Not now

Custom PCBs, enclosure design / 3D printing, overseas fabrication, Dante or any
audio, certification testing, MIDI / RTP-MIDI. None of the early design choices
should rule out an audio box later. ([architecture.md](architecture.md#future-audio-box))
