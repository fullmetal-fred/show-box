# 0003. Off-the-shelf modules, no custom PCB in early phases

- Status: Accepted
- Date: 2026-10-02

## Context

We're a tiny, low-volume operation. A custom PCB brings design time, layout
review, fab lead times, assembly, rework, and a support burden for every
revision. Certified, mass-produced modules (ESP32 PoE boards, relay boards,
ring generators) already exist and are cheap relative to our margins.

## Decision

Early phases use only off-the-shelf modules, carrier boards, connectors, and
enclosures, wired and assembled by hand. We accept a higher unit cost in
exchange for less custom design, test, and support burden. Selection criteria:

1. Available from at least one reputable distributor (prefer two).
2. Documented (schematic or datasheet available).
3. Uses a pre-certified radio/digital module where certification matters
   (FCC ID visible), see [compliance.md](../compliance.md).
4. For the ringer: galvanic isolation verified, not assumed ([safety.md](../safety.md)).

## Consequences

- Faster to first sale; any competent hobbyist can rebuild one from our docs
  (which is fine, see ADR-0007).
- Unit cost higher; enclosure internals are bulkier and involve more wiring.
- Supply risk: a module can be discontinued. Mitigation: note alternates in the
  BOM; keep firmware pin maps in per-SKU config so a substitute board is a config change.
- Hand wiring means per-unit test is mandatory (a test checklist ships with each
  SKU's hardware notes).

## Alternatives considered

- **Custom carrier PCB from day one:** cleaner assembly, lower unit cost at
  volume, but months of work before we know whether anyone buys. Deferred to a
  later phase, once a SKU's design is stable and selling.
