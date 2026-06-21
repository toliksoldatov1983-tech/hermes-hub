#!/usr/bin/env python3
"""
Sales + Client Intake Agent — Offline Demo Runner.

Run: python agents/sales_client_intake_agent/demo/run_demo.py

No Telegram. No API. No network. No live clients.
Pure offline demo with golden case verification.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from intake_agent import (  # type: ignore[import-untyped]
    analyze_client_message,
    build_intake_card,
    suggest_questions,
    suggest_response,
    determine_handoff_status,
)

# ---------------------------------------------------------------------------
# 15 demo scenarios from TEST_SCENARIOS.md
# ---------------------------------------------------------------------------

DEMO_SCENARIOS = [
    {
        "id": 1,
        "name": "Цена без размеров",
        "input": "Сколько стоит покрасить фасады?",
        "expected": {
            "has_sizes": False,
            "has_material": False,
            "has_color": False,
            "flags.discount_request": True,
            "status": "needs_more_info",
            "ready_for_malyarka": False,
            "needs_manager": True,  # discount → manager
        },
    },
    {
        "id": 2,
        "name": "Размеры без материала",
        "input": "1000 400 2 шт\n600 300 1 шт",
        "expected": {
            "has_sizes": True,
            "has_material": False,
            "status": "needs_more_info",
            "ready_for_malyarka": False,
            "needs_manager": False,
            "items_count": 2,
        },
    },
    {
        "id": 3,
        "name": "Фасады белые",
        "input": "Нужны фасады белые",
        "expected": {
            "has_sizes": False,
            "has_color": True,
            "status": "needs_more_info",
            "ready_for_malyarka": False,
        },
    },
    {
        "id": 4,
        "name": "Фрезеровка без типа",
        "input": "Фрезеровка + покраска фасадов МДФ 800 500 4 шт",
        "expected": {
            "has_sizes": True,
            "has_material": True,
            "flags.technical_advice_requested": True,
            "flags.manager_review_required": True,
            "ready_for_malyarka": False,
            "needs_manager": True,
        },
    },
    {
        "id": 5,
        "name": "Скидка",
        "input": "1000 400 МДФ белый. Скидка будет если 10 штук?",
        "expected": {
            "has_sizes": True,
            "flags.discount_request": True,
            "status": "ready_for_review",
            "ready_for_malyarka": False,  # discount blocks handoff
            "needs_manager": True,  # discount → manager
        },
    },
    {
        "id": 6,
        "name": "Какой материал лучше?",
        "input": "Что лучше для кухни — МДФ или массив?",
        "expected": {
            "flags.technical_advice_requested": True,
            "flags.manager_review_required": True,
            "ready_for_malyarka": False,
            "needs_manager": True,
        },
    },
    {
        "id": 7,
        "name": "Сроки",
        "input": "За сколько сделаете?",
        "expected": {
            "flags.manager_review_required": True,
            "ready_for_malyarka": False,
            "needs_manager": True,
        },
    },
    {
        "id": 8,
        "name": "Неполное описание",
        "input": "Покрасить надо",
        "expected": {
            "has_sizes": False,
            "status": "needs_more_info",
            "ready_for_malyarka": False,
        },
    },
    {
        "id": 9,
        "name": "Только покраска",
        "input": "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый",
        "expected": {
            "has_sizes": True,
            "has_material": True,
            "has_color": True,
            "status": "ready_for_review",
            "ready_for_malyarka": True,
            "needs_manager": False,
        },
    },
    {
        "id": 10,
        "name": "Переделка старых фасадов",
        "input": "Старые фасады перекрасить. Дерево. 600 400 5 шт в белый",
        "expected": {
            "has_sizes": True,
            "has_material": True,
            "has_color": True,
            "status": "ready_for_review",
            "ready_for_malyarka": True,
        },
    },
    {
        "id": 11,
        "name": "Фасады под ключ",
        "input": "Нужны фасады под ключ. Кухня 5 фасадов. Размеры уточню.",
        "expected": {
            "has_sizes": False,
            "status": "needs_more_info",
            "ready_for_malyarka": False,
        },
    },
    {
        "id": 12,
        "name": "Цвет без RAL",
        "input": "1000 400 3 шт МДФ цвет кофе с молоком",
        "expected": {
            "has_sizes": True,
            "has_material": True,
            "has_color": True,
            "status": "ready_for_review",
            "ready_for_malyarka": True,
        },
    },
    {
        "id": 13,
        "name": "Примерно 20 штук",
        "input": "Фасады МДФ белые примерно 20 штук, размеры разные",
        "expected": {
            "has_material": True,
            "has_color": True,
            "has_sizes": False,
            "status": "needs_more_info",
            "ready_for_malyarka": False,
        },
    },
    {
        "id": 14,
        "name": "Посчитайте кухню",
        "input": "Посчитайте мне кухню",
        "expected": {
            "has_sizes": False,
            "status": "needs_more_info",
            "ready_for_malyarka": False,
        },
    },
    {
        "id": 15,
        "name": "Все данные есть",
        "input": (
            "1000 400 4 шт МДФ белый матовый RAL 9010\n"
            "600 300 2 шт дерево коричневый глянцевый\n"
            "Нужна грунтовка для МДФ. Поверхность готова.\n"
            "Санкт-Петербург."
        ),
        "expected": {
            "has_sizes": True,
            "has_material": True,
            "has_color": True,
            "status": "ready_for_review",
            "ready_for_malyarka": True,
            "needs_manager": False,
            "items_count": 2,
            "city": "Санкт-Петербург",
        },
    },
]


def get_nested(d, path):
    """Get nested dict value by dot-separated path."""
    keys = path.split(".")
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return None
    return d


def run_scenario(scenario):
    """Run one scenario and return results."""
    text = scenario["input"]
    expected = scenario["expected"]

    analysis = analyze_client_message(text)
    card = build_intake_card(text)
    response = suggest_response(card)
    questions = suggest_questions(card)
    handoff = determine_handoff_status(card)

    checks = {}
    for key, expected_val in expected.items():
        if key.startswith("flags."):
            actual = get_nested(analysis, key) or get_nested(card, key)
        elif key == "status":
            actual = card.get("status")
        elif key == "ready_for_malyarka":
            actual = handoff.get("ready_for_malyarka_agent")
        elif key == "needs_manager":
            actual = handoff.get("needs_manager_review")
        elif key == "items_count":
            actual = len(card.get("items", []))
        elif key == "city":
            actual = card.get("client", {}).get("city")
        else:
            actual = analysis.get(key)
        checks[key] = {"expected": expected_val, "actual": actual, "ok": actual == expected_val}

    return {
        "id": scenario["id"],
        "name": scenario["name"],
        "input": text,
        "analysis": {
            "has_sizes": analysis["has_sizes"],
            "has_material": analysis["has_material"],
            "has_color": analysis["has_color"],
            "items": analysis["items"],
            "flags": analysis["flags"],
            "missing_fields": analysis["missing_fields"],
        },
        "card_status": card["status"],
        "handoff": handoff,
        "response": response,
        "questions": questions,
        "checks": checks,
    }


def main():
    """Run all demo scenarios and print results."""
    print("=" * 60)
    print("  Sales + Client Intake Agent — Offline Demo")
    print("  No Telegram. No API. No live clients.")
    print("=" * 60)

    passed = 0
    failed = 0

    for scenario in DEMO_SCENARIOS:
        result = run_scenario(scenario)

        all_ok = all(c["ok"] for c in result["checks"].values())
        if all_ok:
            passed += 1
            status = "✅ PASS"
        else:
            failed += 1
            status = "❌ FAIL"

        print(f"\n{'─' * 60}")
        print(f"  #{result['id']:02d} {result['name']} {status}")
        print(f"  Input: {result['input'][:80]}")
        print(f"  Status: {result['card_status']}")
        print(f"  Handoff: ready={result['handoff']['ready_for_malyarka_agent']}, "
              f"manager={result['handoff']['needs_manager_review']}")
        print(f"  Response: {result['response'][:100]}")

        if not all_ok:
            for key, check in result["checks"].items():
                if not check["ok"]:
                    print(f"  ❌ {key}: expected={check['expected']}, actual={check['actual']}")

    print(f"\n{'=' * 60}")
    print(f"  TOTAL: {passed} passed, {failed} failed out of {len(DEMO_SCENARIOS)}")
    print(f"{'=' * 60}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
