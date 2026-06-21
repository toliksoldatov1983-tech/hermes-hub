#!/usr/bin/env python3
"""Malyarka Agent — Offline Demo Runner. No server, no live, no real orders."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from malyarka_agent import build_preliminary_result

DEMOS = [
    ("DEMO-001", {"items": [{"height_mm":1000,"width_mm":400,"quantity":2,"material":"МДФ","material_confirmed":True,"color":"белый","finish":"матовый"}],"material":{"raw":"МДФ","confirmed":True},"color":{"raw":"белый"},"flags":{}}, "ready", 0.8, False),
    ("DEMO-002", {"items":[{"height_mm":600,"width_mm":400,"quantity":5,"material":"дерево","material_confirmed":False,"color":"белый"}],"material":{"raw":"дерево","confirmed":False},"color":{"raw":"белый"},"flags":{"material_question":True}}, "blocked", 0, True),
    ("DEMO-003", {"items":[{"height_mm":800,"width_mm":500,"quantity":3,"material":"МДФ","material_confirmed":True,"color":"RAL 9010","finish":"матовый"}],"material":{"raw":"МДФ","confirmed":True},"color":{"raw":"RAL 9010","structured":"RAL 9010"},"flags":{}}, "ready", 1.2, False),
    ("DEMO-010", {"items":[{"height_mm":1000,"width_mm":400,"quantity":4,"material":"МДФ","material_confirmed":True,"color":"RAL 9010","finish":"матовый"},{"height_mm":600,"width_mm":300,"quantity":2,"material":"МДФ","material_confirmed":True,"color":"RAL 8017","finish":"глянцевый"},{"height_mm":800,"width_mm":500,"quantity":1,"material":"МДФ","material_confirmed":True,"color":"RAL 7016","finish":"матовый"}],"material":{"raw":"МДФ","confirmed":True},"color":{"raw":"RAL 9010","structured":"RAL 9010"},"flags":{}}, "ready", 2.36, False),
]

passed = 0
for name, card, exp_status, exp_area, exp_blocked in DEMOS:
    r = build_preliminary_result(card)
    ok = True
    if exp_status == "ready" and r["status"] != "ready_for_human_review": ok = False
    if exp_status == "blocked" and r["status"] != "blocked_disputed_data": ok = False
    if abs(r["total_area_m2"] - exp_area) > 0.01: ok = False
    if r["export_blocked"] != exp_blocked: ok = False
    status = "✅" if ok else "❌"
    if ok: passed += 1
    print(f"{status} {name}: status={r['status']}, area={r['total_area_m2']} m², blocked={r['export_blocked']}")

print(f"\n{passed}/{len(DEMOS)} passed")
