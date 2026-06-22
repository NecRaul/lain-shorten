import copy
import json
import os
import platform
from pathlib import Path

CONFIG_NAMESPACE = "necraul"
CONFIG_NAME = "lain-shorten.json"

DEFAULT_CONFIG = {
    "default_shortener": "lainla",
    "open_urls": False,
}


def get_default_config_path():
    match platform.system():
        case "Windows":
            base = os.getenv("APPDATA")
            if base:
                config_dir = Path(base)
            else:
                config_dir = Path.home() / "AppData" / "Roaming"
        case "Darwin":
            config_dir = Path.home() / "Library" / "Application Support"
        case "Linux":
            config_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
        case _:
            config_dir = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
    return config_dir / CONFIG_NAMESPACE / CONFIG_NAME


def load_config(path=None):
    if path is None:
        path = get_default_config_path()
    else:
        path = Path(path).expanduser()
    if not path.exists():
        return copy.deepcopy(DEFAULT_CONFIG)
    with path.open("r", encoding="utf-8") as f:
        user_cfg = json.load(f)
    return merge_config(DEFAULT_CONFIG, user_cfg)


def merge_config(base, override):
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    return result


def save_config(cfg, path=None):
    if path is None:
        path = get_default_config_path()
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")
    return path.absolute()


def load_effective_config(path=None, no_config=False):
    if no_config:
        return copy.deepcopy(DEFAULT_CONFIG)
    if path:
        return load_config(path)
    return load_config()
