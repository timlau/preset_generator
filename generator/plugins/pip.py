""" slidein preset generator """

from string import Template
import urllib

from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path
from generator.plugins import CROP_CORNERS, MASK_CORNERS, BorderCalc, PresetType
from generator.preset import factory
from generator.preset.utils import get_input_values, to_percent
from generator.preset.types import InputValue

PRESETS = {
    PresetType.SIZE_POSITION_ROTATE: """---
transition.fill: 1
transition.distort: 0
transition.rect: $x $y $width $height 1
transition.halign: center
transition.valign: middle
"shotcut:animIn": "00:00:00.000"
"shotcut:animOut": "00:00:00.000"
...""",
    PresetType.MASK_SIMPLE: """---
filter.1: 0.252083
filter.2: 0.253704
filter.3: 0.252083
filter.4: 0.253704
filter.0: 0
filter.5: 0.5
filter.6: 0
filter.9: 0
"shotcut:rect": $x $y $width $height 1
...""",
    PresetType.CROP_RECTANGLE: """---
rect: $x $y $width $height 1
radius: 0
color: "#00000000"
...""",
}


@dataclass
class PipPreset:
    name: str
    width: round
    height: round
    size: float
    padding: round
    values: list[InputValue] = None
    output: str = "./shotcut"
    active_type: PresetType = PresetType.SIZE_POSITION_ROTATE

    def setup(self, settings: namedtuple) -> None:
        self.output = settings.output

    def generate(self) -> None:
        values: namedtuple = get_input_values(self.values)
        self.size = values.size
        match (self.active_type):
            case PresetType.CROP_RECTANGLE:
                self.calc_crop_preset()
            case PresetType.SIZE_POSITION_ROTATE:
                self.calc_spr_preset()
            case PresetType.MASK_SIMPLE:
                self.calc_mask_preset()

    def inputs(self) -> list[InputValue]:
        if not self.values:
            self.values = [
                InputValue("size", "Size(%)", float, self.size),
            ]
        return self.values

    def types(self) -> list(PresetType):
        return [
            PresetType.SIZE_POSITION_ROTATE,
            PresetType.MASK_SIMPLE,
            PresetType.CROP_RECTANGLE,
        ]

    @property
    def description(self) -> str:
        return "Picture in Picture"

    @property
    def filename(self):
        if self.active_type in [PresetType.MASK_SIMPLE, PresetType.CROP_RECTANGLE]:
            return f"{self.size:.0f}%_Border"  # noqa
        else:
            return f"{self.size:.0f}%"  # noqa

    def padded_size(self):
        return to_percent(
            self.border + round((self.size / 100) * self.width), self.width
        )

    @property
    def prefix(self):
        return (100 - self.size) / 100

    @property
    def border(self):
        if self.active_type == PresetType.MASK_SIMPLE:
            return self.padding / 2
        else:
            return 0

    def calc_crop_preset(self):
        calculator = BorderCalc(size=self.size)
        for corner in CROP_CORNERS.keys():
            prefix = f"Pip_{corner.name}"
            template = Template(PRESETS[self.active_type])
            x, y, w, h = calculator.calc_crop(corner)
            tpl = template.substitute(
                x=to_percent(x, self.width),
                y=to_percent(y, self.height),
                height=to_percent(h, self.height),
                width=to_percent(w, self.width),
            )
            self.write_preset(f"{prefix}_{self.filename}", tpl)

    def calc_mask_preset(self):
        calculator = BorderCalc(size=self.size)
        for corner in MASK_CORNERS.keys():
            prefix = f"Pip_{corner.name}"
            template = Template(PRESETS[self.active_type])
            x, y, w, h = calculator.calc_mask(corner)
            tpl = template.substitute(
                x=to_percent(x, self.width),
                y=to_percent(y, self.height),
                height=to_percent(h, self.height),
                width=to_percent(w, self.width),
            )
            self.write_preset(f"{prefix}_{self.filename}", tpl)

    def calc_top_left(self, border: bool = True):
        prefix = "Pip_TopLeft"
        template = Template(PRESETS[self.active_type])
        x = y = 0
        tpl = template.substitute(
            x=to_percent(x, self.width),
            y=to_percent(y, self.height),
            height=self.padded_size(),
            width=self.padded_size(),
        )
        self.write_preset(f"{prefix}_{self.filename}", tpl)

    def calc_top_right(self, border: bool = True):
        prefix = "Pip_TopRight"
        template = Template(PRESETS[self.active_type])
        x = round(self.prefix * self.width)
        y = 0
        tpl = template.substitute(
            x=to_percent(x, self.width),
            y=to_percent(y, self.height),
            height=self.padded_size(),
            width=self.padded_size(),
        )
        self.write_preset(f"{prefix}_{self.filename}", tpl)

    def calc_bottom_left(self, border: bool = True):
        prefix = "Pip_BottomLeft"
        template = Template(PRESETS[self.active_type])
        x = 0
        y = round(self.prefix * self.height)
        tpl = template.substitute(
            x=to_percent(x, self.width),
            y=to_percent(y, self.height),
            height=self.padded_size(),
            width=self.padded_size(),
        )
        self.write_preset(f"{prefix}_{self.filename}", tpl)

    def calc_bottom_right(self, border: bool = True):
        prefix = "Pip_BottomRight"
        template = Template(PRESETS[self.active_type])
        x = round(self.prefix * self.width)
        y = round(self.prefix * self.height)
        tpl = template.substitute(
            x=to_percent(x, self.width),
            y=to_percent(y, self.height),
            height=self.padded_size(),
            width=self.padded_size(),
        )
        self.write_preset(f"{prefix}_{self.filename}", tpl)

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

    def calc_spr_preset(self):
        self.calc_top_left()
        self.calc_top_right()
        self.calc_bottom_left()
        self.calc_bottom_right()


def register() -> None:
    factory.register("pip", PipPreset)
