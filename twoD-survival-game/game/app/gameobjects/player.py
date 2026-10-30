import pygame
import math

from game.package import (
    Gameobject,
    Component,
    Transform,
    SpriteRenderer, 
    Collider,
)


class Player(Gameobject):

    def __init__(self, engine, scene, kwargs):
        super().__init__(engine, scene, kwargs)

        position: tuple[float,float] = kwargs["position"]
        layer: int = kwargs["layer"]
        
        transform = self.add_component(Transform)
        sprite_renderer = self.add_component(SpriteRenderer)
        collider = self.add_component(Collider)
        

        transform.position = position
        transform.scale = (1,1)
        transform.layer = layer

        surface = pygame.Surface((16,16))
        surface.fill((255,255,255))
        sprite_renderer.set_surface(surface)
        
        collider.is_collision_enabled = False
        collider.add_hitbox((0,0), (16,16), (0,255,0,200))

        self.add_component(Controller)

        self.move_speed = 50

        self.inventory = []

    

class Controller(Component):

    def __init__(self, engine, scene, parent, kwargs):
        super().__init__(engine, scene, parent, kwargs)
        self.dt = self.engine.delta_time
        self.keys = self.engine.input_status.keys

        self.parent_transform = self.parent.get_component("Transform")
    
    def update(self):
        
        w, h = self.parent.get_component("SpriteRenderer").get_surface().get_size()
        sx, sy = self.parent.get_component("Transform").scale
        scaled_size = (
            w * sx,
            h * sy
        )

        if self.keys.get("w", False):
            self.parent_transform.position.y -= (scaled_size[1] / 2) * self.parent.move_speed * self.dt

        if self.keys.get("s", False):
            self.parent_transform.position.y += (scaled_size[1] / 2) * self.parent.move_speed * self.dt

        if self.keys.get("a", False):
            self.parent_transform.position.x -= (scaled_size[0] / 2) *self.parent.move_speed * self.dt
        
        if self.keys.get("d", False):
            self.parent_transform.position.x += (scaled_size[0] / 2) *self.parent.move_speed * self.dt

        self.parent_transform.position.xy = round(self.parent_transform.position.xy)

        camera = self.engine.current_scene.get_gameobject("Camera1")
        camera_transform = camera.get_component("Transform")
        camera_transform.position = (
            self.parent_transform.position.x + scaled_size[0] //2,
            self.parent_transform.position.y + scaled_size[1] //2
            )

        return super().update()