import pygame

from hero_world.buildings import Building
from hero_world.land import Land
from hero_world.constants import (
    TILE_SIZE,
    ASSET_ROOT,
    DEBUG,
    NeighborSlots,
    NON_EDGE_LAND,
    LandTiles,
)


class World:
    def __init__(self, screen, world) -> None:
        self.screen = screen
        self.buildings = {}
        self.world = world
        self.columns = len(world[0])
        self.rows = len(world)
        self.land = {}
        self._create_land()

    def _get_neighboring_structures(self, row_index, col_index):
        neighboring_structures = {
            NeighborSlots.TOP: self.buildings.get((row_index - 1, col_index)),
            NeighborSlots.LEFT: self.buildings.get((row_index, col_index - 1)),
            NeighborSlots.RIGHT: self.buildings.get((row_index, col_index + 1)),
            NeighborSlots.BOTTOM: self.buildings.get((row_index + 1, col_index)),
        }
        return neighboring_structures

    def _get_neighbors(self, row_index, col_index):
        neighbors = {
            NeighborSlots.TOP_LEFT: self.world[row_index - 1][col_index - 1]
            if row_index > 0 and col_index > 0
            else 0,
            NeighborSlots.TOP: self.world[row_index - 1][col_index]
            if row_index > 0
            else 0,
            NeighborSlots.TOP_RIGHT: self.world[row_index - 1][col_index + 1]
            if row_index > 0 and col_index < len(self.world[0]) - 1
            else 0,
            NeighborSlots.LEFT: self.world[row_index][col_index - 1]
            if col_index > 0
            else 0,
            NeighborSlots.RIGHT: self.world[row_index][col_index + 1]
            if col_index < len(self.world[0]) - 1
            else 0,
            NeighborSlots.BOTTOM_LEFT: self.world[row_index + 1][col_index - 1]
            if row_index < len(self.world) - 1 and col_index > 0
            else 0,
            NeighborSlots.BOTTOM: self.world[row_index + 1][col_index]
            if row_index < len(self.world) - 1
            else 0,
            NeighborSlots.BOTTOM_RIGHT: self.world[row_index + 1][col_index + 1]
            if row_index < len(self.world) - 1 and col_index < len(self.world[0]) - 1
            else 0,
        }
        return neighbors

    def _create_land(self) -> None:
        for row_index, row in enumerate(self.world):
            for col_index, _ in enumerate(row):
                if self.world[row_index][col_index] == 1:
                    neighbors = self._get_neighbors(row_index, col_index)
                    self._add_land(row_index, col_index, neighbors)
        for land in self.land.values():
            land.choose_type()

    def _add_land(self, row, col, neighbors) -> None:
        position = (row, col)
        self.land[position] = Land(position, neighbors, TILE_SIZE, ASSET_ROOT)

    def add_building(self, building: Building) -> bool:
        building_pos = (building.pos[0], building.pos[1])
        if building_pos not in self.buildings and building_pos in self.land.keys():
            self.buildings[building_pos] = building
            if self.land[building_pos].land_type in NON_EDGE_LAND:
                self.land[building_pos].land_type = LandTiles.grass_field
            return True
        return False

    def remove_building(self, pos) -> None:
        if pos in self.buildings:
            self.buildings.pop(pos)

    def draw(self) -> None:
        if DEBUG:
            for row in range(self.rows):
                for col in range(row % 2, self.columns, 2):
                    pygame.draw.rect(
                        self.screen,
                        (40, 40, 40),
                        (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )
        for land in self.land.values():
            land.draw(self.screen)
        for position, building in self.buildings.items():
            neighbors = self._get_neighboring_structures(position[0], position[1])
            for position, neighbor in neighbors.items():
                if neighbor:
                    building.neighbors[position] = True
                else:
                    building.neighbors[position] = False
            building.draw(self.screen)
