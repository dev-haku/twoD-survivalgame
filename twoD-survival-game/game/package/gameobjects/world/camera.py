import pygame

from game.package.core.gameobject import Gameobject
from game.package.components.transform import Transform


class Camera(Gameobject):
    
    def __init__(self, engine, scene, kwargs):
        super().__init__(engine, scene, kwargs)

        self.tags.append("camera")
        self.add_component(Transform)
        self._anchor = pygame.Vector2()
        self.pos_ratio: tuple = (0,0)

    @property
    def anchor(self) -> pygame.Vector2:
        return self._anchor

    @anchor.setter
    def anchor(self, value: tuple[float, float]):
        self.pos_ratio = (
            max(0.0, min(1.0, value[0])), 
            max(0.0, min(1.0, value[1]))
        )  

    def update(self):
        screen_size = self.scene.screen.get_size()

        self._anchor = pygame.Vector2(
            screen_size[0] * self.pos_ratio[0],
            screen_size[1] * self.pos_ratio[1]
        )

        return super().update()

    def zoom(self, value: int):
        if value is not 0:
            w, h = self.scene.screen.get_size()
            self.scene.screen = pygame.transform.scale(self.scene.screen, (w // value, h // value))
