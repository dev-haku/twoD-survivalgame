from pathlib import Path


ROOT = Path(__file__).resolve().parent

GAME_CONFIG = ROOT / "config.json"

ASSET_DIR = ROOT / "assets" 

DEFAULT_ICON_IMAGE = ASSET_DIR / "image" / "default_icon.ico"