from dataclasses import dataclass
from enum import StrEnum
from functools import cached_property


class PresetType(StrEnum):
    CROP_RECTANGLE = "cropRectangle"
    SIZE_POSITION_ROTATE = "affineSizePosition"
    MASK_SIMPLE = "maskSimpleShape"


PRESET_NAMES = {
    PresetType.CROP_RECTANGLE: "Crop Rectangle",
    PresetType.SIZE_POSITION_ROTATE: "Size, Position & Restore",
    PresetType.MASK_SIMPLE: "Mask: Simple Shape",
}


@dataclass
class GridCalculator:
    rows: int
    columns: int
    width: int = 3840
    height: int = 2150
    padding: int = 32

    @cached_property
    def grid_width(self):
        return round(self.width / self.columns)

    @cached_property
    def grid_height(self):
        return round(self.height / self.rows)

    def calc_block(self, start_row, start_col, num_row, num_col, border: bool = True):
        last_col = start_col + num_col
        last_row = start_row + num_row
        if border:
            dt = self.padding / 2
            extra = 0
        else:
            dt = 0
            # if no border we need to add extra to width & height
            extra = self.padding / 2
        x = round(dt + (start_col * self.grid_width))
        y = round(dt + (start_row * self.grid_height))
        if last_col == self.columns:
            width = round(num_col * self.grid_width - (2 * dt)) + extra
        else:
            width = round(num_col * self.grid_width - (dt)) + extra
        if last_row == self.rows:
            height = round(num_row * self.grid_height - (2 * dt)) + extra
        else:
            height = round(num_row * self.grid_height - (dt)) + extra
        return x, y, width, height
