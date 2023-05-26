""" test preset generator """
from dataclasses import dataclass
from generator.preset import factory


@dataclass
class Test:
    name: str

    def generate(self) -> None:
        print(f"this is the {self.name} preset generator")


def register() -> None:
    factory.register("test", Test)
