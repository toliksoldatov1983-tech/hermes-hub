"""Message formatting for the safe Telegram skeleton."""


def format_order_reply(order_result: dict) -> str:
    """Format an existing Malyarka Clean order result for Telegram."""
    status = order_result["status"]
    lines = [
        "Malyarka Clean",
        f"Статус: {status}",
        f"Площадь: {_format_area(order_result['total_area_m2'])} m2",
        f"Export blocked: {_format_bool(order_result['export_blocked'])}",
        "",
        "Подтверждённые строки:",
        *_format_confirmed_rows(order_result["confirmed_rows"]),
        "",
        "Спорные строки:",
        *_format_disputed_rows(order_result["disputed_rows"]),
        "",
        _next_action_text(status),
    ]
    return "\n".join(lines).strip()


def _format_confirmed_rows(rows):
    if not rows:
        return ["нет"]

    formatted = []
    for row in rows:
        formatted.append(
            "- строка {source_line}: {height} x {width}, количество {quantity}".format(
                source_line=row["source_line"],
                height=row["height"],
                width=row["width"],
                quantity=row["quantity"],
            )
        )
    return formatted


def _format_disputed_rows(rows):
    if not rows:
        return ["нет"]

    formatted = []
    for row in rows:
        formatted.append(
            "- строка {source_line}: {raw_text} ({reason}). {question}".format(
                source_line=row["source_line"],
                raw_text=row["raw_text"],
                reason=row["reason"],
                question=row["suggested_question"],
            )
        )
    return formatted


def _next_action_text(status):
    if status == "clean":
        return "Заказ чистый. Excel можно создать локальным запускателем."
    if status == "has_disputes":
        return "Excel заблокирован. Исправь только спорные строки и отправь заказ снова."
    return (
        "Заказ пустой или непонятный. Отправь строки с размерами, "
        "например: 1000 400 2."
    )


def _format_area(value):
    return f"{value:.6g}"


def _format_bool(value):
    return "да" if value else "нет"

