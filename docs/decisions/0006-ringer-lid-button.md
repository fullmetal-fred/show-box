# 0006. Ringer lid button uses the same code path as network commands

- Status: Accepted (default button mode: Proposed)
- Date: 2026-10-02

## Context

Existing theatrical phone ringers are manual push-button boxes. Many
productions will keep a human on the button at first, or need a manual fallback
when the network is down. If the Ringer box can't be used exactly like the box
it replaces, adoption is harder.

## Decision

- The Ringer has a momentary push button on the lid.
- The button does **not** switch the ring voltage directly. It is read by the
  ESP32 and calls the same internal ring functions as `/ring/start`,
  `/ring/stop`, and `/ring/once`. Same safety limit, same gating, same status
  reporting.
- The button's mapping is a setting (`ring.button_mode`): `hold` (ring while
  held, `steady` cadence: drop-in replacement for manual ringers), `once`, or
  `toggle`. See [protocol.md](../protocol.md#ringer).
- **Proposed default: `hold`**, because it matches the manual workflow exactly
  (the operator supplies the cadence by hand and stops the instant the actor
  answers). Pending owner decision.

## Consequences

- One code path to test; button and network can't disagree about state.
- The button works with no network at all, as long as the box has power.
- If the ESP32 is crashed/hung, the button does nothing. A hardware bypass
  (button wired in parallel with the gate relay) was considered and rejected:
  it would bypass the safety time limit and make the gate's state invisible to
  firmware. The watchdog ([architecture.md](../architecture.md)) must reset a
  hung ESP32, and a reset always leaves the ringer off.
- Debounce and press/release events must be handled carefully in `hold` mode
  (a bouncy release must not leave the ringer on). Covered by the safety limit
  as a backstop.

## Alternatives considered

- **Button hard-wired to the ring generator:** simplest, works when firmware
  is dead, but no safety limit, invisible to status. Rejected.
- **No button:** loses the drop-in-replacement story. Rejected.
