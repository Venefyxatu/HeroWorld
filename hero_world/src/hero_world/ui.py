from pathlib import Path
from typing import Callable

import pygame
import pygame_gui


from hero_world.constants import BUTTON_HEIGHT, BUTTON_BAR_MARGIN


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
            relative_rect=pygame.Rect(
                20,
                20,
                BUTTON_HEIGHT + (2 * BUTTON_BAR_MARGIN),
                (2 * BUTTON_HEIGHT) + (2 * BUTTON_BAR_MARGIN),
            ),
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
                    BUTTON_BAR_MARGIN,
                    BUTTON_BAR_MARGIN + (BUTTON_HEIGHT * len(self.buttons))
                    if len(self.buttons)
                    else BUTTON_BAR_MARGIN,
                    BUTTON_HEIGHT,
                    BUTTON_HEIGHT,
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
