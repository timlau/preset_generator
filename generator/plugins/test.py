""" test preset generator """
from dataclasses import dataclass
from generator.preset import factory, InputValue


@dataclass
class Test:
    name: str
    values: list[InputValue] = None

    def generate(self) -> None:
        print(f"this is the {self.name} preset generator")

    def inputs(self) -> list[InputValue]:
        return [
            InputValue("value1", "Value1", int),
            InputValue("value2", "Value2", str),
            InputValue("value3", "Value3", float),
        ]

    def set_values(self, values: list[InputValue]) -> None:
        self.values = values


def register() -> None:
    factory.register("test", Test)
