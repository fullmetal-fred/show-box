# 0011. Plain OSC and HTTP only; no custom protocol or OSC extension

- Status: Accepted
- Date: 2026-10-02
- Related: [0002](0002-osc-and-http-not-midi.md)

## Context

At least one competitor (Show Technologies) is building its own OSC extension
(XOSC) along with configuration software ([competitive-landscape.md](../competitive-landscape.md)).
A custom protocol layer can enable richer features: discovery, typed device
models, patching. It also means users need the vendor's software, or other
tools need to adopt the extension.

## Decision

The boxes speak **plain OSC 1.0 over UDP and plain HTTP/JSON**, nothing else.

- No custom framing, no required handshake, no proprietary extension, and no
  companion software required to send a command.
- Anything QLab, TouchOSC, Companion, `curl`, or a browser can send is enough
  to use every feature.
- Configuration happens in the box's built-in web page, not an installed app.
- Conveniences (e.g. mDNS service records, `/status` JSON) must be optional
  and built on existing standards.

## Consequences

- No lock-in, which is part of the pitch: "it works with what you already have."
- We give up a vendor-controlled discovery/patching ecosystem. If customers
  later need multi-box management, it will be a separate optional tool that
  speaks the same public protocol, not a requirement.
- If an open standard for show-control device description emerges and gets
  real adoption, we can *add* support for it alongside plain OSC. That would
  need a new ADR.
