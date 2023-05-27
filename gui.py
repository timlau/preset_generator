import sys

from PyQt6.QtWidgets import QApplication

from generator.gui.window import MainWindow
from generator.preset import load_presets

if __name__ == "__main__":
    presets, settings = load_presets()
    # Qt application setup
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.setup(settings)
    win.add_presets(presets)
    win.show()
    sys.exit(app.exec())
