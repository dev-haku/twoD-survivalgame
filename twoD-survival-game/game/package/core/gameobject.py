from __future__ import annotations
from typing import TYPE_CHECKING
import time
import sys

from game.package.core.component import Component

if TYPE_CHECKING:
    from game.package.core.engine import Engine
    from game.package.core.scene import Scene


class Gameobject:
    
    def __init__(self, engine: Engine, scene: Scene, kwargs: dict) -> None:
        self.id: str = None
        self.active: bool = True
        self.is_started: bool = False
        self.tags: list[str] = []

        self.parent = None
        self.children:dict[str, Gameobject] = {}
        self.components: dict[str, Component] = {}
        
        self.created_timestamp: float = time.time()

        self.engine: Engine = engine
        self.scene: Scene = scene

    def update(self):
        pass

    def add_child(self, name: str, child_gameobject):
        child_gameobject.parent = self
        self.children[name] = id(child_gameobject)

    def get_child(self, target_name: str):
        for name, _id in self.children.items():
            if name == target_name:
                return self.engine.current_scene.get_worldobject(_id)
        return None
    
    def add_component(self, component_class: type[Component], **kwargs: dict) -> Component:

        comp = component_class(self.engine, self.scene, self, kwargs)
        if self.engine is None:
            print(f"{self.__class__.__name__}の self.engineがNoneで{comp.__class__.__name__}に代入できなかった",file=sys.stderr)
        self.components[comp.__class__.__name__] = comp

        return comp

    def remove_component(self, target_name):
        for name in self.components.keys():
            if name == target_name:
                del self.component[name]

    def get_component(self, target_name: str) -> Component | None:
        for name, comp in self.components.items():
            if name == target_name:
                return comp
        return None
    
    def destroy(self):
        for gameobject in self.scene.gameobjects:
            if self == gameobject:
                self.scene.gameobjects.remove(gameobject)
                return