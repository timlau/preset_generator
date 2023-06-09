import platform
import os

from pathlib import Path
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout
from PyQt6 import uic
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtCore import QUrl, pyqtSlot

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
        self.presets: list[PresetGenerator] = None
        self.ui: list = None
        self.settings = None
        self.media_player: QMediaPlayer = None
        self.video_widget: QVideoWidget = None
        self.setGeometry(0, 0, 600, 920)

    def setup(self, settings):
        self.settings = settings
        self.get_output_path()

    def setup_video(self):
        box = QVBoxLayout()
        self.media_player = QMediaPlayer()
        self.media_player.errorOccurred.connect(self.on_player_error)
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)
        box.addWidget(self.video_widget)
        self.preview.setLayout(box)

    def play_video(self, preset: str):
        video = DATA_DIR / Path(f"media/{preset}.webm")
        if video.exists():
            if not self.media_player:
                self.setup_video()
            self.media_player.setSource(QUrl.fromLocalFile(video.as_posix()))
            self.media_player.setPosition(0)
            self.media_player.play()

    def add_presets(self, presets: list[PresetGenerator]):
        self.presets = presets
        for preset in self.presets:
            self.cb_presets.addItem(preset.description)
        self.cb_presets.activated.connect(self.on_preset_activated)
        self.btn_generate.clicked.connect(self.on_generate_clicked)
        self.le_output.textEdited.connect(self.on_output_edited)
        self.setup_parameters(self.presets[0])

    def get_output_path(self):
        print(f"platform: {platform.system()}")
        match platform.system().lower():
            case "linux":
                if path := get_output_path(self.settings.LIXUX_PATHS):
                    self.settings = self.settings._replace(output=path)
            case "windows":
                localappdata = os.getenv("LOCALAPPDATA")
                path = Path(localappdata) / Path("Meltytech") / Path("Shotcut")
                if path.exists():
                    self.settings = self.settings._replace(output=str(path))
            case "darwin":
                path = Path(
                    "~/Library/Application Support/Meltytech/Shotcut/"
                ).expanduser()
                if path.exists():
                    self.settings = self.settings._replace(output=str(path))
        print("Data directory: {self.settings.output}")

        self.le_output.setText(self.settings.output)

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
        self.play_video(preset.name.lower())

    @pyqtSlot("QMediaPlayer::Error", str)
    def on_player_error(self, error, error_string):
        print(f"Video player error : {error_string}")

    def on_output_edited(self, txt):
        self.settings = self.settings._replace(output=txt)
        print(self.settings.output)

    def on_preset_activated(self):
        index = self.cb_presets.currentIndex()
        print(f"New preset selected : {index}")
        preset = self.presets[index]
        self.setup_parameters(preset)

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
