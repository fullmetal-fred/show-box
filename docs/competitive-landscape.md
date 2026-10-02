# Competitive landscape

Status: draft. Facts marked *(owner)* come from the project owner's notes and
haven't been independently checked yet. A verification pass is in progress.

## Summary

| | Show Technologies ShowIO | Manual ring generators | showbox |
|---|---|---|---|
| Shape | Platform: custom I/O node + ShowNET software + XOSC protocol extension | Single-purpose manual gadget | Appliance: one box, one job |
| Control | Serial, Ethernet, Wi-Fi; DMX, sACN, Art-Net; OSC + XOSC *(owner)* | Push button; some offer an RF wireless remote | Plain OSC/UDP + HTTP; lid button on the Ringer |
| Software needed | ShowNET for programming/config/patching *(owner)* | None | None (built-in web page) |
| Hardware | Custom PCB *(owner)* | Custom, battery or AC | Off-the-shelf modules ([ADR-0010](decisions/0010-defer-custom-pcb.md)) |
| Phone ringer | Not that we know of | Yes, that's all they do | Yes (flagship) |
| Price | No public pricing; Early Adopter Program *(owner)* | ~$100–140 ([ringer.md](ringer.md#market-gap)) | GP ~$179, Ringer $199–249 (hypothesis) |
| Buyers | Theater, escape rooms, haunted houses, QLab users *(owner)* | Vintage phone collectors first, theater second *(owner)* | Theater / show control first, escape rooms second |

## Show Technologies (show-technologies.com)

*(owner)* ShowIO C44 is a networked I/O controller and show control node
(serial, Ethernet, Wi-Fi) on a custom PCB. Show Technologies is building a
platform around it: ShowNET software (programming, device config,
multiprotocol patching) and XOSC, their own OSC extension, which they say will
become an open standard. It also supports DMX, sACN, and Art-Net. It's
currently in an Early Adopter Program with no public pricing. Same target
buyers as us.

**What this means for us:**

- They're the closest competitor for GP/Input/Relay buyers, and they'll
  probably out-feature us on breadth. We shouldn't try to match that.
- Our pitch against them is *no software, no new protocol, works with what you
  already have* ([ADR-0011](decisions/0011-no-custom-protocol.md)), plus the ringer.
- Risk: if XOSC does become a widely adopted open standard, "plain OSC only"
  could start to look dated. Watch it. Adding support later is a new ADR, not a
  redesign, since XOSC is described as an OSC extension.
- Risk: they could add a ringer. The ringer's moat is the work in safety,
  isolation, and cadences, plus being first. That's thin, so speed matters.

## Manual theatrical ring generators

*(owner)* Push-button units around $100 (Old Phone Shop, TeleRing, eBay
sellers). Some offer RF wireless remotes. None takes a network or show
control cue. They're sold mainly to vintage phone collectors, with theater as
a side market.

Our earlier research ([ringer.md](ringer.md#market-gap)) found list prices of
$120–138 for the Old Phone Shop and Oldphoneworks units, plus add-ons sold
separately: a ~$85 cadence adapter and a ~$61 wireless remote. So a theater
that wants cadence and remote control is already paying **~$265** for a
manual system. That comparison makes a $199–249 network ringer look
reasonable, and is worth using in the pitch. (Medium confidence on the prices.)

## Other networked show-control I/O

*Pending verification pass.*
