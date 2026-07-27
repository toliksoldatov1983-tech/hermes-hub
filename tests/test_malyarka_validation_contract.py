from hermes_modules.malyarka.parser_contract import ParserContract
from hermes_modules.malyarka.validation_contract import validate_order


def test_valid_order_passes_validation():
    order = ParserContract().parse("paint | 2 | bucket")

    result = validate_order(order)

    assert result.valid is True
    assert result.blocked is False
    assert result.confirmed_count == 1
    assert result.disputed_count == 0
    assert result.issues == []


def test_malformed_row_blocks_validation():
    order = ParserContract().parse("paint 2 bucket")

    result = validate_order(order)

    assert result.valid is False
    assert result.blocked is True
    assert result.issues[0].code == "malformed_row"


def test_missing_item_blocks_validation():
    order = ParserContract().parse(" | 2 | bucket")

    result = validate_order(order)

    assert result.valid is False
    assert result.issues[0].code == "missing_item"


def test_missing_unit_blocks_validation():
    order = ParserContract().parse("paint | 2 | ")

    result = validate_order(order)

    assert result.valid is False
    assert result.issues[0].code == "missing_unit"


def test_bad_quantity_blocks_validation():
    order = ParserContract().parse("paint | many | bucket")

    result = validate_order(order)

    assert result.valid is False
    assert result.issues[0].code == "invalid_quantity"


def test_zero_quantity_blocks_validation():
    order = ParserContract().parse("paint | 0 | bucket")

    result = validate_order(order)

    assert result.valid is False
    assert result.issues[0].code == "invalid_quantity"


def test_mixed_order_blocks_final_validation():
    order = ParserContract().parse("paint | 2 | bucket\nbroken row")

    result = validate_order(order)

    assert result.valid is False
    assert result.confirmed_count == 1
    assert result.disputed_count == 1
    assert result.issues[0].blocks_final is True
