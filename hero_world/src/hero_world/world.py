import pygame

from hero_world.buildings import Building
from hero_world.land import Land
from hero_world.constants import (
    TILE_SIZE,
    ASSET_ROOT,
    DEBUG,
)


class World:
    def __init__(self, screen, world) -> None:
        self.screen = screen
        self.buildings = {}
        self.columns = len(world[0])
        self.rows = len(world)
        self.land_positions = []
        self.land = []
        self._create_land(world)

    def _get_neighbors(self, world, row_index, col_index):
        neighbors = [
            world[row_index - 1][col_index - 1]
            if row_index > 0 and col_index > 0
            else 0,
            world[row_index - 1][col_index] if row_index > 0 else 0,
            world[row_index - 1][col_index + 1]
            if row_index > 0 and col_index < len(world[0]) - 1
            else 0,
            world[row_index][col_index - 1] if col_index > 0 else 0,
            world[row_index][col_index + 1] if col_index < len(world[0]) - 1 else 0,
            world[row_index + 1][col_index - 1]
            if row_index < len(world) - 1 and col_index > 0
            else 0,
            world[row_index + 1][col_index] if row_index < len(world) - 1 else 0,
            world[row_index + 1][col_index + 1]
            if row_index < len(world) - 1 and col_index < len(world[0]) - 1
            else 0,
        ]
        return neighbors

    def _create_land(self, world) -> None:
        for row_index, row in enumerate(world):
            for col_index, _ in enumerate(row):
                if world[row_index][col_index] == 1:
                    neighbors = self._get_neighbors(world, row_index, col_index)
                    self._add_land(row_index, col_index, neighbors)

    def _add_land(self, x, y, neighbors) -> None:
        position = (y * TILE_SIZE, x * TILE_SIZE)
        self.land_positions.append(position)
        self.land.append(Land(position, neighbors, TILE_SIZE, ASSET_ROOT))

    def add_building(self, building: Building) -> None:
        building_pos = (building.pos[0], building.pos[1])
        if building_pos not in self.buildings and building_pos in self.land_positions:
            self.buildings[building_pos] = building

    def draw(self) -> None:
        if DEBUG:
            for row in range(self.rows):
                for col in range(row % 2, self.columns, 2):
                    pygame.draw.rect(
                        self.screen,
                        (40, 40, 40),
                        (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )
        for land in self.land:
            land.draw(self.screen)
        for building in self.buildings.values():
            building.draw(self.screen)
