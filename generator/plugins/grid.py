""" test preset generator """
from dataclasses import dataclass
from generator.preset import factory, get_input_values
from generator.preset.factory import InputValue


@dataclass
class Grid:
    name: str
    values: list[InputValue] = None

    def generate(self) -> None:
        print(f"this is the {self.name} preset generator")
        values = get_input_values(self.values)
        print(values)

    def inputs(self) -> list[InputValue]:
        if not self.values:
            self.values = [
                InputValue("rows", "Rows", int),
                InputValue("columns", "Columns", int),
            ]
        return self.values

    @property
    def description(self) -> str:
        return "Crop Rectangle: Grid presets"


def register() -> None:
    factory.register("grid", Grid)
