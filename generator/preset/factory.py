"""Factory for creating a preset generatro."""

from dataclasses import dataclass
from typing import Any, Callable, Protocol, Type


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


class PresetGenerator(Protocol):
    def generator(self) -> None:
        ...

    def inputs(self) -> list[InputValue]:
        ...

    @property
    def description(self) -> str:
        ...


preset_creation_funcs: dict[str, Callable[..., PresetGenerator]] = {}


def register(preset_type: str, creator_fn: Callable[..., PresetGenerator]) -> None:
    """Register a new preset generator type."""
    preset_creation_funcs[preset_type] = creator_fn


def unregister(preset_type: str) -> None:
    """Unregister a preset generator type."""
    preset_creation_funcs.pop(preset_type, None)


def create(arguments: dict[str, Any]) -> PresetGenerator:
    """Create a preset generator of a specific type, given JSON data."""
    args_copy = arguments.copy()
    preset_type = args_copy.pop("type")
    try:
        creator_func = preset_creation_funcs[preset_type]
    except KeyError:
        raise ValueError(f"unknown character type {preset_type!r}") from None
    return creator_func(**args_copy)
