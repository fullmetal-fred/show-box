# 0008. Licenses: CERN-OHL-S-2.0 (hardware), MPL-2.0 (firmware), CC BY-SA 4.0 (docs)

- Status: **Proposed — needs owner decision**
- Date: 2026-10-02

Not legal advice.

## Context

We publish hardware docs and firmware (ADR-0007). We want: improvements by
commercial cloners to come back to the community; no obstacle to using
proprietary off-the-shelf modules; and no obstacle to a future audio box that
may involve a proprietary SDK (e.g. an Audinate Dante module).

## Decision (proposed)

### Hardware: CERN-OHL-S-2.0 (strongly reciprocal)

The CERN-OHL v2 family has three variants: **P** (permissive), **W** (weakly
reciprocal), **S** (strongly reciprocal). Our designs are integrations of
off-the-shelf parts. All three variants exempt "Available Components" (parts
generally available from third parties, like the Olimex board or a ring
generator module), so choosing S costs us nothing on the module side. What S
adds: someone who ships a modified showbox must publish their modified design.
That fits ADR-0007 (compete on quality, but improvements stay open).

- Choose **W** instead if we want people to be able to embed a showbox design
  inside a larger proprietary product without opening the rest.
- Choose **P** if maximum adoption matters more than reciprocity.

### Firmware: MPL-2.0 (file-level copyleft)

The brief framed this as MIT vs GPL. Recommendation is a third option:

| | MIT | GPL-3.0 | **MPL-2.0** |
|---|---|---|---|
| Modifications to our files must be shared | No | Yes | **Yes** |
| Can combine with proprietary code (e.g. a vendor SDK) | Yes | **No** (whole binary must be GPL) | **Yes** (their files stay theirs) |
| Compatible with LGPL Arduino core/libraries | Yes | Yes | Yes |
| Familiar to hobbyists | Very | Very | Less |

The deciding factor is the someday audio box: Dante modules are driven by
vendor host code that may be under NDA or a proprietary license. GPL would
likely forbid linking that into the same firmware image; MPL-2.0 doesn't, while
still requiring changes to *our* files to be shared. MIT is the fallback if we
want zero friction and don't care about reciprocity. (Medium confidence that
the Dante concern is real; it depends on how Audinate licenses host-side code,
which we haven't checked.)

### Docs prose: CC BY-SA 4.0

Manuals, guides, and example show-file commentary. Share-alike matches the
hardware choice.

### Bench configs: MIT-0

`bench/esphome/` and `bench/osc-proxy/` are throwaway bench tooling, not
product firmware. Licensed MIT-0 (no attribution required) so anyone can paste
them into their own ESPHome setup.

## Consequences

- Three license files in the root plus a note in `bench/`. Each source file
  gets an SPDX header (`SPDX-License-Identifier: MPL-2.0`).
- If the owner picks differently, swap the files; nothing has been published yet.

## Open question for owner

Approve S / MPL-2.0 / CC BY-SA, or choose W or P for hardware and MIT for firmware.
