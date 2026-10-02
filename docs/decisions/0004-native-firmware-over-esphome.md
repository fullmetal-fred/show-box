# 0004. Native Arduino-ESP32 product firmware; ESPHome only for bench proof

- Status: Accepted
- Date: 2026-10-02

## Context

ESPHome can make an ESP32 with Ethernet click relays from a YAML file in an
afternoon. It's ideal for proving hardware. As product firmware it has
drawbacks for us:

- No native OSC receiver; its API is aimed at Home Assistant, with a REST web
  server as a secondary interface.
- Behavior is defined by the upstream framework, which changes regularly.
  Rebuilding with a newer ESPHome can change timing, defaults, or web endpoints.
  That conflicts with determinism and long-lived show files.
- Boot time and memory footprint include components we don't need.
- Our protocol ([protocol.md](../protocol.md)) is our own contract; we want full
  control of parsing, timing, and error behavior.

## Decision

- **Phase 1 bench proof:** ESPHome is allowed, purely to prove hardware fast
  (relay drive, Ethernet/PoE bring-up, and above all: does the ring generator
  ring a vintage handset?). If QLab needs to drive ESPHome during the bench
  phase, a small OSC→HTTP proxy runs on the show machine (`bench/osc-proxy/`).
  ESPHome configs live in `bench/esphome/` and are never shipped.
- **Product firmware:** native **Arduino-ESP32** (on ESP-IDF underneath), built
  with PlatformIO, one shared codebase with per-SKU build targets.
  - OSC via a small, well-understood library (candidate: CNMAT OSC), or a
    minimal in-house parser if libraries prove awkward. OSC 1.0 parsing is small.
  - Pin every dependency to an exact version (platform, core, libraries) in the
    build config. Upgrades are deliberate, tested, and noted in the changelog.
- Escalate to plain **ESP-IDF** only if Arduino gets in the way of timing or
  Ethernet control. Arduino-ESP32 exposes IDF APIs (esp_timer, FreeRTOS), so we
  can drop to IDF per-feature without a rewrite.

## Consequences

- We own more code: networking glue, settings, web UI, OTA. More work, full control.
- Firmware behavior only changes when we release it.
- The bench ESPHome configs and product firmware will diverge; that's fine.
  Bench configs exist to answer hardware questions, not to become product.

## Alternatives considered

- **ESPHome as product firmware:** see context. Rejected for product.
- **ESP-IDF from day one:** more boilerplate for the web server, OSC, and
  settings; Arduino's library ecosystem saves real time. Kept as an escape hatch.
- **MicroPython / CircuitPython:** GC pauses and slower boot conflict with
  deterministic timing. Rejected.
