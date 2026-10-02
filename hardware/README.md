# Hardware

No custom PCBs ([ADR-0003](../docs/decisions/0003-off-the-shelf-parts.md)).
Each SKU is off-the-shelf modules wired by hand in an off-the-shelf enclosure.
This directory holds the wiring notes, pin maps, and per-unit test checklists.

| Dir | Contents |
|---|---|
| [common/](common/) | Controller board, power, I/O expander: shared by all SKUs |
| [general-purpose/](general-purpose/) | 2–4 relays, 2 inputs, 2 outputs |
| [relay/](relay/) | 8 relays |
| [input/](input/) | 8–12 contact-closure inputs |
| [ringer/](ringer/) | Ring generator, isolation, lid button |
| [bom/](bom/) | Bills of materials (CSV + generated markdown) |

Everything here is **draft** until the phase 1 bench tests pass
([plan](../docs/phase1-bench-plan.md)). Pin numbers marked **[verify]** come from
the Olimex manual plus general ESP32 knowledge and haven't been checked on a board.

Hardware documentation is licensed CERN-OHL-S-2.0 (proposed, see
[ADR-0008](../docs/decisions/0008-licensing.md)).
