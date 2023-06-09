from collections import namedtuple
from configparser import ConfigParser
from pathlib import Path

from generator.preset.types import InputValue


def dict_to_namedtuple(values: dict) -> namedtuple:
    names = [key for key in values.keys()]
    named_tuple = namedtuple("Values", names)
    return named_tuple(**values)


def get_input_values(values: list[InputValue]):
    names = [value.name for value in values]
    Values = namedtuple("Values", names)
    values = [value.value for value in values]
    return Values(*values)


def get_dict_values(values: list[InputValue]):
    value_dict = {value.name: value.value for value in values}
    return value_dict


def to_percent(value: int, max_value: int):
    percent: float = (float(value) / max_value) * 100
    return f"{percent:.4f}%"


def get_output_path(setting_files: list[str]):
    paths = [
        Path(dst).expanduser()
        for dst in setting_files
        if Path(dst).expanduser().exists()
    ]
    paths = sorted(paths, key=lambda path: path.stat().st_mtime, reverse=True)
    appdata_dir = None
    if paths:
        config_path: str = paths[0].as_posix()
        print(f" --> config path: {config_path}")
        config = ConfigParser()
        config.read(config_path)
        try:
            appdata_dir = Path(config["General"]["appdatadir"])
        except KeyError:
            if "/.var/app/org.shotcut.Shotcut/" in config_path:
                appdata_dir = Path(
                    "~/.var/app/org.shotcut.Shotcut/data/Meltytech/Shotcut"
                ).expanduser()
            elif "/.config/" in config_path:
                appdata_dir = Path("~/.local/share/Meltytech/Shotcut").expanduser()
    if appdata_dir and appdata_dir.exists():
        print(f" --> Shotcut app data dir: {appdata_dir}")
        return appdata_dir.as_posix()
    else:
        return None
