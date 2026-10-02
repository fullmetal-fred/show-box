# 0005. Latch vs momentary chosen per command, not per channel

- Status: Accepted
- Date: 2026-10-02

## Context

Many relay controllers configure each channel as "latching" or "momentary" in
a settings page. In a show, the same relay is often used both ways: pulse a
projector screen controller's "down" contact, but hold a light on for a scene.
A per-channel setting hidden in a web UI means the meaning of a cue depends on
state the operator can't see in the show file.

## Decision

Every relay and output accepts every verb at all times:
`on` / `off` / `toggle` / `set` (latching) and `pulse [ms]` (momentary).
The cue says what it does. Pulse length has a per-channel default (factory
500 ms, runtime adjustable via `/config/.../pulse_ms` or the web UI, persisted),
and any `pulse` command can override it with an argument.

Overlap rules (pulse restarts on re-pulse; latching verbs cancel a pending
pulse) are specified in [protocol.md](../protocol.md#timing-and-state-semantics).

## Consequences

- A show file is self-describing. Swapping a box for a spare (with factory
  settings) behaves the same as long as cues specify pulse lengths.
- We recommend that cues specify `ms` explicitly when the length matters.
- No channel-mode setting to get wrong.

## Alternatives considered

- **Per-channel mode setting:** hidden state; rejected.
