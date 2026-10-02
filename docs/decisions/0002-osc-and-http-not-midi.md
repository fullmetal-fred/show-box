# 0002. OSC (primary) + HTTP (secondary); no MIDI / RTP-MIDI

- Status: Accepted
- Date: 2026-10-02

## Context

The primary client, QLab, sends OSC natively from Network cues. Other show
tools (Isadora, Watchout, TouchOSC, Bitfocus Companion, escape room platforms)
speak OSC, HTTP, or both. MIDI is widely supported in theatre but needs either
physical MIDI (cabling, interfaces) or RTP-MIDI (session setup, platform-specific
drivers on Windows, flaky discovery), and maps poorly to named, human-readable
commands.

## Decision

- **OSC over UDP** is the primary protocol. Addresses are human-readable
  (`/relay/1/pulse`).
- **HTTP** mirrors the same paths for scripts, the web UI, curl, and tools that
  don't speak OSC.
- Both are always on. No protocol toggles.
- **No MIDI, MSC, or RTP-MIDI** for now.
- [protocol.md](../protocol.md) is the single source of truth for both.

## Consequences

- One internal command dispatcher, two thin front-ends (OSC parser, HTTP router).
- Users who only have MIDI (e.g. a lighting console firing MSC) need a bridge
  on the show computer. QLab itself can bridge MIDI to OSC.
- UDP is fire-and-forget: a dropped packet means a missed cue. On a wired,
  dedicated show network loss is rare, but it's real. We document the risk;
  we don't add retries in the box. (Senders can send twice; most commands are
  idempotent, and `/ring/start` is explicitly double-fire safe.)

## Alternatives considered

- **RTP-MIDI / AppleMIDI:** support headache across OSes. Rejected for now;
  could be revisited as an add-on front-end since the dispatcher is protocol-agnostic.
- **OSC over TCP:** QLab supports it, but UDP is simpler, connectionless, and
  what users expect. TCP may be added later if needed.
- **sACN / Art-Net:** lighting protocols; good for continuous values, awkward
  for discrete triggers. Out of scope.
