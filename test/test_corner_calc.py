import pytest
from generator.plugins import MOD_CORNERS, BorderCalc, CornerType


@pytest.fixture
def calc() -> BorderCalc:
    return BorderCalc(size=50)


def test_prefix(calc: BorderCalc):
    assert calc.prefix_x == 1920
    assert calc.prefix_y == 1080


def test_border(calc: BorderCalc):
    assert calc.border == 16


def test_block_wh(calc: BorderCalc):
    assert calc.block_width == 1920
    assert calc.block_height == 1080


def test_start_point_top_left(calc: BorderCalc):
    mod = MOD_CORNERS[CornerType.TopLeft]
    x, y = calc.start_point(mod)
    assert x == 16
    assert y == 16


def test_start_point_top_right(calc: BorderCalc):
    mod = MOD_CORNERS[CornerType.TopRight]
    x, y = calc.start_point(mod)
    assert x == 1928
    assert y == 16


def test_start_point_bottom_left(calc: BorderCalc):
    mod = MOD_CORNERS[CornerType.BottomLeft]
    x, y = calc.start_point(mod)
    assert x == 16
    assert y == 1088


def test_start_point_bottom_right(calc: BorderCalc):
    mod = MOD_CORNERS[CornerType.BottomRight]
    x, y = calc.start_point(mod)
    assert x == 1928
    assert y == 1088


def test_block_size_top_left(calc: BorderCalc):
    mod = MOD_CORNERS[CornerType.TopLeft]
    _, _, w, h = calc.block_size(mod)
    assert w == 1896
    assert h == 1056


def test_block_size_top_right(calc: BorderCalc):
    mod = MOD_CORNERS[CornerType.TopRight]
    print(mod)
    _, _, w, h = calc.block_size(mod)
    assert w == 1896
    assert h == 1056


def test_block_size_bottom_left(calc: BorderCalc):
    mod = MOD_CORNERS[CornerType.BottomLeft]
    print(mod)
    _, _, w, h = calc.block_size(mod)
    assert w == 1896
    assert h == 1056


def test_block_size_bottom_right(calc: BorderCalc):
    mod = MOD_CORNERS[CornerType.BottomRight]
    print(mod)
    _, _, w, h = calc.block_size(mod)
    assert w == 1896
    assert h == 1056


def test_calc_block(calc: BorderCalc):
    x, y, w, h = calc.calc_block(CornerType.TopLeft)
    assert w == 1896
    assert h == 1056
    assert x == 16
    assert y == 16
