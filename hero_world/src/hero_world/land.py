import pygame


class LandTiles:
    grass_top = "assets/ground/grass_top.png"
    grass_top_left = "assets/ground/grass_top_left.png"
    grass_top_right = "assets/ground/grass_top_right.png"
    grass_bottom = "assets/ground/grass_bottom.png"
    grass_bottom_left = "assets/ground/grass_bottom_left.png"
    grass_bottom_right = "assets/ground/grass_bottom_right.png"
    grass_left = "assets/ground/grass_left.png"
    grass_right = "assets/ground/grass_right.png"
    grass_field = "assets/ground/grass_field.png"
    grass_inner_tl = "assets/ground/grass_inner_tl.png"
    grass_inner_tr = "assets/ground/grass_inner_tr.png"
    grass_inner_bl = "assets/ground/grass_inner_bl.png"
    grass_inner_br = "assets/ground/grass_inner_br.png"


class Land:
    def __init__(self, pos, neighbors, tile_size) -> None:
        """
        neighbors: tl, t, tr, l, r, bl, b, br, 1 for land, 0 for nothing
        """
        x = tile_size * (pos[0] // tile_size)
        y = tile_size * (pos[1] // tile_size)
        self.pos = (x, y)
        self.neighbors = neighbors

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
        screen.blit(pygame.image.load(land_type), self.pos)
