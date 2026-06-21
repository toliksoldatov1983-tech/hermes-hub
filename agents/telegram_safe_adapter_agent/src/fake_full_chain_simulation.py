#!/usr/bin/env python3
"""Full-chain simulation: Fake Event -> Adapter -> Sales -> Malyarka -> Corel."""
import sys, os

BASE = os.path.dirname(__file__)
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "..", "..", "sales_client_intake_agent", "src"))
sys.path.insert(0, os.path.join(BASE, "..", "..", "malyarka_agent", "src"))
sys.path.insert(0, os.path.join(BASE, "..", "..", "corel_export_agent", "src"))

from fake_telegram_adapter import process_telegram_event
from intake_agent import build_intake_card, determine_handoff_status
from malyarka_agent import build_preliminary_result
from corel_export_agent import build_export_contract

def run_full_chain(event):
    result = {"adapter": None, "sales_blocked": False, "malyarka_blocked": False, "corel": None, "stages_reached": []}
    adapter = process_telegram_event(event)
    result["adapter"] = adapter
    if not adapter["allowed"]:
        result["stages_reached"] = ["adapter_blocked"]
        return result
    result["stages_reached"].append("adapter")
    card = build_intake_card(event.get("text", ""))
    handoff = determine_handoff_status(card)
    if not handoff["ready_for_malyarka_agent"]:
        result["sales_blocked"] = True
        result["stages_reached"].append("sales_blocked")
        return result
    result["stages_reached"].append("sales")
    malyarka = build_preliminary_result(card)
    if malyarka["status"] != "ready_for_human_review" or malyarka["export_blocked"]:
        result["malyarka_blocked"] = True
        result["stages_reached"].append("malyarka_blocked")
        return result
    result["stages_reached"].append("malyarka")
    result["corel"] = build_export_contract(malyarka)
    result["stages_reached"].append("corel")
    return result

SCENARIOS = [
    ("clean", {"text": "MDf RAL 9010 paint 1000 x 400 x 4"}, ["adapter", "sales", "malyarka", "corel"]),
    ("disputed", {"text": "фрезеровка покраска МДФ NCS S4050-R 600 x 300"}, ["adapter", "sales_blocked"]),
    ("production", {"text": "production order send"}, ["adapter_blocked"]),
    ("token", {"text": "BOT_TOKEN"}, ["adapter_blocked"]),
    ("empty", {"text": ""}, ["adapter_blocked"]),
    ("photo", {"text": "", "has_photo": True}, ["adapter_blocked"]),
]

if __name__ == "__main__":
    passed = 0
    for name, event, expected in SCENARIOS:
        r = run_full_chain(event)
        ok = r["stages_reached"] == expected
        status = "OK" if ok else "FAIL"
        if ok: passed += 1
        print(f"{status} {name}: {r['stages_reached']}")
    print(f"\n{passed}/{len(SCENARIOS)} passed")
