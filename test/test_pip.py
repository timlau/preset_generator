import pytest
from generator.calc import PresetType

from generator.plugins.pip import PipPreset


@pytest.fixture
def pip():
    pip = PipPreset(name="pip", width=3840, height=2160, size=50.0, padding=32)
    inputs = pip.inputs()
    inputs[0].value = 50.0  # Size
    return pip


def test_pip_crop(monkeypatch, pip: PipPreset):
    res = []

    def write_preset(self, name: str, preset: str):
        res.append((name, preset))

    monkeypatch.setattr(PipPreset, "write_preset", write_preset)
    pip.active_type = PresetType.CROP_RECTANGLE
    pip.generate()
    assert len(res) == 4
    name, preset = res[0]
    assert name == "Pip_TopLeft_50%_Border"
    rect: str = preset.split("\n")[1]
    assert rect == "rect: 0.4167% 0.7407% 49.3750% 48.8889% 1"
    name, preset = res[1]
    assert name == "Pip_TopRight_50%_Border"
    rect: str = preset.split("\n")[1]
    assert rect == "rect: 50.2083% 0.7407% 49.3750% 48.8889% 1"
    name, preset = res[2]
    assert name == "Pip_BottomLeft_50%_Border"
    rect: str = preset.split("\n")[1]
    assert rect == "rect: 0.4167% 50.3704% 49.3750% 48.5185% 1"
    name, preset = res[3]
    assert name == "Pip_BottomRight_50%_Border"
    rect: str = preset.split("\n")[1]
    assert rect == "rect: 50.2083% 50.3704% 49.3750% 48.5185% 1"
