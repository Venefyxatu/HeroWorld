from enum import Enum
from pathlib import Path

DEBUG = False

ASSET_ROOT = Path(Path(__file__).absolute().parent / "assets")

# UI Settings
TILE_SIZE = 64
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
INFO_HEIGHT = 40

BUTTON_HEIGHT = 60
BUTTON_BAR_MARGIN = 10

NUM_BUTTONS = 5

# Player Settings
INITIAL_GOLD = 200


class NeighborSlots(Enum):
    TOP_LEFT = 0
    TOP = 1
    TOP_RIGHT = 2
    LEFT = 3
    RIGHT = 4
    BOTTOM_LEFT = 5
    BOTTOM = 6
    BOTTOM_RIGHT = 7
