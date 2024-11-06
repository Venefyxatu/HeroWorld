import pygame


class Building:
    def __init__(self, pos, tile_size) -> None:
        x = tile_size * (pos[0] // tile_size)
        y = tile_size * (pos[1] // tile_size)
        self.pos = (x, y)
        self.image = self._load_image()

    def _load_image(self) -> pygame.surface.Surface:
        raise NotImplementedError("Children must implement this")

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.pos)


class Forge(Building):
    def _load_image(self) -> pygame.surface.Surface:
        return pygame.image.load("assets/structures/forge.png")
