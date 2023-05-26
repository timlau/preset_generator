""" Implement a basic preset generator"""

from typing import Protocol


class PresetGenerator(Protocol):
    def generator(self):
        ...
