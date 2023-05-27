from collections import namedtuple
import json

from pathlib import Path

from generator.preset import factory, loader
from generator.preset.factory import PresetGenerator, InputValue
from generator import DATA_DIR


def get_input_values(values: list[InputValue]):
    names = [value.name for value in values]
    Values = namedtuple("Values", names)
    values = [value.value for value in values]
    return Values(*values)


def load_presets() -> list[PresetGenerator]:
    # read data from a JSON file
    file_name = DATA_DIR / Path("other/presets.json")
    with file_name.open("r") as file:
        data = json.load(file)

        # load the plugins
        loader.load_plugins(data["plugins"])

        # create the generators
        presets = [factory.create(item) for item in data["generators"]]

    return presets
