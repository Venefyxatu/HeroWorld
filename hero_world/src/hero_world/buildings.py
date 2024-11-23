from pathlib import Path
import pygame

from hero_world.constants import TILE_SIZE, NeighborSlots


class Building:
    cost = 0

    def __init__(self, pos, tile_size: int, asset_root: Path) -> None:
        x = pos[0]  # row
        y = pos[1]  # column
        self.pos = (x, y)
        self.asset_root = asset_root
        self.neighbors = {
            NeighborSlots.TOP: False,
            NeighborSlots.BOTTOM: False,
            NeighborSlots.LEFT: False,
            NeighborSlots.RIGHT: False,
        }
        self.image = self._load_image()

    def _load_image(self) -> pygame.surface.Surface:
        raise NotImplementedError("Children must implement this")

    def _draw_pos(self):
        return (self.pos[1] * TILE_SIZE, self.pos[0] * TILE_SIZE)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self._load_image(), self._draw_pos())


class WoodCutter(Building):
    cost = 2

    def _load_image(self) -> pygame.surface.Surface:
        return pygame.image.load(self.asset_root / "structures/woodcutter.png")


class Forge(Building):
    cost = 5

    def _load_image(self) -> pygame.surface.Surface:
        return pygame.image.load(self.asset_root / "structures/forge.png")


class Road(Building):
    cost = 1

    def __init__(self, pos, tile_size: int, asset_root: Path, direction: str) -> None:
        self.direction = direction
        self.intention = direction
        super().__init__(pos, tile_size, asset_root)

    def _determine_crossroads(self):
        if all(self.neighbors.values()):
            self.direction = "4way"
        elif all(x is False for x in self.neighbors.values()):
            self.direction = self.intention
        elif (
            self.neighbors[NeighborSlots.LEFT]
            and self.neighbors[NeighborSlots.RIGHT]
            and self.neighbors[NeighborSlots.BOTTOM]
            and not self.neighbors[NeighborSlots.TOP]
        ):
            self.direction = "t_down"
        elif (
            self.neighbors[NeighborSlots.LEFT]
            and self.neighbors[NeighborSlots.RIGHT]
            and self.neighbors[NeighborSlots.TOP]
            and not self.neighbors[NeighborSlots.BOTTOM]
        ):
            self.direction = "t_up"
        elif (
            self.neighbors[NeighborSlots.LEFT]
            and self.neighbors[NeighborSlots.BOTTOM]
            and self.neighbors[NeighborSlots.TOP]
            and not self.neighbors[NeighborSlots.RIGHT]
        ):
            self.direction = "t_left"
        elif (
            self.neighbors[NeighborSlots.RIGHT]
            and self.neighbors[NeighborSlots.BOTTOM]
            and self.neighbors[NeighborSlots.TOP]
            and not self.neighbors[NeighborSlots.LEFT]
        ):
            self.direction = "t_right"
        elif (
            self.neighbors[NeighborSlots.LEFT]
            and self.neighbors[NeighborSlots.BOTTOM]
            and not self.neighbors[NeighborSlots.RIGHT]
            and not self.neighbors[NeighborSlots.TOP]
        ):
            self.direction = "c_up_left"
        elif (
            self.neighbors[NeighborSlots.RIGHT]
            and self.neighbors[NeighborSlots.BOTTOM]
            and not self.neighbors[NeighborSlots.LEFT]
            and not self.neighbors[NeighborSlots.TOP]
        ):
            self.direction = "c_up_right"
        elif (
            self.neighbors[NeighborSlots.LEFT]
            and self.neighbors[NeighborSlots.TOP]
            and not self.neighbors[NeighborSlots.RIGHT]
            and not self.neighbors[NeighborSlots.BOTTOM]
        ):
            self.direction = "c_down_left"
        elif (
            self.neighbors[NeighborSlots.RIGHT]
            and self.neighbors[NeighborSlots.TOP]
            and not self.neighbors[NeighborSlots.LEFT]
            and not self.neighbors[NeighborSlots.BOTTOM]
        ):
            self.direction = "c_down_right"
        elif self.intention == "vert":
            if (
                self.neighbors[NeighborSlots.LEFT]
                and self.neighbors[NeighborSlots.RIGHT]
            ):
                self.direction = "4way"
            elif self.neighbors[NeighborSlots.LEFT]:
                self.direction = "t_left"
            elif self.neighbors[NeighborSlots.RIGHT]:
                self.direction = "t_right"
        elif self.intention == "hor":
            if (
                self.neighbors[NeighborSlots.TOP]
                and self.neighbors[NeighborSlots.BOTTOM]
            ):
                self.direction = "4way"
            elif self.neighbors[NeighborSlots.TOP]:
                self.direction = "t_up"
            elif self.neighbors[NeighborSlots.BOTTOM]:
                self.direction = "t_down"

    def _load_image(self) -> pygame.surface.Surface:
        self._determine_crossroads()
        return pygame.image.load(
            self.asset_root / f"structures/road_{self.direction}.png"
        )
