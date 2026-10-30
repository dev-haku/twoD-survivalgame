import pygame

from game.package import (
    Gameobject,
    SimpleSpriteRenderer,
    Collider
)



class DropItem(Gameobject):
    
    SCALE = 2

    def __init__(self, engine, scene, kwargs):
        super().__init__(engine, scene, kwargs)
        pass

