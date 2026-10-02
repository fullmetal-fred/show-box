#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Regenerate hardware/bom/README.md from hardware/bom/bom.csv."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "hardware/bom/bom.csv"
MD = ROOT / "hardware/bom/README.md"

HEADER = """# Bills of materials

Machine-readable source: [`bom.csv`](bom.csv). This table is generated from it
(`python3 tools/bom_to_md.py`); edit the CSV, not this file.

`price_status`: **snippet** = from a search-result snippet, not a live page;
**estimate** = from the original brief; **unverified** = unknown. Treat every
price as unconfirmed. `TODO` = not chosen yet (no part numbers are invented).
"""

FOOTER = """## Cost notes

- The brief estimated the Olimex board at ~$20. It's about EUR 25 at qty 1
  (~EUR 22.50 at 10+), before VAT and shipping.
- The ringer needs an isolated DC/DC converter and control isolation that the
  brief's estimate didn't include. Expect ringer parts at the top of the
  $75-85 range or above until those are priced.
"""


def main() -> None:
    rows = list(csv.DictReader(CSV.open()))
    out = [HEADER]
    for sku in dict.fromkeys(r["sku"] for r in rows):
        out += [f"## {sku}", "",
                "| Part | Supplier | Part # | Unit cost | Qty | Status | Notes |",
                "|---|---|---|---|---|---|---|"]
        for r in rows:
            if r["sku"] != sku:
                continue
            pn = f"[{r['part_number']}]({r['url']})" if r["url"].startswith("http") else r["part_number"]
            cost = "TODO" if r["unit_cost"] == "TODO" else f"{r['unit_cost']} {r['currency']}"
            out.append(f"| {r['part']} | {r['supplier']} | {pn} | {cost} | {r['qty']} "
                       f"| {r['price_status']} | {r['notes']} |")
        out.append("")
    out.append(FOOTER)
    MD.write_text("\n".join(out))


if __name__ == "__main__":
    main()
