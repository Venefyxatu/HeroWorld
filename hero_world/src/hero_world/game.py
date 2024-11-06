import pygame
import json

from hero_world.buildings import Building, Forge
from hero_world.land import Land

TILE_SIZE = 64
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

DEBUG = False


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
        self.land.append(Land(position, neighbors, TILE_SIZE))

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


class TownGame:
    def __init__(self, world) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.world = World(self.screen, world)

    def main(self) -> None:
        while self.running:
            self.loop()
        pygame.quit()

    def loop(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.world.add_building(Forge(pos, TILE_SIZE))

        # self.screen.fill("#aaeebb")  # nice pygame-website-green
        self.screen.fill("#3498db")  # nice kenney-preview-blue
        self.world.draw()

        # flip() the display to put your work on screen
        pygame.display.flip()

        self.clock.tick(60)  # limits FPS to 60


def game():
    with open("world.json", "r") as fp:
        world = json.load(fp)
    town_game = TownGame(world)
    town_game.main()


if __name__ == "__main__":
    game()
