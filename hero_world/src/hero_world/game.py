from enum import Enum
from pathlib import Path
import pygame

import pygame_gui
import json

from hero_world.buildings import Forge
from hero_world.ui import UI
from hero_world.world import World
from hero_world.constants import (
    TILE_SIZE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    ASSET_ROOT,
)


class Buildings(Enum):
    FORGE = Forge


class Modes(Enum):
    NONE = None
    BUILD = "build"


class TownGame:
    def __init__(self, world) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.world = World(self.screen, world)
        self.mode = Modes.NONE
        self.building = Buildings.FORGE
        self.manager = pygame_gui.UIManager(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            theme_path=Path(Path(__file__).absolute().parent / "theme.default.json"),
        )
        self.ui = UI(ASSET_ROOT, self.manager)
        self.draw_ui()

    def draw_ui(self) -> None:
        self.ui.add_button(
            "#btn_forge_toggle",
            "",
            self.build,
            Buildings.FORGE,
        )
        self.ui.add_button(
            "#btn_quit",
            "Quit",
            self.quit,
        )

    def build(self, building: Buildings):
        if self.mode != Modes.BUILD:
            self.mode = Modes.BUILD
            self.building = building
        else:
            self.mode = Modes.NONE

    def quit(self):
        self.running = False

    def main(self) -> None:
        while self.running:
            self.loop()
        pygame.quit()

    def loop(self) -> None:
        time_delta = self.clock.tick(60) / 1000.0  # limits FPS to 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONUP and self.mode == Modes.BUILD:
                pos = pygame.mouse.get_pos()
                self.world.add_building(self.building.value(pos, TILE_SIZE, ASSET_ROOT))
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if any(
                    x.endswith("toggle")
                    for x in event.ui_element.object_ids
                    if isinstance(x, str)
                ):
                    if self.mode == Modes.NONE:
                        event.ui_element.select()
                    else:
                        event.ui_element.unselect()
                self.ui.button_clicked(event.ui_element)
            self.manager.process_events(event)

        self.manager.update(time_delta)

        # self.screen.fill("#aaeebb")  # nice pygame-website-green
        self.screen.fill("#3498db")  # nice kenney-preview-blue
        self.world.draw()
        self.manager.draw_ui(self.screen)

        # flip() the display to put your work on screen
        pygame.display.flip()


def game():
    with open(Path(Path(__file__).absolute().parent / "world.json"), "r") as fp:
        world = json.load(fp)
    town_game = TownGame(world)
    town_game.main()


if __name__ == "__main__":
    game()
