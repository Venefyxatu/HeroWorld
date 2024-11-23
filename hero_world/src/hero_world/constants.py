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

NUM_BUTTONS = 6

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


class LandTiles(Enum):
    grass_top = "ground/grass_top.png"
    grass_top_left = "ground/grass_top_left.png"
    grass_top_right = "ground/grass_top_right.png"
    grass_bottom = "ground/grass_bottom.png"
    grass_bottom_left = "ground/grass_bottom_left.png"
    grass_bottom_right = "ground/grass_bottom_right.png"
    grass_left = "ground/grass_left.png"
    grass_right = "ground/grass_right.png"
    grass_field = "ground/grass_field.png"
    grass_inner_tl = "ground/grass_inner_tl.png"
    grass_inner_tr = "ground/grass_inner_tr.png"
    grass_inner_bl = "ground/grass_inner_bl.png"
    grass_inner_br = "ground/grass_inner_br.png"
    poplar_1 = "ground/poplar_1.png"
    poplar_2 = "ground/poplar_2.png"
    poplar_3 = "ground/poplar_3.png"
    poplar_7 = "ground/poplar_7.png"


NON_EDGE_LAND = [
    LandTiles.grass_field,
    LandTiles.poplar_1,
    LandTiles.poplar_2,
    LandTiles.poplar_3,
    LandTiles.poplar_7,
]
