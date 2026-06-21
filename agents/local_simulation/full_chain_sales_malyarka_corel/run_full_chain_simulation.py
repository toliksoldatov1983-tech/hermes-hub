#!/usr/bin/env python3
"""
Full-Chain Local Simulation: Sales → Malyarka → Corel Export.
No Telegram. No API. No server. No live. No real orders.
"""

import sys, os

BASE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE, "..", "..", "sales_client_intake_agent", "src"))
sys.path.insert(0, os.path.join(BASE, "..", "..", "malyarka_agent", "src"))
sys.path.insert(0, os.path.join(BASE, "..", "..", "corel_export_agent", "src"))

from intake_agent import build_intake_card, determine_handoff_status
from malyarka_agent import build_preliminary_result
from corel_export_agent import build_export_contract

MESSAGES = [
    ("#1 All clear", "1000 400 4 шт МДФ белый матовый RAL 9010. Санкт-Петербург."),
    ("#2 Two positions", "1000 400 2 шт МДФ RAL 9010 матовый\n600 300 1 шт МДФ RAL 8017 глянцевый\nМосква."),
    ("#3 Three positions", "1000 400 4 шт МДФ RAL 9010 матовый\n600 300 2 шт МДФ RAL 8017 глянцевый\n800 500 1 шт МДФ RAL 7016 матовый\nСПб."),
    ("#4 Discount", "1000 400 МДФ белый. Скидка будет если 10 штук?"),
    ("#5 Tech advice", "Фрезеровка + покраска фасадов МДФ 800 500 4 шт"),
    ("#6 No sizes", "Сколько стоит покрасить фасады?"),
    ("#7 Ambiguous wood", "600 400 5 шт дерево белый"),
    ("#8 Paint only", "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый"),
    ("#9 Old facades", "Старые фасады перекрасить. Дерево. 600 400 5 шт в белый"),
    ("#10 Incomplete", "Покрасить надо"),
]

blocked_sales = 0
blocked_malyarka = 0
blocked_corel = 0
reached_corel = 0
total = len(MESSAGES)

print("=" * 70)
print("  Full-Chain: Sales → Malyarka → Corel Export")
print("=" * 70)

for name, msg in MESSAGES:
    print(f"\n{'─' * 70}\n  {name}\n  Message: {msg[:80]}")

    # Stage 1: Sales
    card = build_intake_card(msg)
    handoff = determine_handoff_status(card)
    print(f"  Sales: status={card['status']}, ready={handoff['ready_for_malyarka_agent']}")

    if not handoff["ready_for_malyarka_agent"]:
        blocked_sales += 1
        print(f"  ❌ BLOCKED at Sales — {handoff.get('reason', 'blocking flags')[:60]}")
        continue

    # Stage 2: Malyarka
    malyarka_result = build_preliminary_result(card)
    print(f"  Malyarka: status={malyarka_result['status']}, area={malyarka_result['total_area_m2']} m², blocked={malyarka_result['export_blocked']}")

    if malyarka_result["status"] != "ready_for_human_review" or malyarka_result["export_blocked"]:
        blocked_malyarka += 1
        print(f"  ❌ BLOCKED at Malyarka — {malyarka_result.get('status', 'blocked')}")
        continue

    # Stage 3: Corel Export
    corel_contract = build_export_contract(malyarka_result)
    reached_corel += 1
    print(f"  Corel: ready={corel_contract['ready_for_corel']}, rows={len(corel_contract['corel_rows'])}")

    if not corel_contract["ready_for_corel"]:
        blocked_corel += 1
        print(f"  ❌ BLOCKED at Corel — {corel_contract['export_blockers']}")
    else:
        print(f"  ✅ FULL CHAIN PASSED")
        for row in corel_contract["corel_rows"]:
            print(f"     {row['height_mm']}×{row['width_mm']} mm, ×{row['quantity']}, {row['material']}, {row['color']}")

print(f"\n{'=' * 70}")
print(f"  TOTAL: {total} messages")
print(f"  Blocked at Sales:   {blocked_sales}")
print(f"  Blocked at Malyarka: {blocked_malyarka}")
print(f"  Blocked at Corel:   {blocked_corel}")
print(f"  Reached Corel:      {reached_corel}")
print(f"{'=' * 70}")
