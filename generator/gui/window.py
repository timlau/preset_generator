from pathlib import Path
import platform

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
)
from PyQt6 import uic

from generator import DATA_DIR
from generator.plugins import PRESET_NAMES
from generator.preset import PresetGenerator
from generator.preset.types import InputValue
from generator.preset.utils import get_output_path


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        ui_file = DATA_DIR / Path("ui/main.ui")
        uic.loadUi(ui_file, self)
        self.presets = None
        self.ui = None
        self.settings = None

    def setup(self, settings):
        self.settings = settings
        self.get_output_path()

    def add_presets(self, presets: list[PresetGenerator]):
        self.presets = presets
        for preset in self.presets:
            self.cb_presets.addItem(preset.description)
        self.cb_presets.activated.connect(self.on_preset_activated)
        self.btn_generate.clicked.connect(self.on_generate_clicked)
        self.setup_parameters(self.presets[0])

    def get_output_path(self):
        print(f"platform: {platform.system()}")
        if platform.system() == "Linux":
            if path := get_output_path(self.settings.LIXUX_PATHS):
                self.settings = self.settings._replace(output=path)
                print(self.settings.output)

    def clean_out_widgets(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def setup_parameters(self, preset: PresetGenerator):
        self.cb_preset_type.clear()
        for preset_type in preset.types():
            self.cb_preset_type.addItem(PRESET_NAMES[preset_type])
        needed_values: list[InputValue] = preset.inputs()
        fbox = self.fl_parameters
        self.clean_out_widgets(fbox)
        self.ui = []
        for value in needed_values:
            label = QLabel(value.label)
            edit = QLineEdit()
            self.ui.append(edit)
            if value.value:
                edit.setText(str(value.value))
            fbox.addRow(label, edit)

    def on_preset_activated(self):
        index = self.cb_presets.currentIndex()
        print(f"New preset selected : {index}")
        self.setup_parameters(self.presets[index])

    def on_generate_clicked(self):
        index = self.cb_presets.currentIndex()
        preset = self.presets[index]
        index = self.cb_preset_type.currentIndex()
        preset.active_type = preset.types()[index]
        preset.output = self.settings.output
        print(f"Generating : {preset.name}")
        needed_values: list[InputValue] = preset.inputs()
        for i, value in enumerate(needed_values):
            text = self.ui[i].text()
            value.value_from_string(text)
        preset.generate()
