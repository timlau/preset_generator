""" slidein preset generator """

from string import Template
import urllib

from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
from generator.plugins import GridCalculator
from generator.preset import factory
from generator.preset.utils import get_input_values, to_percent
from generator.preset.types import InputValue

PRESET = """---
rect: 0=$x_start $y_start 0 0 1;$frame_in=$x_end $y_end $width $height 1;$frame_out=$x_end $y_end $width $height 1;$frame_end=$x_start $y_start 0 0 1
radius: 0=0;$frame_in=0;$frame_out=0;$frame_end=0
color: "#00000000"
"shotcut:animIn": "00:00:01.000"
"shotcut:animOut": "00:00:01.000"
..."""  # noqa

PRESET_BORDER = """---
rect: 0|=0 0 0 0 1;$frame_in|=$x_end $y_end $width $height 1;$frame_out|=0 0 0 0 1
radius: 0
color: "#00000000"
"shotcut:animIn": "00:00:00.000"
"shotcut:animOut": "00:00:00.000"
..."""


@dataclass
class SlideInPreset:
    name: str
    width: int
    height: int
    fps: int
    duration: int
    size: int
    values: list[InputValue] = None
    output: str = "./shotcut"
    grid_calc: GridCalculator = None

    def setup(self, settings: namedtuple) -> None:
        self.output = settings.output

    def generate(self) -> None:
        print(f"this is the {self.name} preset generator")
        values: namedtuple = get_input_values(self.values)
        self.grid_calc = GridCalculator(rows=values.rows, columns=values.columns)
        self.generate_preset()

    def inputs(self) -> list[InputValue]:
        if not self.values:
            self.values = [
                InputValue("rows", "Rows", int, 3),
                InputValue("columns", "Columns", int, 3),
                InputValue("size", "Size", int, self.size),
                InputValue("duration", "Duration", int, self.duration),
                InputValue("fps", "FPS", int, self.fps),
            ]
        return self.values

    @property
    def description(self) -> str:
        return "Crop Rectangle: Slide in from corners"

    @property
    def frame_end(self):
        return (self.duration * self.fps) - 1

    @property
    def frame_in(self):
        return self.fps - 1

    @property
    def frame_out(self):
        return self.frame_end - self.fps + 1

    @property
    def filename(self):
        return f"{self.fps}fps_{self.duration}s_{self.size}x{self.size}"  # noqa

    def calc_top_left(self, border: bool = True):
        x, y, w, h = self.grid_calc.calc_block(
            0, 0, self.size, self.size, border=border
        )
        prefix = "SlideIn_TL"
        if not border:
            prefix += "_B"
            template = Template(PRESET_BORDER)
        else:
            template = Template(PRESET)
        tpl = template.substitute(
            x_start=to_percent(x, self.width),
            y_start=to_percent(y, self.height),
            x_end=to_percent(x, self.width),
            y_end=to_percent(y, self.height),
            frame_in=self.frame_in,
            frame_out=self.frame_out,
            frame_end=self.frame_end,
            height=to_percent(h, self.height),
            width=to_percent(w, self.width),
        )
        self.write_preset(f"{prefix}_{self.filename}", tpl)

    def calc_top_right(self, border: bool = True):
        x, y, w, h = self.grid_calc.calc_block(
            0, 1, self.size, self.size, border=border
        )
        prefix = "SlideIn_TR"
        if not border:
            prefix += "_B"
            template = Template(PRESET_BORDER)
        else:
            template = Template(PRESET)
        tpl = template.substitute(
            x_start=to_percent(x + w, self.width),
            y_start=to_percent(y, self.height),
            x_end=to_percent(x, self.width),
            y_end=to_percent(y, self.height),
            frame_in=self.frame_in,
            frame_out=self.frame_out,
            frame_end=self.frame_end,
            height=to_percent(h, self.height),
            width=to_percent(w, self.width),
        )
        self.write_preset(f"{prefix}_{self.filename}", tpl)

    def calc_bottom_left(self, border: bool = True):
        x, y, w, h = self.grid_calc.calc_block(
            1, 0, self.size, self.size, border=border
        )
        prefix = "SlideIn_BL"
        if not border:
            prefix += "_B"
            template = Template(PRESET_BORDER)
        else:
            template = Template(PRESET)
        tpl = template.substitute(
            x_start=to_percent(x, self.width),
            y_start=to_percent(y + h, self.height),
            x_end=to_percent(x, self.width),
            y_end=to_percent(y, self.height),
            frame_in=self.frame_in,
            frame_out=self.frame_out,
            frame_end=self.frame_end,
            height=to_percent(h, self.height),
            width=to_percent(w, self.width),
        )
        self.write_preset(f"{prefix}_{self.filename}", tpl)

    def calc_bottom_right(self, border: bool = True):
        x, y, w, h = self.grid_calc.calc_block(
            1, 1, self.size, self.size, border=border
        )
        prefix = "SlideIn_BR"
        if not border:
            prefix += "_B"
            template = Template(PRESET_BORDER)
        else:
            template = Template(PRESET)
        tpl = template.substitute(
            x_start=to_percent(x + w, self.width),
            y_start=to_percent(y + h, self.height),
            x_end=to_percent(x, self.width),
            y_end=to_percent(y, self.height),
            frame_in=self.frame_in,
            frame_out=self.frame_out,
            frame_end=self.frame_end,
            height=to_percent(h, self.height),
            width=to_percent(w, self.width),
        )
        self.write_preset(f"{prefix}_{self.filename}", tpl)

    def write_preset(self, name: str, preset: str):
        qf_name = urllib.parse.quote_plus(name)
        directory = Path(self.output).expanduser() / Path("presets/cropRectangle")
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        path = directory / Path(qf_name)
        print(f"create preset {name} : {path.resolve().name}")
        with open(path.resolve(), "w") as out_file:
            out_file.write(preset)

    def generate_preset(self):
        self.calc_top_left()
        self.calc_top_left(border=False)
        self.calc_top_right()
        self.calc_top_right(border=False)
        self.calc_bottom_left()
        self.calc_bottom_left(border=False)
        self.calc_bottom_right()
        self.calc_bottom_right(border=False)


def register() -> None:
    factory.register("slidein", SlideInPreset)
