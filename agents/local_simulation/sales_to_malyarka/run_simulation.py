#!/usr/bin/env python3
"""
Sales → Malyarka Local Integration Simulation.

Runs: Fake Message → Sales Agent → Intake Card → Handoff Check → Malyarka Agent → Preliminary Result
No Telegram. No API. No server. No live. No real orders.
"""

import sys, os

# Add src paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "sales_client_intake_agent", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "malyarka_agent", "src"))

from intake_agent import build_intake_card, determine_handoff_status
from malyarka_agent import build_preliminary_result

FAKE_MESSAGES = [
    ("#1 All clear", "1000 400 4 шт МДФ белый матовый RAL 9010. Санкт-Петербург."),
    ("#2 Two positions", "1000 400 2 шт МДФ RAL 9010 матовый\n600 300 1 шт МДФ RAL 8017 глянцевый\nМосква."),
    ("#3 Ambiguous wood", "600 400 5 шт дерево белый"),
    ("#4 Discount", "1000 400 МДФ белый. Скидка будет если 10 штук?"),
    ("#5 Technical advice", "Фрезеровка + покраска фасадов МДФ 800 500 4 шт"),
    ("#6 No sizes", "Сколько стоит покрасить фасады?"),
    ("#7 Incomplete", "Покрасить надо"),
    ("#8 Paint only", "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый"),
    ("#9 Old facades", "Старые фасады перекрасить. Дерево. 600 400 5 шт в белый"),
    ("#10 Three positions", "1000 400 4 шт МДФ RAL 9010 матовый\n600 300 2 шт МДФ RAL 8017 глянцевый\n800 500 1 шт МДФ RAL 7016 матовый\nСПб."),
]

print("=" * 70)
print("  Sales → Malyarka Local Integration Simulation")
print("=" * 70)

passed_to_malyarka = 0
blocked_by_sales = 0
total = len(FAKE_MESSAGES)

for name, msg in FAKE_MESSAGES:
    print(f"\n{'─' * 70}")
    print(f"  {name}")
    print(f"  Message: {msg[:80]}")

    # Step 1: Sales Agent
    card = build_intake_card(msg)
    handoff = determine_handoff_status(card)

    print(f"  Sales status: {card['status']}")
    print(f"  Handoff ready: {handoff['ready_for_malyarka_agent']}")
    print(f"  Blocked: {handoff['needs_manager_review'] or handoff['needs_clarification']}")

    # Step 2: Check if should pass to Malyarka
    if not handoff['ready_for_malyarka_agent']:
        blocked_by_sales += 1
        print(f"  ❌ BLOCKED by Sales — not passed to Malyarka")
        print(f"     Reason: {handoff.get('reason', 'blocking flags or incomplete data')}")
        continue

    # Step 3: Malyarka Agent
    result = build_preliminary_result(card)
    passed_to_malyarka += 1

    print(f"  ✅ Passed to Malyarka")
    print(f"  Malyarka status: {result['status']}")
    print(f"  Confirmed: {len(result['confirmed_rows'])}, Disputed: {len(result['disputed_rows'])}")
    print(f"  Area: {result['total_area_m2']} m²")
    print(f"  Export blocked: {result['export_blocked']}")
    print(f"  Not final order: {result['not_final_order']}")

print(f"\n{'=' * 70}")
print(f"  TOTAL: {total} messages")
print(f"  Passed to Malyarka: {passed_to_malyarka}")
print(f"  Blocked by Sales: {blocked_by_sales}")
print(f"{'=' * 70}")
