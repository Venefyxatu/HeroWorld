from pathlib import Path
import pygame
from enum import Enum

from hero_world.constants import NeighborSlots


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


class Land:
    def __init__(self, pos, neighbors, tile_size, asset_root: Path) -> None:
        """
        neighbors: 1 for land, 0 for nothing
        """
        row = tile_size * (pos[0])
        col = tile_size * (pos[1])
        self.pos = (col, row)
        # self.pos = pos
        self.neighbors = neighbors
        self.asset_root = asset_root

    def draw(self, screen: pygame.surface.Surface) -> None:
        if (
            self.neighbors[NeighborSlots.TOP_LEFT] == 0
            and self.neighbors[NeighborSlots.TOP] == 0
            and self.neighbors[NeighborSlots.LEFT] == 0
        ):
            land_type = LandTiles.grass_top_left
        elif (
            self.neighbors[NeighborSlots.TOP] == 0
            and self.neighbors[NeighborSlots.LEFT] == 1
            and self.neighbors[NeighborSlots.RIGHT] == 1
        ):
            land_type = LandTiles.grass_top
        elif (
            self.neighbors[NeighborSlots.TOP] == 0
            and self.neighbors[NeighborSlots.TOP_RIGHT] == 0
            and self.neighbors[NeighborSlots.RIGHT] == 0
        ):
            land_type = LandTiles.grass_top_right
        elif (
            self.neighbors[NeighborSlots.LEFT] == 0
            and self.neighbors[NeighborSlots.TOP] == 1
            and self.neighbors[NeighborSlots.BOTTOM] == 1
        ):
            land_type = LandTiles.grass_left
        elif (
            self.neighbors[NeighborSlots.RIGHT] == 0
            and self.neighbors[NeighborSlots.TOP] == 1
            and self.neighbors[NeighborSlots.BOTTOM] == 1
        ):
            land_type = LandTiles.grass_right
        elif (
            self.neighbors[NeighborSlots.LEFT] == 0
            and self.neighbors[NeighborSlots.BOTTOM_LEFT] == 0
            and self.neighbors[NeighborSlots.BOTTOM] == 0
        ):
            land_type = LandTiles.grass_bottom_left
        elif (
            self.neighbors[NeighborSlots.BOTTOM] == 0
            and self.neighbors[NeighborSlots.LEFT] == 1
            and self.neighbors[NeighborSlots.RIGHT] == 1
        ):
            land_type = LandTiles.grass_bottom
        elif (
            self.neighbors[NeighborSlots.RIGHT] == 0
            and self.neighbors[NeighborSlots.BOTTOM] == 0
            and self.neighbors[NeighborSlots.BOTTOM_RIGHT] == 0
        ):
            land_type = LandTiles.grass_bottom_right
        elif (
            self.neighbors[NeighborSlots.TOP] == 1
            and self.neighbors[NeighborSlots.LEFT] == 1
            and self.neighbors[NeighborSlots.TOP_LEFT] == 0
        ):
            land_type = LandTiles.grass_inner_tl
        elif (
            self.neighbors[NeighborSlots.TOP] == 1
            and self.neighbors[NeighborSlots.RIGHT] == 1
            and self.neighbors[NeighborSlots.TOP_RIGHT] == 0
        ):
            land_type = LandTiles.grass_inner_tr
        elif (
            self.neighbors[NeighborSlots.LEFT] == 1
            and self.neighbors[NeighborSlots.BOTTOM] == 1
            and self.neighbors[NeighborSlots.BOTTOM_LEFT] == 0
        ):
            land_type = LandTiles.grass_inner_bl
        elif (
            self.neighbors[NeighborSlots.RIGHT] == 1
            and self.neighbors[NeighborSlots.BOTTOM] == 1
            and self.neighbors[NeighborSlots.BOTTOM_RIGHT] == 0
        ):
            land_type = LandTiles.grass_inner_br

        else:
            land_type = LandTiles.grass_field
        screen.blit(pygame.image.load(self.asset_root / land_type.value), self.pos)
