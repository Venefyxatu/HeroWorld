from pathlib import Path
import pygame


class LandTiles:
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
        neighbors: tl, t, tr, l, r, bl, b, br, 1 for land, 0 for nothing
        """
        x = tile_size * (pos[0] // tile_size)
        y = tile_size * (pos[1] // tile_size)
        self.pos = (x, y)
        self.neighbors = neighbors
        self.asset_root = asset_root

    def draw(self, screen: pygame.surface.Surface) -> None:
        if self.neighbors[0] == 0 and self.neighbors[1] == 0 and self.neighbors[3] == 0:
            land_type = LandTiles.grass_top_left
        elif (
            self.neighbors[1] == 0 and self.neighbors[3] == 1 and self.neighbors[4] == 1
        ):
            land_type = LandTiles.grass_top
        elif (
            self.neighbors[1] == 0 and self.neighbors[2] == 0 and self.neighbors[4] == 0
        ):
            land_type = LandTiles.grass_top_right
        elif (
            self.neighbors[3] == 0 and self.neighbors[1] == 1 and self.neighbors[6] == 1
        ):
            land_type = LandTiles.grass_left
        elif (
            self.neighbors[4] == 0 and self.neighbors[1] == 1 and self.neighbors[6] == 1
        ):
            land_type = LandTiles.grass_right
        elif (
            self.neighbors[3] == 0 and self.neighbors[5] == 0 and self.neighbors[6] == 0
        ):
            land_type = LandTiles.grass_bottom_left
        elif (
            self.neighbors[6] == 0 and self.neighbors[3] == 1 and self.neighbors[4] == 1
        ):
            land_type = LandTiles.grass_bottom
        elif (
            self.neighbors[4] == 0 and self.neighbors[6] == 0 and self.neighbors[7] == 0
        ):
            land_type = LandTiles.grass_bottom_right
        elif (
            self.neighbors[1] == 1 and self.neighbors[3] == 1 and self.neighbors[0] == 0
        ):
            land_type = LandTiles.grass_inner_tl
        elif (
            self.neighbors[1] == 1 and self.neighbors[4] == 1 and self.neighbors[2] == 0
        ):
            land_type = LandTiles.grass_inner_tr
        elif (
            self.neighbors[3] == 1 and self.neighbors[6] == 1 and self.neighbors[5] == 0
        ):
            land_type = LandTiles.grass_inner_bl
        elif (
            self.neighbors[4] == 1 and self.neighbors[6] == 1 and self.neighbors[7] == 0
        ):
            land_type = LandTiles.grass_inner_br

        else:
            land_type = LandTiles.grass_field
        screen.blit(pygame.image.load(self.asset_root / land_type), self.pos)
