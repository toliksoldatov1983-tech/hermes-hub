from __future__ import annotations

from dataclasses import dataclass

from hermes_modules.malyarka.dispute_classifier import classify_disputed_row
from hermes_modules.malyarka.order_contract import MalyarkaOrder, MalyarkaOrderRow


QUESTION_BY_CATEGORY = {
    "FORMAT_ERROR": "Rewrite this row as: item | quantity | unit.",
    "MISSING_ITEM": "What item name should be used for this row?",
    "INVALID_QUANTITY": "What positive numeric quantity should be used for this row?",
    "MISSING_UNIT": "What unit should be used for this row?",
    "UNKNOWN_DISPUTE": "Please inspect this row manually before any export.",
}


@dataclass(frozen=True)
class DisputeQuestion:
    row_number: int
    raw_text: str
    category: str
    question: str
    blocks_final: bool = True


def question_for_row(row: MalyarkaOrderRow, *, row_number: int = 1) -> DisputeQuestion:
    classification = classify_disputed_row(row)
    return DisputeQuestion(
        row_number=row_number,
        raw_text=row.raw_text,
        category=classification.category,
        question=QUESTION_BY_CATEGORY.get(classification.category, QUESTION_BY_CATEGORY["UNKNOWN_DISPUTE"]),
        blocks_final=classification.blocks_final,
    )


def questions_for_order(order: MalyarkaOrder) -> list[DisputeQuestion]:
    questions: list[DisputeQuestion] = []
    for index, row in enumerate(order.rows, start=1):
        if row in order.disputed_rows:
            questions.append(question_for_row(row, row_number=index))
    return questions
