# Competitive landscape

Status: draft, 2026-10-02.

**Sources.** *(owner)* = from the project owner's notes. Everything else comes
from a web research pass that could only read search-engine snippets: the
proxy blocked show-technologies.com, controlgeek.net, and most vendor sites.
Confidence: **H** = several snippets agree, or a distributor listing;
**M** = one snippet; **L** = inferred.

## Summary

| | Show Technologies ShowIO | Manual ring generators | showbox |
|---|---|---|---|
| Shape | Platform: I/O nodes + config software + protocol extension *(owner)* | Single-purpose manual gadget | Appliance: one box, one job |
| Control | OSC over Ethernet is the core protocol (H). Serial, Wi-Fi, DMX, sACN, Art-Net *(owner, not verified)* | Push button; some offer an RF wireless remote | Plain OSC/UDP + HTTP; lid button on the Ringer |
| Software needed | ShowNET for config/patching *(owner, not verified)* | None | None (built-in web page) |
| Hardware | Custom PCB *(owner)* | Custom, battery or AC | Off-the-shelf modules ([ADR-0010](decisions/0010-defer-custom-pcb.md)) |
| Phone ringer | None found | Yes, that's all they do | Yes (flagship) |
| Price | **$200/unit, $60 bare board** (M, see below) | $90–230 | GP ~$179, Ringer $199–249 (hypothesis) |

## Show Technologies (show-technologies.com)

**Owner's notes:** ShowIO C44 is a networked I/O controller and show-control
node (serial, Ethernet, Wi-Fi) on a custom PCB. Around it they're building a
platform: ShowNET software (programming, device config, multiprotocol
patching) and XOSC, their own OSC extension, which they say will become an
open standard. It also supports DMX, sACN, and Art-Net. Early Adopter Program,
no public pricing. Same buyers as us: theater, escape rooms, haunted houses,
QLab users.

**What the research pass found (snippets only):**

- Founded fall 2024 by Purdue alumni Shep Dick, Trevor Marshall, and Xiong
  Wang (H, Purdue CLA news).
- **ShowIO /DIGITAL/COMBO/8**: 4 inputs (12–24 V), 4 outputs (2 A). **OSC is
  the core protocol**, over 10/100 Ethernet (H).
- **Price: $200 per unit, or $60 for the bare board**, per John Huntington's
  controlgeek.net blog, Aug 2026 (M). **This contradicts "no public pricing"**
  in the owner's notes. Check the blog post directly.
- "Widely available May 2026"; Early Adopters get pre-release units and
  priority support (M).
- Lists integration with QLab, Eos, grandMA, Medialon, Q-Sys, TouchOSC (M).
- **Not confirmed by any snippet:** the C44 model specifically (L), PoE,
  serial/DMX/sACN/Art-Net, Wi-Fi, ShowNET as their product (search results
  returned an unrelated Laserworld product), and an XOSC spec (results
  returned x-io's unrelated x-OSC board).
- No ringer product found.

### What this means for us

- **They're closer to us than "platform vs appliance" implies.** If ShowIO
  speaks plain OSC natively at about $200 with 4 in / 4 out, then the General
  Purpose box (~$179, 2–4 relays) is close to a direct substitute. Our
  differences on GP are smaller than for the ringer: dry-contact relays (their
  outputs may be driven 2 A rather than dry contacts **[verify]**), PoE, no
  software required, HTTP, and open firmware.
  **The GP/Input SKUs need a sharper reason to exist than "simpler."**
  Candidates: PoE-only power, open source, example show files, docs for props
  people, price.
- **The ringer is the clear gap.** Nobody who speaks show control makes one.
  That supports launching it first.
- Risk: if XOSC becomes a widely adopted open standard, "plain OSC only" could
  look dated. Adding support later is a new ADR, not a redesign
  ([ADR-0011](decisions/0011-no-custom-protocol.md)).
- Risk: they could add a ringer. The moat is the safety, isolation, and
  cadence work, plus being first. That's thin, so speed matters.

## Manual theatrical ring generators

*(owner)* Push-button units around $100 (Old Phone Shop, TeleRing, eBay
sellers). Some offer RF wireless remotes. None takes a network or show-control
cue. They're sold mainly to vintage phone collectors, with theater as a side
market.

Prices found (M, eBay listings and vendor snippets):

| Product | Price |
|---|---|
| TeleRing plug-in (RGA) / battery (GRB) | $89.95 |
| TeleRing with cadence (GRC) | $139.95 |
| TeleRing wireless | $119.95 |
| **TeleRing all-in-one wireless (RGWC)** | **$229.95** |
| Old Phone Shop Telephone Ring Generator | $119.99 (+ cadence adapter ~$85, wireless remote ~$61) |
| Oldphoneworks Ring Generator | $137.94 |
| stagetelephone.co.uk Exchange in a Box (UK) | £128 |

**Pricing implication:** the closest feature match to our Ringer (cadence +
remote) already sells at **$230–266**. A $199–249 Ringer with network cues,
lid button, presets, and safety design is priced in line with that, not above
it. This supports $249 more than the "lean $199" in the brief. (Medium confidence.)

None of these advertises OSC or network control (M).

## Other networked show-control I/O

| Product | Price band | OSC? | Notes |
|---|---|---|---|
| Nemesis Research OSCA-IO16 | £1,600–2,400 | Yes, native | 16 isolated GPI, 16 relays (0.5 A). High-end |
| Kiss-Box IO3CC + cards | $384 cage + ~$136/card | Not stated (UDP/TCP, Art-Net, RTP-MIDI, Modbus) | Modular |
| Alcorn McBride IO64 / AMIO | IO64 ~$300 used | Not verified | 32 in / 32 relays; theme-park pedigree |
| ENTTEC S-Play | unverified | Yes (OSC/HTTP API) | Primarily a lighting playback device with contact closure and RS232 |
| Electroconcept relay board | unverified | Yes (also Art-Net/sACN/DMX) | 8 out / 6 in |
| Escape Room Master controller V2 | $199 | No (own software) | 4 in / 4 out + audio |
| Escape Room Techs Ethernet kit | $185 | No (MQTT, Houdini, Clue Control) | Escape-room platform integration |
| Escape Room Supplier puzzle controller | $149–179 | Not stated | |

Takeaways:

- Above ~$1,000 (Nemesis, Kiss-Box, Alcorn) is pro-installation gear. Not our buyers.
- The **$150–200 band** is crowded: ShowIO, escape-room controllers. They
  usually speak their own platform's language (MQTT, Houdini, Clue Control)
  rather than OSC.
- **Escape-room buyers may need MQTT or platform integrations** more than OSC.
  If the Input box targets escape rooms, check which room-control software
  they actually run before assuming OSC/HTTP is enough. **[open]**
- Off-the-shelf DIN I/O boards (Waveshare, KinCony, ~$50–70; see
  [BOM](../hardware/bom/README.md) `din` rows) set a floor on what buyers will
  pay for bare I/O. Our price has to be justified by firmware, docs, testing,
  and show files, not the hardware.
