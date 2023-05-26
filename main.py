import json

from generator.preset import factory, loader


def main() -> None:
    """Create game characters from a file containg a level definition."""

    # read data from a JSON file
    with open("presets.json") as file:
        data = json.load(file)

        # load the plugins
        loader.load_plugins(data["plugins"])

        # create the characters
        presets = [factory.create(item) for item in data["generators"]]

        # do something with the characters
        for preset in presets:
            preset.generate()


if __name__ == "__main__":
    main()
