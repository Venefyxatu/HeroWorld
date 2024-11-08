from pathlib import Path
from typing import Callable

import pygame
import pygame_gui

DEFAULT_ICON = "buttons/default.png"
BUTTON_BACKGROUND = "buttons/background.png"
BUTTON_BORDER = "buttons/border.png"
BUTTON_FORGE = "buttons/forge.png"

BUTTON_HEIGHT = 40


# class Button:
#     def __init__(
#         self,
#         screen,
#         name: str,
#         pos: tuple[int, int],
#         asset_root: Path,
#         icon: Optional[str] = None,
#     ) -> None:
#         self.screen = screen
#         self.name = name
#         self.icon = icon if icon else DEFAULT_ICON
#         self.asset_root = asset_root
#         self.pos = pos
#
#     def draw(self):
#         self.screen.blit(self._load_image(BUTTON_BACKGROUND), self.pos)
#         self.screen.blit(self._load_image(BUTTON_BORDER), self.pos)
#         self.screen.blit(
#             self._load_image(self.icon, inner=True), (self.pos[0] + 5, self.pos[1] + 5)
#         )
#
#     def _load_image(self, path: str, inner: bool = False) -> pygame.surface.Surface:
#         height = BUTTON_HEIGHT - 10 if inner else BUTTON_HEIGHT
#         return pygame.transform.scale(
#             pygame.image.load(self.asset_root / path), (height, height)
#         )


class UI:
    def __init__(
        self,
        asset_root: Path,
        manager: pygame_gui.UIManager,
    ) -> None:
        self.pos = (20, 20)
        self.asset_root = asset_root
        self.buttons = {}
        self.manager = manager
        self.button_bar = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(20, 20, 80, 140),
            manager=self.manager,
            # margins={"top": 10, "left": 10, "right": 10, "bottom": 10},
        )

    def add_button(
        self,
        button_id: str,
        text: str,
        callback: Callable,
        *args,
        **kwargs,
    ) -> None:
        self.buttons[
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    10,
                    10 + (60 * len(self.buttons)) if len(self.buttons) else 10,
                    60,
                    60,
                ),
                text=text,
                manager=self.manager,
                container=self.button_bar,
                object_id=button_id,
            )
        ] = {"callback": callback, "args": args, "kwargs": kwargs}

    def button_clicked(self, button: pygame_gui.elements.UIButton) -> None:
        action = self.buttons[button]
        action["callback"](*action["args"], **action["kwargs"])
