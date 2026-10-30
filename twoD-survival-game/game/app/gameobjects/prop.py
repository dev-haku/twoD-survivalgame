from __future__ import annotations
import pygame

from game.package import (
    Gameobject,
    Transform,
    SpriteRenderer,
    SimpleSpriteRenderer,
    Collider
)


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.assets.data import thing_defs


class Prop(Gameobject):

    SCALE = 3
        
    def __init__(self, engine, scene, kwargs) -> None:
        super().__init__(engine, scene, kwargs)

        self.thing_id: thing_defs.ThingIDs = kwargs["thing_id"]

        transform: Transform = self.add_component(Transform)
        transform.position = kwargs["position"]
        transform.layer = kwargs["layer"]
        
        self.add_component(
            component_class= SimpleSpriteRenderer, 
            surface= kwargs["surface"]
        )

        collider: Collider = self.add_component(Collider)
        collider.add_hitbox((0,0),(16,16))


        entity_def: thing_defs.EntityDef = kwargs["entity_def"]
        
        self.max_health = entity_def.stats.max_health
        self.health = self.max_health

        self.drop_items = entity_def.stats.drop_items


    def _attacked(self, effects: tuple[thing_defs.Effect]):
        pass
