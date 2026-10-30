import pygame

from game.package.core.gameobject import Gameobject
from game.package.components.transform import RectTransform
from game.package.components.sprite_renderer import SpriteRenderer


class Image(Gameobject):
    def __init__(self, engine, scene, kwargs):
        super().__init__(engine, scene, kwargs)

        surface: pygame.Surface = kwargs["surface"]
        position: tuple[float,float] = kwargs["position"]
        scale: tuple[float,float] = kwargs["scale"]
        layer: int = kwargs["layer"]

        transform = self.add_component(RectTransform)
        transform.position = position
        transform.scale = scale
        transform.layer = layer

        surface = pygame.Surface((16,16))
        surface.fill((255,255,255))
        sprite_renderer = self.add_component(SpriteRenderer)
        sprite_renderer.set_surface(surface)

    def set_surface(self, surface: pygame.Surface):
        self.sprite_renderer.set_surface(surface)