""" test preset generator """
from dataclasses import dataclass
from generator.preset import factory, InputValue


@dataclass
class Grid:
    name: str
    values: list[InputValue] = None

    def generate(self) -> None:
        print(f"this is the {self.name} preset generator")

    def inputs(self) -> list[InputValue]:
        return [
            InputValue("rows", "Rows", int),
            InputValue("columns", "Columns", int),
        ]

    def set_values(self, values: list[InputValue]) -> None:
        self.values = values


def register() -> None:
    factory.register("grid", Grid)
