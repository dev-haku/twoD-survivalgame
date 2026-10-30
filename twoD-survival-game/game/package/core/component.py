from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.package.core.engine import Engine
    from game.package.core.scene import Scene
    from game.package.core.gameobject import Gameobject


class Component:
    
    def __init__(self, engine: Engine, scene: Scene, parent: Gameobject, kwargs: dict):
        self.active: bool = True
        self.tags: list[str] = []
        self.is_started: bool = False
    
        self.engine: Engine = engine
        self.scene: Scene = scene
        self.parent: Gameobject = parent

    def update(self):
        pass

    def add_tag(self, tag_name: str):
        self._tags.append(tag_name)

        