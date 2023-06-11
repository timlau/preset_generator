import pytest

from generator.plugins.grid import GridPreset


@pytest.fixture
def grid_res(monkeypatch):
    res = []

    def write_preset(self, name: str, preset: str):
        res.append((name, preset))

    monkeypatch.setattr(GridPreset, "write_preset", write_preset)
    grid = GridPreset(name="grid")
    inputs = grid.inputs()
    # 2x2 Grid
    inputs[0].value = 2  # rows
    inputs[1].value = 2  # columns
    grid.generate()
    return res


def test_grid_11_11(grid_res):
    """Test TopLeft Grid"""
    assert len(grid_res) == 9
    fname, preset = grid_res[0]
    preset = preset.split("\n")
    assert fname == "Grid_2x2_(1,1.1x1)"
    # p_x = (padding/2)/width*100 = (16/3840)*100 ≈ 0.4167
    # p_y = (padding/2)/height*100 = (16/2160)*100 ≈ 0.7407
    # P_width = (width/cols-padding/2)/width*100 = (3840/2-16)/3840*100 ≈ 49.5833
    # p_height = (height/rows-padding/2)/height*100 = (2160/2-16)/2160*100 ≈ 49.2593
    assert preset[1] == "rect: 0.4167% 0.7407% 49.5833% 49.2593% 1"


def test_grid_12_11(grid_res):
    """Test TopRight Grid"""
    assert len(grid_res) == 9
    fname, preset = grid_res[4]
    preset = preset.split("\n")
    assert fname == "Grid_2x2_(1,2.1x1)"
    # p_x = (col*width/cols+padding/2)/width*100 = (1*3840/2+16)/3840*100 ≈ 50,4167
    # p_y = (padding/2)/height*100 = (16/2160)*100 ≈ 0.7407
    # P_width = (width/cols-padding)/width*100 = (3840/2-32)/3840*100 ≈ 49,1667
    # p_height = (height/rows-padding/2)/height*100 = (2160/2-16)/2160*100 ≈ 49.2593
    assert preset[1] == "rect: 50.4167% 0.7407% 49.1667% 49.2593% 1"


def test_grid_21_11(grid_res):
    """Test BottomLeft Grid"""
    assert len(grid_res) == 9
    fname, preset = grid_res[6]
    preset = preset.split("\n")
    assert fname == "Grid_2x2_(2,1.1x1)"
    # p_x = (padding/2)/width*100 = (16/3840)*100 ≈ 0.4167
    # p_y = (row*height/rows+padding/2)/height*100 = (1*2160/2+16)/2160*100 ≈ 50.7407
    # P_width = (width/cols-padding/2)/width*100 = (3840/2-16)/3840*100 ≈ 49.5833
    # p_height = (height/rows-padding)/height*100 = (2160/2-32)/2160*100 ≈ 48.5185
    assert preset[1] == "rect: 0.4167% 50.7407% 49.5833% 48.5185% 1"


def test_grid_22_11(grid_res):
    """Test BottomRight Grid"""
    assert len(grid_res) == 9
    fname, preset = grid_res[8]
    preset = preset.split("\n")
    assert fname == "Grid_2x2_(2,2.1x1)"
    # p_x = (col*width/cols+padding/2)/width*100 = (1*3840/2+16)/3840*100 ≈ 50,4167
    # p_yy = (row*height/rows+padding/2)/height*100 = (1*2160/2+16)/2160*100 ≈ 50,7407
    # P_width = (width/cols-padding)/width*100 = (3840/2-32)/3840*100 ≈ 49,1667
    # p_height = (height/rows-padding)/height*100 = (2160/2-32)/2160*100 ≈ 48,5185
    assert preset[1] == "rect: 50.4167% 50.7407% 49.1667% 48.5185% 1"
