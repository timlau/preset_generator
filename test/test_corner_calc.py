import pytest
from generator.plugins import CROP_BLOCKS, BlockCalc, BlockType


@pytest.fixture
def calc() -> BlockCalc:
    return BlockCalc(size=50)


@pytest.fixture
def calc75() -> BlockCalc:
    return BlockCalc(size=75)


def test_prefix(calc: BlockCalc):
    assert calc.prefix_x == 1920
    assert calc.prefix_y == 1080


def test_border(calc: BlockCalc):
    assert calc.border == 16


def test_block_wh(calc: BlockCalc):
    assert calc.block_width == 1920
    assert calc.block_height == 1080


def test_start_point_top_left(calc: BlockCalc):
    mod = CROP_BLOCKS[BlockType.TopLeft]
    x, y = calc.start_point(mod)
    assert x == 16
    assert y == 16


def test_start_point_top_right(calc: BlockCalc):
    mod = CROP_BLOCKS[BlockType.TopRight]
    x, y = calc.start_point(mod)
    assert x == 1928
    assert y == 16


def test_start_point_bottom_left(calc: BlockCalc):
    mod = CROP_BLOCKS[BlockType.BottomLeft]
    x, y = calc.start_point(mod)
    assert x == 16
    assert y == 1088


def test_start_point_bottom_right(calc: BlockCalc):
    mod = CROP_BLOCKS[BlockType.BottomRight]
    x, y = calc.start_point(mod)
    assert x == 1928
    assert y == 1088


def test_block_size_top_left(calc: BlockCalc):
    mod = CROP_BLOCKS[BlockType.TopLeft]
    _, _, w, h = calc.block_size(mod)
    assert w == 1896
    assert h == 1056


def test_block_size_top_right(calc: BlockCalc):
    mod = CROP_BLOCKS[BlockType.TopRight]
    print(mod)
    _, _, w, h = calc.block_size(mod)
    assert w == 1896
    assert h == 1056


def test_block_size_bottom_left(calc: BlockCalc):
    mod = CROP_BLOCKS[BlockType.BottomLeft]
    print(mod)
    _, _, w, h = calc.block_size(mod)
    assert w == 1896
    assert h == 1048


def test_block_size_bottom_right(calc: BlockCalc):
    mod = CROP_BLOCKS[BlockType.BottomRight]
    print(mod)
    _, _, w, h = calc.block_size(mod)
    assert w == 1896
    assert h == 1048


def test_calc_crop(calc: BlockCalc):
    x, y, w, h = calc.calc_crop(BlockType.TopLeft)
    assert w == 1896
    assert h == 1056
    assert x == 16
    assert y == 16


def test_calc_crop75(calc75: BlockCalc):
    x, y, w, h = calc75.calc_crop(BlockType.TopLeft)
    assert w == 2856
    assert h == 1596
    assert x == 16
    assert y == 16


def test_calc_mask_top_left(calc: BlockCalc):
    x, y, w, h = calc.calc_mask(BlockType.TopLeft)
    assert w == 1928
    assert h == 1088
    assert x == 0
    assert y == 0


def test_calc_mask_top_right(calc: BlockCalc):
    x, y, w, h = calc.calc_mask(BlockType.TopRight)
    assert w == 1928
    assert h == 1088
    assert x == 1912
    assert y == 0


def test_calc_mask_bottom_left(calc: BlockCalc):
    x, y, w, h = calc.calc_mask(BlockType.BottomLeft)
    assert w == 1928
    assert h == 1088
    assert x == 0
    assert y == 1072


def test_calc_mask_bottom_right(calc: BlockCalc):
    x, y, w, h = calc.calc_mask(BlockType.BottomRight)
    assert w == 1928
    assert h == 1088
    assert x == 1912
    assert y == 1072


def test_calc_spr_top_left(calc: BlockCalc):
    x, y, w, h = calc.calc_spr(BlockType.TopLeft)
    assert w == 1920
    assert h == 1080
    assert x == 0
    assert y == 0


def test_calc_spr_top_right(calc: BlockCalc):
    x, y, w, h = calc.calc_spr(BlockType.TopRight)
    assert w == 1920
    assert h == 1080
    assert x == 1920
    assert y == 0


def test_calc_spr_bottom_left(calc: BlockCalc):
    x, y, w, h = calc.calc_spr(BlockType.BottomLeft)
    assert w == 1920
    assert h == 1080
    assert x == 0
    assert y == 1080


def test_calc_spr_bottom_right(calc: BlockCalc):
    x, y, w, h = calc.calc_spr(BlockType.BottomRight)
    assert w == 1920
    assert h == 1080
    assert x == 1920
    assert y == 1080
