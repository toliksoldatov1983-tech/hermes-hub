"""Simple local user order input for Malyarka Clean."""

from pathlib import Path
import argparse
from datetime import datetime
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HERMES_ROOT = PROJECT_ROOT.parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
OUTPUT_PATH = HERMES_ROOT / "outputs" / "LAST_ORDER_RESULT.txt"
DEFAULT_INPUT_PATH = HERMES_ROOT / "inputs" / "ORDER_INPUT.txt"
sys.path.insert(0, str(SRC_ROOT))

from malyarka_clean_core import build_corel_export_model, build_order_result  # noqa: E402


SAMPLES = {
    "clean": "1000 400 2\n700 300",
    "dispute": "1000 400 2\nмусор\n700 300",
    "garbage": "привет\nничего непонятно",
}


def main():
    parser = argparse.ArgumentParser(description="Local Malyarka Clean order input")
    parser.add_argument("--sample", choices=sorted(SAMPLES), help="Run a built-in sample order.")
    parser.add_argument("--input-file", type=Path, help="Read order text from a plain .txt file.")
    args = parser.parse_args()

    if args.input_file:
        raw_text = _read_order_file(args.input_file)
    elif args.sample:
        raw_text = SAMPLES[args.sample]
    else:
        raw_text = _read_user_order()

    _print_result(raw_text)


def _read_user_order():
    print("Вставьте текст заказа.")
    print("Когда закончите, напишите на новой строке: ГОТОВО")
    print()

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() == "ГОТОВО":
            break
        lines.append(line)

    return "\n".join(lines)


def _read_order_file(path):
    input_path = path if path.is_absolute() else DEFAULT_INPUT_PATH.parent / path
    if not input_path.exists():
        raise SystemExit(f"Файл заказа не найден: {input_path}")

    return input_path.read_text(encoding="utf-8")


def _print_result(raw_text):
    order_result = build_order_result(raw_text, source="user_order_input")
    corel_model = build_corel_export_model(order_result)
    result_text = _format_result(raw_text, order_result, corel_model)

    print()
    print(result_text)
    _save_result(result_text)
    print()
    print(f"Результат сохранён в файл: {OUTPUT_PATH}")


def _format_result(raw_text, order_result, corel_model):
    checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = order_result["status"]
    total_area = order_result["total_area_m2"]
    export_blocked = order_result["export_blocked"]
    confirmed_rows = order_result["confirmed_rows"]
    disputed_rows = order_result["disputed_rows"]
    corel_rows = corel_model["corel_rows"]
    reason = corel_model["reason"]

    lines = [
        "MALYARKA CLEAN - РЕЗУЛЬТАТ ПРОВЕРКИ ЗАКАЗА",
        "=" * 64,
        "",
        f"Дата и время проверки: {checked_at}",
        "Важно: это локальная проверка. Это не Telegram, не Vision, не API, не база и не Excel/Corel export.",
        "",
        "КОРОТКИЙ ИТОГ",
        "-" * 64,
        f"Статус: {_status_label(status)} ({status})",
        f"Площадь подтверждённых строк: {total_area} м2",
        f"Будущий экспорт заблокирован: {_yes_no(export_blocked)}",
        f"Причина: {_reason_label(reason)}",
        "",
        "ИСХОДНЫЙ ЗАКАЗ",
        "-" * 64,
        _display_text(raw_text) if raw_text.strip() else "(пусто)",
        "",
        f"ПОДТВЕРЖДЁННЫЕ СТРОКИ ({len(confirmed_rows)})",
        "-" * 64,
        *_format_confirmed_rows(confirmed_rows),
        "",
        f"СПОРНЫЕ СТРОКИ ({len(disputed_rows)})",
        "-" * 64,
        *_format_disputed_rows(disputed_rows),
        "",
        f"COREL-СТРОКИ ({len(corel_rows)})",
        "-" * 64,
        *_format_corel_rows(corel_rows, export_blocked),
        "",
        "ЧТО ДЕЛАТЬ ДАЛЬШЕ",
        "-" * 64,
        *_next_steps(status, export_blocked, disputed_rows),
    ]

    return "\n".join(lines)


def _format_confirmed_rows(rows):
    if not rows:
        return ["- нет"]

    result = []
    for row in rows:
        line_no = row.get("source_line", "?")
        height = row.get("height", "?")
        width = row.get("width", "?")
        quantity = row.get("quantity", "?")
        raw = row.get("raw_text", "")
        result.append(f"- Строка {line_no}: {height} x {width}, количество {quantity}. Исходно: {_display_text(raw)}")
    return result


def _format_disputed_rows(rows):
    if not rows:
        return ["- нет"]

    result = []
    for row in rows:
        line_no = row.get("source_line", "?")
        raw = row.get("raw_text", "")
        reason = row.get("reason", "unknown")
        question = row.get("suggested_question", "Нужно уточнение.")
        result.append(f"- Строка {line_no}: {_display_text(raw)}")
        result.append(f"  Причина: {_reason_label(reason)} ({reason})")
        result.append(f"  Что уточнить: {question}")
    return result


def _format_corel_rows(rows, export_blocked):
    if export_blocked:
        return ["- заблокировано: сначала нужно разобраться со спорными или пустыми данными"]
    if not rows:
        return ["- нет"]

    result = []
    for index, row in enumerate(rows, start=1):
        height = row.get("height_mm", "?")
        width = row.get("width_mm", "?")
        quantity = row.get("quantity", "?")
        result.append(f"- Corel {index}: высота {height} мм, ширина {width} мм, количество {quantity}")
    return result


def _next_steps(status, export_blocked, disputed_rows):
    if status == "clean" and not export_blocked:
        return [
            "- Заказ выглядит чистым.",
            "- Можно использовать подтверждённые строки и Corel-строки для следующего безопасного этапа.",
            "- Это всё ещё не производственный экспорт.",
        ]

    if disputed_rows:
        return [
            "- Проверь спорные строки выше.",
            "- Уточни непонятные места в заказе.",
            "- После исправления снова запусти проверку.",
        ]

    return [
        "- Заказ пустой или непонятный.",
        "- Вставь строки с размерами и снова запусти проверку.",
    ]


def _status_label(status):
    labels = {
        "clean": "чистый заказ",
        "has_disputes": "есть спорные строки",
        "empty_or_invalid": "пустой или непонятный заказ",
    }
    return labels.get(status, "неизвестный статус")


def _reason_label(reason):
    labels = {
        "ready": "готово",
        "disputed_rows_present": "есть спорные строки",
        "empty_or_invalid": "пустой или непонятный заказ",
        "unparsed_order_text": "текст нельзя безопасно разобрать",
    }
    return labels.get(reason, reason)


def _yes_no(value):
    return "да" if value else "нет"


def _display_text(text):
    return text.replace("\ufeff", "").replace("×", "x")


def _save_result(result_text):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(result_text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
