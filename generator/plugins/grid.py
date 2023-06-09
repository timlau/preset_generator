""" test preset generator """
from collections import namedtuple
from pathlib import Path
import urllib

from dataclasses import dataclass
from string import Template
from generator.preset import factory
from generator.preset.utils import get_dict_values, to_percent
from generator.preset.types import InputValue
from generator.plugins import GridCalculator, PresetType

PRESETS = {
    PresetType.CROP_RECTANGLE: """---
rect: $x $y $width $height 1
radius: 0
color: "#00000000"
..."""
}


@dataclass
class GridPreset:
    name: str
    values: list[InputValue] = None
    output: str = "./shotcut"
    grid_calc: GridCalculator = None
    active_type: PresetType = PresetType.CROP_RECTANGLE

    def setup(self, settings: namedtuple) -> None:
        self.output = settings.output

    def generate(self) -> None:
        values = get_dict_values(self.values)
        self.grid_calc = GridCalculator(**values)
        self.generate_preset()

    def inputs(self) -> list[InputValue]:
        if not self.values:
            self.values = [
                InputValue("rows", "Rows", int, 3),
                InputValue("columns", "Columns", int, 3),
            ]
        return self.values

    def types(self) -> list(PresetType):
        return [PresetType.CROP_RECTANGLE]

    @property
    def description(self) -> str:
        return "Grid Presets"

    def make_crop_preset(self, row, col, num_col, num_row):
        x, y, w, h = self.grid_calc.calc_block(row, col, num_row, num_col)
        grid = self.grid_calc
        name = f"Grid_{grid.columns}x{grid.rows}_({row+1},{col+1}.{num_row}x{num_col})"  # noqa
        template = Template(PRESETS[self.active_type])
        tpl = template.substitute(
            x=to_percent(x, 3840),
            y=to_percent(y, 2160),
            height=to_percent(h, 2160),
            width=to_percent(w, 3840),
        )
        self.write_preset(name, tpl)

    def write_preset(self, name: str, preset: str):
        qf_name = urllib.parse.quote_plus(name)
        directory = (
            Path(self.output).expanduser() / Path("presets") / Path(self.active_type)
        )
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        path = directory / Path(qf_name)
        print(f"create preset {name} : {path.resolve().name}")
        with open(path.resolve(), "w") as out_file:
            out_file.write(preset)

    def generate_preset(self):
        grid = self.grid_calc
        for row in range(grid.rows):
            for col in range(grid.columns):
                for row_ndx in range(grid.rows - row):
                    for col_ndx in range(grid.columns - col):
                        num_col = col_ndx + 1
                        num_row = row_ndx + 1
                        self.make_crop_preset(row, col, num_col, num_row)


def register() -> None:
    factory.register("grid", GridPreset)
