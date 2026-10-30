import pygame
import random

from game.package import (
    Gameobject,
    Transform,
    SpriteRenderer, 
    Collider
)


class EnemyManager:
    def __init__(self):
        pass


class Enemy(Gameobject):

    def __init__(self, position, scale, layer):
        super().__init__()

        self.tags.append("Enemy")

        self.transform = Transform()
        self.transform.position = position
        self.transform.scale = scale
        self.transform.layer = layer
        self.add_component(self.transform)

        surface = pygame.Surface((16,16))
        surface.fill((211, 211, 211))
        self.sprite_renderer = SpriteRenderer()
        self.sprite_renderer.set_surface(surface)
        self.add_component(self.sprite_renderer)

        collider = Collider()
        collider.add_hitbox((0,0),(8,8), ((0,255,0,200)))
        collider.is_collision_enabled = False
        self.add_component(collider)

        self.move_speed = 1

        self.rotation_angle = 0
        
    def start(self):
        self.dt = self.engine.delta_time

    def update(self):
        return super().update()
