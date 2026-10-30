import pygame

from game.assets.data.thing_defs import THING_DEFS, ThingIDs

from game.package import Scene
from ..gameobjects.world import World
from game.app.gameobjects.ui import PositionDisplay, ChunkPositionDisplay


class GameScene(Scene):

    def __init__(self, engine):
        super().__init__(engine)

        self.surface_cache: dict[str, pygame.Surface] = {}

        camera = self.get_gameobject("Camera1")
        camera.anchor = (0.5,0.5)
        camera.zoom(1)

        self.add_gameobject(
            gameobject_class= PositionDisplay, 
            position= (0.5,0.1), 
            scale=( 0.5,0.5), 
            layer= 1, 
            text= None, 
            size=100, 
            color= (255,255,255), 
            init_active= True
        )

        self.add_gameobject(
            gameobject_class= ChunkPositionDisplay, 
            position= (0.5,0.2), 
            scale= (0.5,0.5), 
            layer=1, 
            text=None,
            size= 100, 
            color= (255,255,255), 
            init_active= True
        )
        
        self.add_gameobject(World)

    def get_surface(self, ID: ThingIDs):
        surf = self.surface_cache.get(ID, None)
        if surf is None:
            thing_def = THING_DEFS.get(ID)
            entity_def = thing_def.entity_def
            sprite_surface = entity_def.sprite.build_surface()
            gameobject_scale = entity_def.gameobject_class.SCALE
            surf = pygame.transform.scale(sprite_surface, (sprite_surface.get_width() * gameobject_scale, sprite_surface.get_height() * gameobject_scale))
            self.surface_cache[ID] = surf
    
        return surf