import pygame
from game.package.util.make_empty_surface import make_empty_surface

class RenderData:
    def __init__(self):
        self.surface: pygame.Surface = make_empty_surface()
        self.position: pygame.Vector2 = pygame.Vector2()
        self.layer: int = 0
        self.transform_type = None