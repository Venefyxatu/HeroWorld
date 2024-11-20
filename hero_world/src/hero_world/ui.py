from pathlib import Path
from typing import Callable

import pygame
import pygame_gui


from hero_world.constants import (
    BUTTON_HEIGHT,
    BUTTON_BAR_MARGIN,
    INFO_HEIGHT,
    NUM_BUTTONS,
)


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
                (NUM_BUTTONS * BUTTON_HEIGHT) + (2 * BUTTON_BAR_MARGIN),
            ),
            manager=self.manager,
            # margins={"top": 10, "left": 10, "right": 10, "bottom": 10},
        )
        self.info_bar = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(400, 20, 500, INFO_HEIGHT), manager=self.manager
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

    def button_clicked(
        self, button: pygame_gui.elements.UIButton, enable: bool = False
    ) -> None:
        action = self.buttons[button]
        toggle_button = any(
            x.endswith("toggle") for x in button.object_ids if isinstance(x, str)
        )
        if (enable and toggle_button) or not toggle_button:
            action["callback"](*action["args"], **action["kwargs"])

    def add_info(self, info_id: str, text: str) -> pygame_gui.elements.UILabel:
        return pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 100, INFO_HEIGHT - 20),
            text=text,
            object_id=info_id,
            container=self.info_bar,
        )

    def update_info(self, info_label: pygame_gui.elements.UILabel, text: str) -> None:
        info_label.text = text
        info_label.rebuild()
