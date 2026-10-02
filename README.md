# showbox

> **Working name.** `showbox` is a placeholder. See [Renaming](#renaming).

Small, network-controlled I/O boxes for theatrical show control, escape rooms,
and interactive installations. Each box is a standalone ESP32 controller on
Ethernet, powered by PoE (with a DC fallback), triggered directly from show
control software. The primary client is **QLab**: a network cue fires an OSC
message, the box does one obvious thing.

The goal is boring reliability. Fire a cue, a relay clicks, a phone rings.

## Planned product line

| SKU | What it does | Status |
|---|---|---|
| **General Purpose** | 2–4 dry-contact relays, a couple of digital inputs and outputs | Phase 1 bench |
| **Relay** | 8 relay channels (screens, curtains, effects) | Planned |
| **Input** | 8–12 contact-closure inputs that fire OSC/HTTP at QLab | Planned |
| **Ringer** (flagship) | Rings a real analog telephone bell from a cue, or from a button on the lid | Phase 1 bench |
| Audio | Small audio output box | Someday, out of scope |

## How you use it (target experience)

1. Plug the box into a PoE switch. It boots in a few seconds with every output off.
2. Open `http://showbox-XXXX.local/` (or its static IP) to set a name and IP.
3. In QLab, add a Network cue: `/relay/1/pulse` to the box's IP, port 8000.
4. GO.

Every command is listed in [docs/protocol.md](docs/protocol.md), which is the
single source of truth for OSC and HTTP addresses.

## Repository layout

```
docs/                 Product and engineering docs
  vision.md           What we're building and for whom
  architecture.md     Hardware + firmware architecture
  protocol.md         OSC / HTTP command reference (source of truth)
  ringer.md           Ringer box: electrical specs, cadences, module candidates
  safety.md           Isolation and safety design
  compliance.md       FCC / CE / UKCA notes and open questions (not legal advice)
  phase1-bench-plan.md  Step-by-step bench proof + test checklist
  decisions/          Architecture Decision Records (ADRs)
hardware/             Per-SKU wiring notes (no custom PCB yet)
  bom/                Bills of materials (CSV + markdown)
firmware/             Product firmware (Arduino-ESP32, PlatformIO), per-SKU targets
bench/esphome/        Phase 1 bench-proof ESPHome configs. NOT product firmware.
bench/osc-proxy/      Tiny OSC -> HTTP bridge for bench testing ESPHome from QLab
examples/qlab/        Example QLab workspaces per SKU (placeholder)
tools/                Repo helper scripts (e.g. rename)
```

## Project status

Pre-alpha. Phase 1 is a bench proof: does the hardware do what we think, and
does a vintage phone actually ring? No product firmware is written yet. See
[docs/phase1-bench-plan.md](docs/phase1-bench-plan.md).

## Safety

The Ringer box generates roughly 90 V AC. It is designed to ring a prop phone
over a short cable and nothing else.

**DO NOT connect a showbox to a live telephone line.** See [docs/safety.md](docs/safety.md).

## Licensing

Proposed (pending owner sign-off, see [ADR-0008](docs/decisions/0008-licensing.md)):

- Hardware documentation (wiring, BOMs, drawings): **CERN-OHL-S-2.0** — [`LICENSE-HARDWARE`](LICENSE-HARDWARE)
- Product firmware (`firmware/`) and tools: **MPL-2.0** — [`LICENSE`](LICENSE)
- Docs prose: **CC BY-SA 4.0** — [`LICENSE-DOCS`](LICENSE-DOCS)
- `bench/esphome/` configs are bench tooling, separate from product firmware, MIT-0 (see that directory).

## Renaming

The name `showbox` appears in docs, the firmware product constant
(`firmware/include/product.h`), and the default hostname. To rename:

```sh
tools/rename.sh newname          # dry run: lists every file and line that would change
tools/rename.sh newname --apply  # rewrites showbox / ShowBox / SHOWBOX
```
