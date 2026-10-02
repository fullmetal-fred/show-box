# 0001. Standalone devices, no inter-device communication

- Status: Accepted
- Date: 2026-10-02

## Context

Show control rigs fail at the worst moment. Systems built from cooperating
nodes (mesh networks, master/slave controllers, quorum-based clusters) add
failure modes that are hard to diagnose under show pressure: one node's
firmware bug or power loss can cascade. Our users already have a reliable
central brain: QLab (or similar) on the show computer.

## Decision

Each box is an independent device. QLab talks to each box directly. Boxes
never discover, depend on, relay through, or talk to each other. An Input box
that needs to fire a relay on another box does it by sending a message to the
show computer (or, if the user configures it, directly to the other box's IP
as an ordinary client; the target box doesn't know or care that the sender is
another showbox).

## Consequences

- A dead box affects only its own outputs. Every other box and the show
  computer keep working.
- Each box is testable in isolation, with only a laptop.
- No shared state, no firmware version coupling between boxes.
- Logic that spans boxes lives in the show file, where the operator can see it.
- We give up "smart" features like boxes mirroring each other or auto-grouping.
  That's intended.

## Alternatives considered

- **ESP-NOW / Wi-Fi mesh between boxes:** adds RF dependency and coupling. Rejected.
- **A hub box that fans out commands:** single point of failure. Rejected.
