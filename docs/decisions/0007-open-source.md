# 0007. Open hardware and open firmware; sell the assembled unit

- Status: Accepted
- Date: 2026-10-02

## Context

The audience (theatre technicians, escape room builders, makers) values being
able to repair, modify, and understand their gear. The designs are integrations
of off-the-shelf modules (ADR-0003), so there's little secret sauce to protect
in the schematic. The value we add is assembly, isolation and safety work,
testing, enclosure, documentation, and example show files.

## Decision

Publish wiring diagrams, BOMs, safety rationale, and firmware source. What we
sell is the assembled, tested, isolated, enclosed unit with docs and example
show files. Reflashing is permitted and the recovery path is documented, but
not advertised as a feature on the product page.

License choice is a separate decision: [ADR-0008](0008-licensing.md).

## Consequences

- Others can build and sell clones. Accepted; we compete on quality, support,
  and safety.
- Publishing the ringer's safety design invites scrutiny, which is good. It
  also means a DIY clone can be built badly. Docs must make clear that safety
  depends on the build, and that only units we built and tested are ours.
- Community contributions (show files for other platforms, translations) become possible.
- Trademark (the eventual product name) is how we distinguish our units from
  clones; open licenses don't grant trademark rights. Pick a name we can hold.
