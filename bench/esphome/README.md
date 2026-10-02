# ESPHome bench configs

| File | Purpose |
|---|---|
| `common-poe-iso.yaml` | Olimex ESP32-POE-ISO (WROOM) board + Ethernet + web server. Included by the others. |
| `gp-bench.yaml` | 3 relays (GPIO4/13/16), pulse buttons, 1 input that sends OSC to QLab |
| `ringer-ag1171.yaml` | Silvertel Ag1171: RM on GPIO4, F/R (20/25 Hz) on GPIO32 |
| `ringer-blackmagic.yaml` | Black Magic: gate relay on GPIO4 |
| `ringer-cadences.yaml` | Shared cadence scripts (us, uk, short, us-double, steady) |
| `secrets.example.yaml` | Copy to `secrets.yaml` |

```sh
pip install "esphome==2026.6.5"   # validated (config only) with this; avoid 2026.4.1, see esphome#15956
cp secrets.example.yaml secrets.yaml
esphome run gp-bench.yaml                 # first flash over USB
```

**Configs pass `esphome config` on ESPHome 2026.6.5 but have not run on hardware: [verify].** ESPHome config syntax moves between
releases (notably the Ethernet clock option, the `udp` component, and the
web-server REST URL format). If validation fails, fix it against the docs for
the pinned version and note the change in the bench results.

ESPHome web server REST endpoints used by the proxy (format per ESPHome docs
at the time of writing):

- `POST /switch/<id>/turn_on` · `turn_off` · `toggle`
- `POST /button/<id>/press`
