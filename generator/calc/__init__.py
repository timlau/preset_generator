from dataclasses import dataclass
from typing import Self

from generator.plugins import BlockType


@dataclass
class VideoBlock:
    x: int
    y: int
    width: int
    height: int

    def split(self, rows: int, cols: int):
        row_height = round(self.height / rows)
        col_width = round(self.width / cols)
        start_x = self.x
        start_y = self.y
        for row in range(rows):
            for col in range(cols):
                start_x = self.x + col * col_width
                start_y = self.y + row * row_height
                yield VideoBlock(start_x, start_y, col_width, row_height)

    def set_padding(self, padding: int):
        self.x += padding
        self.y += padding
        self.width -= 2 * padding
        self.height -= 2 * padding

    def scale(self, factor: float, center: bool = False):
        center_x = round(self.x + self.width / 2)
        center_y = round(self.y + self.height / 2)
        self.width = round(self.width * factor)
        self.height = round(self.height * factor)
        if center:
            self.x = center_x - self.width / 2
            self.y = center_y - self.height / 2

    def move_to_corner(self, frame: Self, corner: BlockType):
        match corner:
            case BlockType.TopLeft:
                self.x = 0
                self.y = 0
            case BlockType.TopRight:
                self.x = frame.width - self.width
                self.y = 0
            case BlockType.BottomLeft:
                self.x = 0
                self.y = frame.height - self.height
            case BlockType.BottomRight:
                self.x = frame.width - self.width
                self.y = frame.height - self.height

    def __iadd__(self, other: Self):
        self.x += other.x
        self.y += other.y
        self.width += other.width
        self.height += other.height
        return self

    def __add__(self, other: Self):
        self += other
        return self

    def __isub__(self, other: Self):
        self.x -= other.x
        self.y -= other.y
        self.width -= other.width
        self.height -= other.height
        return self

    def __sub__(self, other: Self):
        self -= other
        return self
