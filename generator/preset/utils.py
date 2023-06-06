from collections import namedtuple
from configparser import ConfigParser
from pathlib import Path

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


def get_output_path(setting_files: list[str]):
    paths = [
        Path(dst).expanduser()
        for dst in setting_files
        if Path(dst).expanduser().exists()
    ]
    paths = sorted(paths, key=lambda path: path.stat().st_mtime)
    if paths:
        config = ConfigParser()
        config.read(paths[0])
        try:
            return config["General"]["appdatadir"]
        except KeyError:
            pass
    return None
