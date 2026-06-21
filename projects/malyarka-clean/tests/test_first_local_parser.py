from malyarka_clean_core import (
    build_parse_result,
    parse_size_lines,
    prepare_order_input,
)


def parse_order(text):
    input_data = prepare_order_input(text)
    parsed_data = parse_size_lines(input_data["original_lines"])
    return build_parse_result(input_data, parsed_data)


def test_plain_height_width_defaults_quantity_to_one():
    result = parse_order("1000 400")

    assert result["status"] == "clean"
    assert result["confirmed_rows"][0]["height"] == 1000
    assert result["confirmed_rows"][0]["width"] == 400
    assert result["confirmed_rows"][0]["quantity"] == 1
    assert result["disputed_rows"] == []


def test_plain_height_width_quantity():
    result = parse_order("1000 400 2")

    assert result["status"] == "clean"
    assert result["confirmed_rows"][0]["height"] == 1000
    assert result["confirmed_rows"][0]["width"] == 400
    assert result["confirmed_rows"][0]["quantity"] == 2


def test_separator_formats_default_quantity_to_one():
    for text in ["1000x400", "1000 x 400", "1000*400", "1000×400"]:
        result = parse_order(text)

        assert result["status"] == "clean"
        assert result["confirmed_rows"][0]["height"] == 1000
        assert result["confirmed_rows"][0]["width"] == 400
        assert result["confirmed_rows"][0]["quantity"] == 1


def test_missing_width_is_disputed():
    result = parse_order("1000")

    assert result["status"] == "has_disputes"
    assert result["confirmed_rows"] == []
    assert result["disputed_rows"][0]["reason"] == "missing_width"


def test_too_many_numbers_is_disputed():
    result = parse_order("1000 400 2 5")

    assert result["status"] == "has_disputes"
    assert result["confirmed_rows"] == []
    assert result["disputed_rows"][0]["reason"] == "too_many_numbers"


def test_meaningful_text_is_disputed():
    result = parse_order("срочно 1000 400")

    assert result["status"] == "has_disputes"
    assert result["confirmed_rows"] == []
    assert result["disputed_rows"][0]["reason"] == "unparsed_order_text"


def test_empty_text_is_empty_or_invalid():
    result = parse_order("")

    assert result["status"] == "empty_or_invalid"
    assert result["confirmed_rows"] == []
    assert result["disputed_rows"] == []
