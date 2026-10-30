from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import sys

from game.package.gameobjects.world.camera import Camera

if TYPE_CHECKING:
    from game.package.core.engine import Engine
    from game.package.core.gameobject import Gameobject
    from game.package.core.render_data import RenderData


def create_render_data_list(gameobjects) -> list[RenderData]:
    return  [
        comp.render_data
        for go in gameobjects
        if get_state(go)
        for comp in go.components.values()
        if hasattr(comp, "render_data")
    ]

def get_state(object):

    if object is None:
        return False
    
    if not object.active:
        return False
    
    return True

class Scene:
    
    def __init__(self, engine: Engine):

        self.engine: Engine = engine

        self.active: bool = True
        self.is_started: bool = False

        self.gameobjects: list[Gameobject] = [] 
        self.screen: pygame.Surface = pygame.Surface(self.engine.window.get_size())

        self.add_gameobject(Camera)

    def add_gameobject(self, gameobject_class: type[Gameobject], **kwargs):

        gameobject = gameobject_class(self.engine, self, kwargs)

        target_name = gameobject.__class__.__name__
        count = 0
        for obj in self.gameobjects:
            if obj.__class__.__name__ == target_name:
                count += 1

        gameobject.id = f"{gameobject.__class__.__name__}{count + 1}"

        self.gameobjects.append(gameobject)

        return gameobject

    def get_gameobject(self, gameobject_id: str) -> Gameobject|None:

        for gameobject in self.gameobjects:
            if gameobject.id == gameobject_id:
                return gameobject
            
        return None

    def update(self):
        for go in self.gameobjects:
            go.update()
            for comp in go.components.values():       
                comp.update()

    def render(self) -> pygame.Surface:
        self.screen.fill((0, 0, 0))
        return self._render_gameobjects(self.screen)

    def _render_gameobjects(self, screen):

        camera = self.get_gameobject("Camera1")
        if not get_state(camera):
            return

        camera_transform = camera.get_component("Transform")
        if not get_state(camera_transform):
            return
        
        camera_position = camera_transform.position.xy
        camera_anchor = camera.anchor

        render_data_list = create_render_data_list(self.gameobjects)
        render_data_list.sort(key=lambda x: x.layer)  

        for meta_layer in ["World","Canvas"]:
            
            for render_data in render_data_list:

                draw_surface = render_data.surface
                gameobject_position = render_data.position

                position_dict = {
                    "Canvas" : (
                        gameobject_position.x - (draw_surface.get_size()[0] // 4),
                        gameobject_position.y - (draw_surface.get_size()[1] // 4)
                    ),

                    "World" : (
                        (gameobject_position[0] - camera_position[0]) + camera_anchor[0],
                        (gameobject_position[1] - camera_position[1]) + camera_anchor[1]
                    )
                } 

                if render_data.transform_type == {"Canvas":"RectTransform", "World":"Transform"}[meta_layer]:
                    draw_position = position_dict[meta_layer]
                else:
                    continue

                camera_rect = pygame.Rect(
                    0+self.screen.get_width()//4,
                    0+self.screen.get_height()//4,
                    self.screen.get_width()//2,
                    self.screen.get_height()//2
                )
                camera_rect = pygame.Rect(
                    0,
                    0,
                    self.screen.get_width(),
                    self.screen.get_height()
                )

                other_gameobject_rect = pygame.Rect(
                    draw_position[0],
                    draw_position[1],
                    draw_surface.get_width(),
                    draw_surface.get_height()
                )
                
                if not camera_rect.colliderect(other_gameobject_rect):
                    continue
            
                screen = self._draw_gameobject(
                    screen,
                    draw_surface,
                    draw_position,  
                ) 

        return screen

    def _draw_gameobject(
            self, 
            screen,
            draw_surface: pygame.Surface, 
            draw_position: tuple[int,int]
        ):

        screen.blit(
            draw_surface,
            draw_position
        )

        return screen