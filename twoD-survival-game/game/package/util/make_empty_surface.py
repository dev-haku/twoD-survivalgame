import pygame

from game import paths


def make_empty_surface() -> pygame.Surface:
    try:
        surface = pygame.image.load(paths.ASSET_DIR / "image" / "cb.jpg")
        return surface
    except pygame.error:
        return pygame.Surface.__new__(pygame.Surface)