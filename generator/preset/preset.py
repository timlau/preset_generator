""" Implement a basic preset generator"""

from typing import Protocol
from generator.preset import InputValue


class PresetGenerator(Protocol):
    def generator(self) -> None:
        ...

    def inputs(self) -> list[InputValue]:
        ...

    def set_values(self, values: list[InputValue]) -> None:
        ...
