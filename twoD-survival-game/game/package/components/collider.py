from dataclasses import dataclass
import pygame

from game.package.core.render_data import RenderData
from game.package.core.component import Component


@dataclass
class Hitbox:
    offset_position: tuple[int,int]
    size: tuple[int,int]
    color: tuple[int,int,int]
        

class Collider(Component):
    def __init__(self, engine, scene, parent, kwargs):
        super().__init__(engine, scene, parent, kwargs)
        
        self.hitboxes = []
        self.last_pos = (0,0)
        self.is_collision_enabled = True

        self.parent_transform = self.parent.get_component("Transform")

        self.render_data = RenderData()
        self.render_data.transform_type = self.parent_transform.__class__.__name__

        self.last_pos = self.parent_transform.position

    def update(self):
        if self.engine.debug_settings["show_colliders"]:
            self._update_debug_surface()

        if self.is_collision_enabled:
            self._resolve_collision()

        return super().update()

    def add_hitbox(
            self, 
            offset_position: tuple[float,float], 
            size: tuple[float,float], 
            color: tuple[float,float,float,float] = (255,255,255)
        ):
        self.hitboxes.append(Hitbox(offset_position, size, color))

    def is_colliding(self):
        if self.active == False:
            return

        for my_hitbox in self.hitboxes:

           
           my_rect = self._create_rect(self.parent_transform, my_hitbox)
           
           for target_gameobject in self.scene.gameobjects:
                if target_gameobject is self.parent:
                    continue

                target_collider = target_gameobject.get_component("Collider")
                target_transform = target_gameobject.get_component("Transform")
                if target_collider is None or target_transform is None:
                   continue

                if target_collider.active == False:
                    continue

                for target_hitbox in target_collider.hitboxes:

                    target_rect = self._create_rect(target_transform, target_hitbox)

                    if my_rect.colliderect(target_rect):
                        return True
                
        return False
    
    def get_colliding_gameobjects(self):
        colliding_objects = []

        if self.active == False:
            return colliding_objects

        for my_hitbox in self.hitboxes:
           
            my_rect = self._create_rect(self.parent_transform, my_hitbox)
           
            for target_gameobject in self.scene.gameobjects:
                if target_gameobject is self.parent:
                    continue

                target_collider = target_gameobject.get_component("Collider")
                target_transform = target_gameobject.get_component("Transform")
                if target_collider is None or target_transform is None:
                   continue

                if target_collider.active == False:
                    continue

                for target_hitbox in target_collider.hitboxes:

                    target_rect = self._create_rect(target_transform, target_hitbox)

                    if my_rect.colliderect(target_rect):
                        colliding_objects.append(target_gameobject)
                        break
                
        return colliding_objects

    def _resolve_collision(self):
        if self.is_colliding():
            self.parent_transform.position = self.last_pos
            return
        
        self.last_pos = self.parent_transform.position
    
    def _create_rect(self, transform, hitbox):
        pos = (
            transform.position.x + (hitbox.offset_position[0] * transform.scale.x),
            transform.position.y + (hitbox.offset_position[1] * transform.scale.y)
        )

        scaled_size = (
            hitbox.size[0] * transform.scale.x,
            hitbox.size[1] * transform.scale.y
        )

        return pygame.Rect(
            pos[0],
            pos[1],
            scaled_size[0],
            scaled_size[1]
        )
    
    def _update_debug_surface(self):

        position = self.parent_transform.position
        scale = self.parent_transform.scale


        scaled_hitboxes = [
            (
                hitbox.offset_position[0] * scale[0],
                hitbox.offset_position[1] * scale[1],
                hitbox.size[0] * scale[0],
                hitbox.size[1] * scale[1],
                hitbox.color
                )
            for hitbox in self.hitboxes
        ]


        first = scaled_hitboxes[0]

        left = first[0]
        top = first[1]
        right = first[0] + first[2]
        bottom = first[1] + first[3]

        for hitbox in scaled_hitboxes:
            left = min(left, hitbox[0])
            top = min(top, hitbox[1])
            right = max(right, hitbox[0] + hitbox[2])
            bottom = max(bottom, hitbox[1] + hitbox[3])

        x = left
        y = top
        w = right - left
        h = bottom - top

        combined_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        combined_surface.fill((255,255,255,0))


        for hitbox in scaled_hitboxes:
            hitbox_surface = pygame.Surface((hitbox[2],hitbox[3]), pygame.SRCALPHA)
            hitbox_surface.fill(hitbox[4])
            combined_surface.blit(hitbox_surface, (hitbox[0] - x, hitbox[1] - y))

        self.render_data.surface = combined_surface
        self.render_data.position.xy = (position.x + x, position.y + y)
        self.render_data.layer = self.transform.layer +1

