""" slidein preset generator """

from string import Template
import urllib

from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
from generator.plugins import (
    CROP_BLOCKS,
    MASK_BLOCKS,
    BlockCalc,
    PresetType,
)
from generator.preset import factory
from generator.preset.utils import get_input_values, to_percent
from generator.preset.types import InputValue

PRESET = {
    PresetType.CROP_RECTANGLE: """---
rect: 0=$x_start $y_start 0 0 1;$frame_in=$x_end $y_end $width $height 1;$frame_out=$x_end $y_end $width $height 1;$frame_end=$x_start $y_start 0 0 1
radius: 0=0;$frame_in=0;$frame_out=0;$frame_end=0
color: "#00000000"
"shotcut:animIn": "00:00:01.000"
"shotcut:animOut": "00:00:01.000"
..."""  # noqa
}

PRESET_BORDER = {
    PresetType.CROP_RECTANGLE: """---
rect: 0|=0 0 0 0 1;$frame_in|=$x_end $y_end $width $height 1;$frame_out|=0 0 0 0 1
radius: 0
color: "#00000000"
"shotcut:animIn": "00:00:00.000"
"shotcut:animOut": "00:00:00.000"
..."""
}


@dataclass
class SlideInPreset:
    name: str
    width: round
    height: round
    size: float
    fps: int
    duration: int
    padding: round
    values: list[InputValue] = None
    output: str = "./shotcut"
    active_type: PresetType = PresetType.CROP_RECTANGLE

    def setup(self, settings: namedtuple) -> None:
        self.output = settings.output

    def generate(self) -> None:
        values: namedtuple = get_input_values(self.values)
        self.size = values.size
        self.fps = values.fps
        self.duration = values.duration
        self.calc_crop_preset()
        self.calc_crop_border_preset()

    def inputs(self) -> list[InputValue]:
        if not self.values:
            self.values = [
                InputValue("size", "Size(%)", float, self.size),
                InputValue("duration", "Duration", int, self.duration),
                InputValue("fps", "FPS", int, self.fps),
            ]
        return self.values

    def types(self) -> list(PresetType):
        return [PresetType.CROP_RECTANGLE]

    @property
    def description(self) -> str:
        return "Slide in from corners"

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
        return f"{self.size:.0f}%_{self.fps}fps_{self.duration}s"  # noqa

    def calc_crop_preset(self):
        calculator = BlockCalc(size=self.size)
        for corner in CROP_BLOCKS.keys():
            prefix = f"SlideIn_{corner.name}"
            template = Template(PRESET[self.active_type])
            x, y, w, h = calculator.calc_crop(corner)
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

    def calc_crop_border_preset(self):
        calculator = BlockCalc(size=self.size)
        for corner in MASK_BLOCKS.keys():
            prefix = f"SlideIn_{corner.name}_B"
            template = Template(PRESET_BORDER[self.active_type])
            x, y, w, h = calculator.calc_mask(corner)
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
            self.write_preset(f"{prefix}_{self.filename}_Border", tpl)

    def write_preset(self, name: str, preset: str):
        qf_name = urllib.parse.quote_plus(name)
        directory = (
            Path(self.output).expanduser() / Path("presets") / Path(self.active_type)
        )
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        path = directory / Path(qf_name)
        print(f"create preset {name} : {path.resolve().name} in {directory}")
        with open(path.resolve(), "w") as out_file:
            out_file.write(preset)


def register() -> None:
    factory.register("slidein", SlideInPreset)
