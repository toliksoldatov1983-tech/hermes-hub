import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from malyarka_core.parsing import parse_size_line, parse_sizes_text


def test_parse_three_numbers_as_height_width_quantity():
    item, disputed_item = parse_size_line("500 700 2")

    assert disputed_item is None
    assert item is not None
    assert item.height == 500
    assert item.width == 700
    assert item.quantity == 2


def test_parse_two_numbers_defaults_quantity_to_one():
    item, disputed_item = parse_size_line("500 700")

    assert disputed_item is None
    assert item is not None
    assert item.height == 500
    assert item.width == 700
    assert item.quantity == 1


def test_parse_star_separated_sizes_defaults_quantity_to_one():
    draft = parse_sizes_text("1000*400\n1000*600")

    assert [(item.height, item.width, item.quantity) for item in draft.items] == [
        (1000, 400, 1),
        (1000, 600, 1),
    ]
    assert draft.disputed_items == []


def test_parse_x_separated_sizes():
    draft = parse_sizes_text("1000x400\n1000х500\n1000×600")

    assert [(item.height, item.width, item.quantity) for item in draft.items] == [
        (1000, 400, 1),
        (1000, 500, 1),
        (1000, 600, 1),
    ]
    assert draft.disputed_items == []


def test_parse_size_separators_with_quantity():
    draft = parse_sizes_text(
        "1000*400*2\n"
        "1000 x 400 x 3\n"
        "1000х400х4\n"
        "1000×400×5\n"
        "1000*400 6\n"
        "1000 x 400 7"
    )

    assert [(item.height, item.width, item.quantity) for item in draft.items] == [
        (1000, 400, 2),
        (1000, 400, 3),
        (1000, 400, 4),
        (1000, 400, 5),
        (1000, 400, 6),
        (1000, 400, 7),
    ]
    assert draft.disputed_items == []


def test_parse_position_number_is_not_size():
    item, disputed_item = parse_size_line("1. 500 700 2")

    assert disputed_item is None
    assert item is not None
    assert item.height == 500
    assert item.width == 700
    assert item.quantity == 2


def test_parse_zero_or_negative_values_as_disputed():
    draft = parse_sizes_text("0 700 2\n500 -700 2\n500 700 0")

    assert draft.items == []
    assert len(draft.disputed_items) == 3


def test_unclear_line_goes_to_disputed():
    item, disputed_item = parse_size_line("непонятная строка")

    assert item is None
    assert disputed_item is not None


def test_disputed_items_do_not_enter_confirmed_items():
    draft = parse_sizes_text("500 700 2\nнепонятная строка")

    assert len(draft.items) == 1
    assert len(draft.disputed_items) == 1
    assert draft.disputed_items[0].raw == "непонятная строка"
