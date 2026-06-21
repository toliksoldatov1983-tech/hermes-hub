"""Manual Russian check for the minimal Malyarka Clean core."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from malyarka_clean_core import build_corel_export_model, build_order_result  # noqa: E402


EXAMPLES = [
    (
        "Чистый заказ",
        "1000 400 2\n700 300",
    ),
    (
        "Заказ со спорной строкой",
        "1000 400 2\nмусор\n700 300",
    ),
    (
        "Пустой или мусорный заказ",
        "привет\nничего непонятно",
    ),
]


def main():
    print("Ручная проверка минимального ядра Malyarka Clean")
    print("=" * 56)
    print("Это не Telegram, не Vision, не API, не база и не Excel/Corel export.")
    print()

    for index, (title, raw_text) in enumerate(EXAMPLES, start=1):
        order_result = build_order_result(raw_text, source="manual_core_check")
        corel_model = build_corel_export_model(order_result)

        print(f"Пример {index}: {title}")
        print("-" * 56)
        print("Исходный текст:")
        print(raw_text)
        print()
        print(f"status: {order_result['status']}")
        print(f"total_area_m2: {order_result['total_area_m2']}")
        print(f"export_blocked: {order_result['export_blocked']}")
        print(f"confirmed_rows: {len(order_result['confirmed_rows'])}")
        print(f"disputed_rows: {len(order_result['disputed_rows'])}")
        print(f"corel_rows: {corel_model['corel_rows']}")
        print(f"причина блокировки: {corel_model['reason']}")
        print()


if __name__ == "__main__":
    main()
