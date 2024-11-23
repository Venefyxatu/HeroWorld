from enum import Enum
from pathlib import Path
import pygame

import pygame_gui
import json

from hero_world.buildings import Forge, Road
from hero_world.player import Player
from hero_world.ui import UI
from hero_world.world import World
from hero_world.constants import (
    TILE_SIZE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    ASSET_ROOT,
)


class Buildings(Enum):
    FORGE = {"class": Forge, "cost": 5}
    ROAD_VERT = {"class": Road, "cost": 1, "kwargs": {"direction": "vert"}}
    ROAD_HOR = {"class": Road, "cost": 1, "kwargs": {"direction": "hor"}}
    ROAD_4WAY = {"class": Road, "cost": 1}
    ROAD_T_DOWN = {"class": Road, "cost": 1}
    ROAD_T_UP = {"class": Road, "cost": 1}


class Modes(Enum):
    NONE = None
    BUILD = "build"
    DESTROY = "destroy"


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
        self.player = Player()
        self.draw_ui()

    def draw_ui(self) -> None:
        self.ui.add_button(
            "#btn_forge_toggle",
            "",
            self.build,
            Buildings.FORGE,
        )
        self.ui.add_button(
            "#btn_road_h_toggle",
            "",
            self.build,
            Buildings.ROAD_HOR,
        )
        self.ui.add_button(
            "#btn_road_v_toggle",
            "",
            self.build,
            Buildings.ROAD_VERT,
        )
        self.ui.add_button("#btn_destroy_toggle", "", self.destroy)
        self.ui.add_button(
            "#btn_quit",
            "Quit",
            self.quit,
        )
        self.info_gold = self.ui.add_info("#info_gold", f"Gold: {self.player.gold}")

    def destroy(self):
        if self.mode != Modes.DESTROY:
            self.mode = Modes.DESTROY
        else:
            self.mode = Modes.NONE

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

    def _mouse_to_grid(self, mouse_position):
        return (int(mouse_position[1] / TILE_SIZE), int(mouse_position[0] / TILE_SIZE))

    def loop(self) -> None:
        time_delta = self.clock.tick(60) / 1000.0  # limits FPS to 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONUP and self.mode == Modes.DESTROY:
                pos = self._mouse_to_grid(pygame.mouse.get_pos())
                self.world.remove_building(pos)

            elif event.type == pygame.MOUSEBUTTONUP and self.mode == Modes.BUILD:
                pos = self._mouse_to_grid(pygame.mouse.get_pos())
                building = self.building.value
                if building["cost"] <= self.player.gold:
                    # print(f"add_building with pos: {pos}")
                    if self.world.add_building(
                        building["class"](
                            pos,
                            TILE_SIZE,
                            ASSET_ROOT,
                            *building.get("args", []),
                            **building.get("kwargs", {}),
                        )
                    ):
                        self.player.gold -= building["cost"]
                        self.ui.update_info(self.info_gold, f"Gold: {self.player.gold}")
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.mode = Modes.NONE
                enable = False
                for button in self.ui.buttons:
                    if button == event.ui_element:
                        # print(f"Unselect: skipping {button}")
                        continue
                    button.unselect()
                if any(
                    x.endswith("toggle")
                    for x in event.ui_element.object_ids
                    if isinstance(x, str)
                ):
                    if event.ui_element.is_selected:
                        # print(f"Unselecting {event.ui_element}")
                        event.ui_element.unselect()
                        enable = False
                    else:
                        # print(f"Selecting {event.ui_element}")
                        event.ui_element.select()
                        enable = True
                self.ui.button_clicked(event.ui_element, enable)
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
