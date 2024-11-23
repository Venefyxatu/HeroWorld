from pathlib import Path
import random
import pygame

from hero_world.constants import NeighborSlots, LandTiles


class Land:
    def __init__(self, pos, neighbors, tile_size, asset_root: Path) -> None:
        """
        neighbors: 1 for land, 0 for nothing
        """
        row = tile_size * (pos[0])
        col = tile_size * (pos[1])
        self.pos = (col, row)
        self.neighbors = neighbors
        self.asset_root = asset_root
        self.land_type = None

    def choose_type(self):
        if (
            self.neighbors[NeighborSlots.TOP_LEFT] == 0
            and self.neighbors[NeighborSlots.TOP] == 0
            and self.neighbors[NeighborSlots.LEFT] == 0
        ):
            self.land_type = LandTiles.grass_top_left
        elif (
            self.neighbors[NeighborSlots.TOP] == 0
            and self.neighbors[NeighborSlots.LEFT] == 1
            and self.neighbors[NeighborSlots.RIGHT] == 1
        ):
            self.land_type = LandTiles.grass_top
        elif (
            self.neighbors[NeighborSlots.TOP] == 0
            and self.neighbors[NeighborSlots.TOP_RIGHT] == 0
            and self.neighbors[NeighborSlots.RIGHT] == 0
        ):
            self.land_type = LandTiles.grass_top_right
        elif (
            self.neighbors[NeighborSlots.LEFT] == 0
            and self.neighbors[NeighborSlots.TOP] == 1
            and self.neighbors[NeighborSlots.BOTTOM] == 1
        ):
            self.land_type = LandTiles.grass_left
        elif (
            self.neighbors[NeighborSlots.RIGHT] == 0
            and self.neighbors[NeighborSlots.TOP] == 1
            and self.neighbors[NeighborSlots.BOTTOM] == 1
        ):
            self.land_type = LandTiles.grass_right
        elif (
            self.neighbors[NeighborSlots.LEFT] == 0
            and self.neighbors[NeighborSlots.BOTTOM_LEFT] == 0
            and self.neighbors[NeighborSlots.BOTTOM] == 0
        ):
            self.land_type = LandTiles.grass_bottom_left
        elif (
            self.neighbors[NeighborSlots.BOTTOM] == 0
            and self.neighbors[NeighborSlots.LEFT] == 1
            and self.neighbors[NeighborSlots.RIGHT] == 1
        ):
            self.land_type = LandTiles.grass_bottom
        elif (
            self.neighbors[NeighborSlots.RIGHT] == 0
            and self.neighbors[NeighborSlots.BOTTOM] == 0
            and self.neighbors[NeighborSlots.BOTTOM_RIGHT] == 0
        ):
            self.land_type = LandTiles.grass_bottom_right
        elif (
            self.neighbors[NeighborSlots.TOP] == 1
            and self.neighbors[NeighborSlots.LEFT] == 1
            and self.neighbors[NeighborSlots.TOP_LEFT] == 0
        ):
            self.land_type = LandTiles.grass_inner_tl
        elif (
            self.neighbors[NeighborSlots.TOP] == 1
            and self.neighbors[NeighborSlots.RIGHT] == 1
            and self.neighbors[NeighborSlots.TOP_RIGHT] == 0
        ):
            self.land_type = LandTiles.grass_inner_tr
        elif (
            self.neighbors[NeighborSlots.LEFT] == 1
            and self.neighbors[NeighborSlots.BOTTOM] == 1
            and self.neighbors[NeighborSlots.BOTTOM_LEFT] == 0
        ):
            self.land_type = LandTiles.grass_inner_bl
        elif (
            self.neighbors[NeighborSlots.RIGHT] == 1
            and self.neighbors[NeighborSlots.BOTTOM] == 1
            and self.neighbors[NeighborSlots.BOTTOM_RIGHT] == 0
        ):
            self.land_type = LandTiles.grass_inner_br

        else:
            self.land_type = random.choice(
                [
                    LandTiles.grass_field,
                    LandTiles.poplar_1,
                    LandTiles.poplar_2,
                    LandTiles.poplar_3,
                    LandTiles.poplar_7,
                ]
            )

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(pygame.image.load(self.asset_root / self.land_type.value), self.pos)
