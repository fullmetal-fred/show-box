# Example QLab workspaces

**Placeholder.** One workspace per SKU will live here, with pre-built,
commented cues. A link/QR code in each box points to its workspace.

Planned files:

| File | Contents |
|---|---|
| `showbox-gp.qlab5` | Pulse/latch each relay, outputs, input → cue examples |
| `showbox-relay8.qlab5` | Screen up/down/stop pulses, all-off panic |
| `showbox-input.qlab5` | Cues fired by inputs 1–12 (`/cue/in1/start` …) |
| `showbox-ringer.qlab5` | Ring US / UK / count / stop; "phone answered" pattern |

## Until the files exist: build it yourself

1. **Settings → Network**: add a network patch named `showbox-1`.
   Destination: the box's IP address, port **8000**, type **OSC**.
2. Add a **Network cue**, patch `showbox-1`, type **OSC message**.
3. Type the message from the table in
   [docs/protocol.md](../../docs/protocol.md#qlab-quick-reference), e.g.
   `/relay/1/pulse 250` or `/ring/start us`.
4. GO.

### Receiving from an Input box

QLab listens for OSC on port 53000. By default, workspace OSC access with
**no passcode** doesn't allow Control, so incoming `/cue/…/start` messages are
ignored. In **Workspace Settings → Network**, enable **Control** for the
"No Passcode" row (on a private show network), then configure the input to
send `/cue/<number>/start` to the QLab machine on port 53000.

### Ringer pattern: "phone rings until answered"

- Cue A: `/ring/start us` (the phone starts ringing)
- Cue B (operator GOs when the actor lifts the handset): `/ring/stop`,
  then a sound cue with the voice on the line.

Authoring note: `.qlab5` workspaces are bundles. Commit them unzipped so diffs
are at least partially readable, and keep a cue-list printout (PDF) alongside
each one.
