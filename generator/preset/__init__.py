from dataclasses import dataclass
from typing import Any, Type


@dataclass
class InputValue:
    name: str
    label: str
    type: Type
    value: Any = None

    def value_from_string(self, value: str):
        if self.type is str:
            self.value = value
        elif self.type is int:
            self.value = int(value)
        elif self.type is float:
            self.value = float(value)
