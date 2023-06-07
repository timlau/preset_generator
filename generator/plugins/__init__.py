from collections import namedtuple
from dataclasses import dataclass
from enum import IntEnum, StrEnum
from functools import cached_property


class PresetType(StrEnum):
    CROP_RECTANGLE = "cropRectangle"
    SIZE_POSITION_ROTATE = "affineSizePosition"
    MASK_SIMPLE = "maskSimpleShape"


PRESET_NAMES = {
    PresetType.CROP_RECTANGLE: "Crop Rectangle",
    PresetType.SIZE_POSITION_ROTATE: "Size, Position & Rotate",
    PresetType.MASK_SIMPLE: "Mask: Simple Shape",
}


ModMatrix = namedtuple("ModMatrix", ["dx", "dy", "dw", "dh", "xadj", "yadj"])


class BlockType(IntEnum):
    TopLeft = 1
    TopRight = 2
    BottomLeft = 3
    BottomRight = 4


CROP_BLOCKS = {
    BlockType.TopLeft: ModMatrix(dx=1, dy=1, dw=1.5, dh=1.5, xadj=0, yadj=0),
    BlockType.TopRight: ModMatrix(dx=0.5, dy=1, dw=1.5, dh=1.5, xadj=1, yadj=0),
    BlockType.BottomLeft: ModMatrix(dx=1, dy=0.5, dw=1.5, dh=2, xadj=0, yadj=1),
    BlockType.BottomRight: ModMatrix(dx=0.5, dy=0.5, dw=1.5, dh=2, xadj=1, yadj=1),
}

MASK_BLOCKS = {
    BlockType.TopLeft: ModMatrix(dx=0, dy=0, dw=-0.5, dh=-0.5, xadj=0, yadj=0),
    BlockType.TopRight: ModMatrix(dx=-0.5, dy=0, dw=-0.5, dh=-0.5, xadj=1, yadj=0),
    BlockType.BottomLeft: ModMatrix(dx=0, dy=-0.5, dw=-0.5, dh=-0.5, xadj=0, yadj=1),
    BlockType.BottomRight: ModMatrix(
        dx=-0.5, dy=-0.5, dw=-0.5, dh=-0.5, xadj=1, yadj=1
    ),
}

SPR_BLOCKS = {
    BlockType.TopLeft: ModMatrix(dx=0, dy=0, dw=-0, dh=0, xadj=0, yadj=0),
    BlockType.TopRight: ModMatrix(dx=-0, dy=0, dw=0, dh=0, xadj=1, yadj=0),
    BlockType.BottomLeft: ModMatrix(dx=0, dy=-0, dw=0.0, dh=-0, xadj=0, yadj=1),
    BlockType.BottomRight: ModMatrix(dx=0, dy=0, dw=-0, dh=-0, xadj=1, yadj=1),
}


@dataclass
class BlockCalc:
    size: float
    width: int = 3840
    height: int = 2160
    padding: int = 32

    @property
    def prefix_x(self):
        return ((100 - self.size) / 100) * self.width

    @property
    def prefix_y(self):
        return ((100 - self.size) / 100) * self.height

    @property
    def border(self):
        return self.padding / 2

    @property
    def block_width(self):
        return self.width * (self.size / 100)

    @property
    def block_height(self):
        return self.height * (self.size / 100)

    def position(self, mod: ModMatrix):
        x0 = mod.xadj * self.prefix_x
        y0 = mod.yadj * self.prefix_y
        x = x0 + (self.border * mod.dx)
        y = y0 + (self.border * mod.dy)
        return x, y

    def calc_block(self, mod: ModMatrix):
        x, y = self.position(mod)
        w = self.block_width - (self.border * mod.dw)
        h = self.block_height - (self.border * mod.dh)
        return round(x), round(y), round(w), round(h)

    def calc_crop(self, corner: BlockType):
        mod = CROP_BLOCKS[corner]
        return self.calc_block(mod)

    def calc_mask(self, corner: BlockType):
        mod = MASK_BLOCKS[corner]
        return self.calc_block(mod)

    def calc_spr(self, corner: BlockType):
        mod = SPR_BLOCKS[corner]
        return self.calc_block(mod)


@dataclass
class GridCalculator:
    rows: int
    columns: int
    width: int = 3840
    height: int = 2160
    padding: int = 32

    @cached_property
    def block_width(self):
        return round(self.width / self.columns)

    @cached_property
    def block_height(self):
        return round(self.height / self.rows)

    def calc_block(self, start_row, start_col, num_row, num_col, border: bool = True):
        last_col = start_col + num_col
        last_row = start_row + num_row
        if border:
            dt = self.padding / 2
        else:
            dt = 0
        x = dt + (start_col * self.block_width)
        y = dt + (start_row * self.block_height)
        if last_col == self.columns:
            width = num_col * self.block_width - (2 * dt)
        else:
            width = num_col * self.block_width - (dt)
        if last_row == self.rows:
            height = num_row * self.block_height - (2 * dt)
        else:
            height = num_row * self.block_height - (dt)
        return round(x), round(y), round(width), round(height)
