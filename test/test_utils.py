import pytest
from generator.preset.types import InputValue

from generator.preset.utils import (
    dict_to_namedtuple,
    to_percent,
    get_input_values,
    get_dict_values,
)


@pytest.fixture
def values() -> list[InputValue]:
    return [
        InputValue("size", "Size", float, 10.5),
        InputValue("x", "X", int, 10),
        InputValue("label", "Label", str, "text"),
    ]


def test_to_percent():
    assert to_percent(5, 10) == "50.0000%"
    assert to_percent(100 / 3, 100) == "33.3333%"
    assert to_percent(200 / 3, 100) == "66.6667%"


def test_dict_to_namedtuple():
    dict_in = {"key1": "value1", "key2": "value2"}
    out = dict_to_namedtuple(dict_in)
    assert out.key1 == "value1"
    assert out.key2 == "value2"


def test_get_input_values(values: list[InputValue]):
    rc = get_input_values(values)
    assert rc.size == 10.5
    assert rc.x == 10
    assert rc.label == "text"


def test_get_dict_values(values: list[InputValue]):
    rc = get_dict_values(values)
    assert rc["size"] == 10.5
    assert rc["x"] == 10
    assert rc["label"] == "text"
