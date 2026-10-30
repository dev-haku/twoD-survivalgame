import pygame

from game.package.core.gameobject import Gameobject
from game.package.components.transform import Transform
from game.package.components.sprite_renderer import SpriteRenderer
from game.package.components.collider import Collider


class Square(Gameobject):
    def __init__(
            self, 
            position: tuple[float,float], 
            scale: tuple[float,float], 
            layer: int,
            color: tuple[int,int,int],
            hitbox_color: tuple[int,int,int]
        ):
        super().__init__()

        transfrom = Transform()
        transfrom.position = position
        transfrom.scale = scale
        transfrom.layer = layer
        self.add_component(transfrom)

        surface = pygame.Surface((8,8))
        surface.fill(color)
        sprite = SpriteRenderer()
        sprite.set_surface(surface)
        self.add_component(sprite)

        collider = Collider()
        collider.add_hitbox((0,0),(8,8), (hitbox_color))
        self.add_component(collider)