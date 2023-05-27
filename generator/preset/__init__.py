import json

from pathlib import Path

from generator.preset import factory, loader
from generator.preset.types import PresetGenerator
from generator import DATA_DIR
from generator.preset.utils import dict_to_namedtuple


def load_presets() -> list[PresetGenerator]:
    # read data from a JSON file
    file_name = DATA_DIR / Path("other/presets.json")
    with file_name.open("r") as file:
        data = json.load(file)

        # load the plugins
        loader.load_plugins(data["plugins"])

        # create the generators
        presets = [factory.create(item) for item in data["generators"]]

        settings = dict_to_namedtuple(data["settings"])
        # run setup on generators
        for preset in presets:
            preset.setup(settings)

    return presets, settings
