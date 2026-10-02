# 0010. Defer a custom PCB; off-the-shelf modules, DIN-rail where practical

- Status: Accepted (deferred, not rejected)
- Date: 2026-10-02
- Extends: [0003](0003-off-the-shelf-parts.md)

## Context

ADR-0003 chose off-the-shelf modules for early phases. This ADR records *why
we're deferring a custom board*, what would make us revisit it, and how to
make a module-based product look intentional rather than improvised.

A competitor ([Show Technologies ShowIO C44](../competitive-landscape.md)) is
built on a custom PCB. That's a reasonable choice for a platform company. It
isn't evidence that we need one.

## Decision

1. All early products use off-the-shelf modules: controller, relays, ring
   generator, isolation, terminals, enclosure. No custom PCB, including no
   carrier board, for now.
2. **Revisit when both are true:** a SKU's design has been stable through
   real shows (no wiring changes for a few months), *and* volume makes hand
   wiring the bottleneck or the cost driver.
3. **Likely next step when we revisit:** a simple *carrier* PCB that the
   same modules plug into (headers, terminal blocks, spacing for the ring-side
   isolation zone), fabbed in the US (e.g. OSH Park) and still hand-assembled.
   That gets most of the tidiness without taking on module-level design or
   certification.
4. **Polish path for now:** prefer DIN-rail-mountable controller, relay, and
   terminal modules in DIN-style enclosures for an intentional, industrial
   look. Alternates are in the [BOM](../../hardware/bom/README.md) (`din` rows).

## Rationale

- **Faster iteration.** Changing a design means rewiring, not a fab respin.
- **Certification leverage.** Pre-certified modules carry their own FCC
  authorization for the radio. **Caveat:** this covers the module's
  intentional-radiator authorization, not the finished product's
  unintentional emissions (Part 15 Subpart B), which still apply to the
  assembled box. It reduces the compliance work but doesn't remove it
  ([compliance.md](../compliance.md#fcc-part-15)).
- **Field serviceability as a feature.** A theater can swap a failed relay
  module mid-run instead of shipping the unit back. Replaceable, documented,
  known-vendor parts are a selling point, and the docs should say so.

## Limits on serviceability (safety)

User-swappable parts are limited to the **low-voltage side**: relay modules,
terminal plugs, the controller board.

The **Ringer's ring side** (isolated DC/DC, ring module, current limiting,
output connector) is **not user-serviceable**. Its safety depends on wiring,
spacing, and an isolation check after assembly ([safety.md](../safety.md)).
A user swap can quietly break isolation. The ring side is a sealed sub-assembly
that we replace as a unit, with a documented isolation re-test.

This needs to be explicit in the manual, because "swap the $8 module yourself"
is exactly the message we're otherwise promoting.

## Tradeoffs acknowledged

A custom board wins on density, polish, assembly time, and unit cost at volume.
It also allows things modules can't easily do, like tight integration of input
protection or a built-in ring generator. We give those up for now on purpose.

DIN-rail parts have their own costs:

- **Bigger and usually pricier** than bare modules. DIN relay modules often
  want 12/24 V coils, which runs into the PoE power budget
  ([architecture.md](../architecture.md#the-power-budget-problem)).
- **Theaters often don't have a DIN cabinet.** The box still has to sit on a
  shelf, gaffer-taped to a flat, or behind a set wall. The DIN look comes from
  DIN modules *inside* a portable enclosure with a short rail, not from asking
  customers to mount it in a cabinet. Escape rooms are more likely to have a
  control cabinet, so offering a bare DIN-mount variant later may make sense.

## Alternatives considered

- **Custom PCB now:** rejected for this phase, for the reasons above.
- **Bare modules on standoffs in a plastic box:** cheapest and smallest,
  but looks hand-made. Acceptable for bench and early units; DIN is the polish target.
