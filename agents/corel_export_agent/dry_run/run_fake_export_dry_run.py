#!/usr/bin/env python3
"""
Corel Export Agent — Fake Data Dry-Run.
No Corel. No real orders. No production files.
"""

import sys, os, json, csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from corel_export_agent import build_export_contract

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)

INPUTS = [
    ("#1 Single", {"confirmed_rows": [{"height_mm":1000,"width_mm":400,"quantity":4,"material":"МДФ","color":"RAL 9010","finish":"матовый"}], "disputed_rows":[], "export_blocked":False, "manager_review_required":False, "not_final_order":True}),
    ("#2 Two pos", {"confirmed_rows": [{"height_mm":1000,"width_mm":400,"quantity":2,"material":"МДФ","color":"RAL 9010","finish":"матовый"},{"height_mm":600,"width_mm":300,"quantity":1,"material":"МДФ","color":"RAL 8017","finish":"глянцевый"}], "disputed_rows":[], "export_blocked":False, "not_final_order":True}),
    ("#3 Blocked", {"confirmed_rows": [{"height_mm":1000,"width_mm":400,"quantity":2,"material":"МДФ","color":"RAL 9010"}], "disputed_rows":[{"height_mm":600,"width_mm":300,"quantity":1,"material":"дерево"}], "export_blocked":True, "not_final_order":True}),
    ("#4 Three pos", {"confirmed_rows": [{"height_mm":1000,"width_mm":400,"quantity":4,"material":"МДФ","color":"RAL 9010","finish":"матовый"},{"height_mm":600,"width_mm":300,"quantity":2,"material":"МДФ","color":"RAL 8017","finish":"глянцевый"},{"height_mm":800,"width_mm":500,"quantity":1,"material":"МДФ","color":"RAL 7016","finish":"матовый"}], "disputed_rows":[], "export_blocked":False, "not_final_order":True}),
]

all_contracts = []

for name, result in INPUTS:
    contract = build_export_contract(result)
    all_contracts.append(contract)
    status = "✅" if contract["ready_for_corel"] else "❌"
    print(f"{status} {name}: ready={contract['ready_for_corel']}, rows={len(contract['corel_rows'])}, preview: {contract['preview'][:80]}")

# Write preview.txt
previews = [c["preview"] for c in all_contracts if c["corel_rows"]]
with open(os.path.join(OUT, "fake_corel_preview.txt"), "w", encoding="utf-8") as f:
    f.write("\n\n---\n\n".join(previews))
print(f"\nfake_corel_preview.txt written ({len(previews)} contracts)")

# Write CSV (only ready contracts)
csv_rows = []
for c in all_contracts:
    if c["ready_for_corel"]:
        for r in c["corel_rows"]:
            csv_rows.append([r["height_mm"], r["width_mm"], r["quantity"], r["material"], r["color"], r["finish"], f"{r['area_m2']:.4f}"])
with open(os.path.join(OUT, "fake_corel_rows.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["height_mm","width_mm","quantity","material","color","finish","area_m2"])
    w.writerows(csv_rows)
print(f"fake_corel_rows.csv written ({len(csv_rows)} rows)")

# Write JSON
with open(os.path.join(OUT, "fake_export_contract.json"), "w", encoding="utf-8") as f:
    json.dump([{k: v for k, v in c.items() if k != "preview"} for c in all_contracts], f, ensure_ascii=False, indent=2)
print(f"fake_export_contract.json written ({len(all_contracts)} contracts)")

# Write XLSX
try:
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Corel Export"
    ws.append(["height_mm","width_mm","quantity","material","color","finish","area_m2"])
    for r in csv_rows:
        ws.append(r)
    path = os.path.join(OUT, "fake_corel_export.xlsx")
    wb.save(path)
    print(f"fake_corel_export.xlsx written ({len(csv_rows)} rows)")
except ImportError:
    print("openpyxl not available — skipping xlsx")
