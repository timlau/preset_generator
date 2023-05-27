import json
from pathlib import Path

from generator.preset import InputValue, factory, loader
from generator import DATA_DIR


def main() -> None:
    """Create game characters from a file containg a level definition."""

    # read data from a JSON file
    file_name = DATA_DIR / Path("other/presets.json")
    with file_name.open("r") as file:
        data = json.load(file)

        # load the plugins
        loader.load_plugins(data["plugins"])

        # create the generators
        presets = [factory.create(item) for item in data["generators"]]

        # do something with the generators
        for preset in presets:
            preset.generate()
            needed_values: list[InputValue] = preset.inputs()
            needs = ",".join([value.label for value in needed_values])
            print(f" --> {preset.name} needs: {needs}")
            for value in needed_values:
                value.value_from_string("10")
            print(needed_values)


if __name__ == "__main__":
    main()
