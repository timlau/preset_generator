from collections import namedtuple

from generator.preset.types import InputValue


def dict_to_namedtuple(values: dict) -> namedtuple:
    names = [key for key in values.keys()]
    named_tuple = namedtuple("Values", names)
    return named_tuple(**values)


def get_input_values(values: list[InputValue]):
    names = [value.name for value in values]
    Values = namedtuple("Values", names)
    values = [value.value for value in values]
    return Values(*values)


def get_dict_values(values: list[InputValue]):
    value_dict = {value.name: value.value for value in values}
    return value_dict


def to_percent(value: int, max_value: int):
    percent: float = (float(value) / max_value) * 100
    return f"{percent:.4f}%"
