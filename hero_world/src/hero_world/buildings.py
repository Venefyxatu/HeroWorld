from pathlib import Path
import pygame

from hero_world.constants import TILE_SIZE, NeighborSlots


class Building:
    def __init__(self, pos, tile_size: int, asset_root: Path) -> None:
        # print(f"Building init at pos {pos}")
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


class Forge(Building):
    def _load_image(self) -> pygame.surface.Surface:
        return pygame.image.load(self.asset_root / "structures/forge.png")


class Road(Building):
    def __init__(self, pos, tile_size: int, asset_root: Path, direction: str) -> None:
        self.direction = direction
        self.intention = direction
        print(f"Road direction: {self.direction}")
        super().__init__(pos, tile_size, asset_root)

    def _determine_crossroads(self):
        print(f"{self}.neighbors = {self.neighbors}")
        if all(self.neighbors.values()):
            self.direction = "4way"
        elif self.intention == "vert":
            if (
                self.neighbors[NeighborSlots.LEFT]
                and self.neighbors[NeighborSlots.RIGHT]
            ):
                self.direction = "4way"
            elif self.neighbors[NeighborSlots.LEFT]:
                self.direction = "t_right"
            elif self.neighbors[NeighborSlots.RIGHT]:
                self.direction = "t_left"
        elif self.intention == "hor":
            if (
                self.neighbors[NeighborSlots.TOP]
                and self.neighbors[NeighborSlots.BOTTOM]
            ):
                self.direction = "4way"
            elif self.neighbors[NeighborSlots.TOP]:
                self.direction = "t_down"
            elif self.neighbors[NeighborSlots.BOTTOM]:
                self.direction = "t_up"

    def _load_image(self) -> pygame.surface.Surface:
        self._determine_crossroads()
        print(f"direction at {self.pos} = {self.direction}")
        return pygame.image.load(
            self.asset_root / f"structures/road_{self.direction}.png"
        )
