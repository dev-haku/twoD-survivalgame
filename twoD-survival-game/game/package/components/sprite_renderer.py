import pygame
from pathlib import Path

from game.package.core.render_data import RenderData
from game.package.core.component import Component
from game.package.components.transform import Transform, RectTransform
from game.package.util.make_empty_surface import make_empty_surface


class SpriteRenderer(Component):

    def __init__(self, engine, scene, parent, kwargs):
        super().__init__(engine, scene, parent, kwargs)

        self.original_surface: pygame.Surface | None = kwargs.get("surface")
        self.flag = True
        self.render_data = RenderData()

        self.rotation_angle = 0

        a = self.parent.get_component("Transform")
        b = self.parent.get_component("RectTransform")
        if not a is None:
            self.transform: Transform = a
        else:
            self.transform: RectTransform = b

        self.render_data.transform_type = self.transform.__class__.__name__

    def update(self):

        if self.flag:
            
            # original_surface_size = self.original_surface.get_size()
            # parent_scale = self.transform.scale.xy
        

            # surface = pygame.Surface((original_surface_size[0]*2, original_surface_size[1]*2))
            # surface.fill((0,255,0))
  
            # sw, sh = surface.get_size()
            # surface.blit(
            #     self.original_surface, 
            #     (
            #         sw/2 - original_surface_size[0]/2,
            #         sh/2 - original_surface_size[1]/2)
            #     )

            # rotated_surface = pygame.transform.rotate(surface, self.rotation_angle) 

            # scaled_surface = pygame.transform.scale(
            #     rotated_surface, 
            #     (
            #         rotated_surface.get_width() * parent_scale[0],
            #         rotated_surface.get_height() * parent_scale[1]
            #     )
            # )

            # self.render_data.surface = scaled_surface

            parent_scale = self.transform.scale.xy

            scaled_surface = pygame.transform.scale(
                self.original_surface, 
                (
                    self.original_surface.get_width() * parent_scale[0],
                    self.original_surface.get_height() * parent_scale[1]
                )
            )
        
            surface = pygame.Surface((scaled_surface.get_width()*2, scaled_surface.get_height()*2), pygame.SRCALPHA)
            surface.blit(
                scaled_surface, 
                (
                    surface.get_width()/2 - scaled_surface.get_width()/2,
                    surface.get_height()/2 - scaled_surface.get_height()/2)
                )

            rotated_surface = pygame.transform.rotate(surface, self.rotation_angle) 

            self.render_data.surface = rotated_surface

            self.flag = False

        self.render_data.position.xy = (
            self.transform.position.x - self.render_data.surface.get_width()/4, 
            self.transform.position.y - self.render_data.surface.get_height()/4
        )
        
        self.render_data.layer = self.transform.layer

        return super().update()
    
    def get_surface(self) -> pygame.Surface:
        return self.original_surface
    
    def set_surface(self, surface : pygame.Surface):
        self.original_surface = surface
        self.flag = True

    def load_surface(self, image_path: Path):
        self.original_surface = pygame.image.load(image_path)
        self.flag = True

    def set_rotation_angle(self, angle_value):
        self.rotation_angle = angle_value
        self.flag = True


class SimpleSpriteRenderer(Component):
    def __init__(self, engine, scene, parent, kwargs):
        super().__init__(engine, scene, parent, kwargs)

        surface: pygame.Surface = kwargs["surface"]

        self.render_data = RenderData()
        self.render_data.surface = surface

        self.parent_transform = None

        a = self.parent.get_component("Transform")
        b = self.parent.get_component("RectTransform")
        if not a is None:
            self.parent_transform: Transform = a
        else:
            self.parent_transform: RectTransform = b
        
        self.render_data.transform_type = self.parent_transform.__class__.__name__
        
    def update(self):
        
        self.render_data.position.xy = (
            self.parent_transform.position.x, 
            self.parent_transform.position.y
        )

        self.render_data.layer = self.parent_transform.layer

        return super().update()
        