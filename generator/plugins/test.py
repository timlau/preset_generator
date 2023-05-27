""" test preset generator """
from dataclasses import dataclass
from generator.preset import factory, get_input_values
from generator.preset.factory import InputValue


@dataclass
class Test:
    name: str
    desc: str = "Test Plugin"
    values: list[InputValue] = None

    def generate(self) -> None:
        print(f"this is the {self.name} preset generator")
        values = get_input_values(self.values)
        print(values)

    def inputs(self) -> list[InputValue]:
        if not self.values:
            self.values = [
                InputValue("value1", "Value1", int),
                InputValue("value2", "Value2", str),
                InputValue("value3", "Value3", float),
            ]
        return self.values

    @property
    def description(self) -> str:
        return "This is a test plugin"


def register() -> None:
    factory.register("test", Test)
