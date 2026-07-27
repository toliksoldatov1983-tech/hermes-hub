from hermes_modules.malyarka.dispute_questions import question_for_row, questions_for_order
from hermes_modules.malyarka.parser_contract import ParserContract


def test_format_error_gets_rewrite_question():
    order = ParserContract().parse("paint 2 bucket")

    question = question_for_row(order.disputed_rows[0])

    assert question.category == "FORMAT_ERROR"
    assert "item | quantity | unit" in question.question
    assert question.blocks_final is True


def test_quantity_error_gets_numeric_question():
    order = ParserContract().parse("paint | many | bucket")

    question = question_for_row(order.disputed_rows[0])

    assert question.category == "INVALID_QUANTITY"
    assert "positive numeric quantity" in question.question


def test_missing_item_gets_item_question():
    order = ParserContract().parse(" | 1 | bucket")

    question = question_for_row(order.disputed_rows[0])

    assert question.category == "MISSING_ITEM"
    assert "item name" in question.question


def test_missing_unit_gets_unit_question():
    order = ParserContract().parse("paint | 1 | ")

    question = question_for_row(order.disputed_rows[0])

    assert question.category == "MISSING_UNIT"
    assert "unit" in question.question


def test_questions_for_order_preserves_row_numbers():
    order = ParserContract().parse("paint | 2 | bucket\nbroken row")

    questions = questions_for_order(order)

    assert len(questions) == 1
    assert questions[0].row_number == 2
