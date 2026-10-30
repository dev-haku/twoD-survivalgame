from pygame import Vector2

from game.package.core.component import Component


class Transform(Component):

    def __init__(self, engine, scene, parent, kwargs):
        super().__init__(engine, scene, parent, kwargs)

        self._position: Vector2 = Vector2(0,0)
        self._scale: Vector2 = Vector2(1,1)
        self.layer: int = 0

    @property
    def position(self) -> Vector2 | None:
        return self._position
    
    @position.setter
    def position(self, value: tuple):
        self._position = Vector2(value[0], value[1])

    @property
    def scale(self) -> Vector2 | None:
        return self._scale
    
    @scale.setter
    def scale(self, value: tuple):
        self._scale = Vector2(
            max(0, value[0]),
            max(0, value[1])
        )

    
class RectTransform(Component):

    def __init__(self, engine, scene, parent, kwargs):
        super().__init__(engine, scene, parent, kwargs)

        self._position: Vector2 = Vector2(0,0)
        self._scale: Vector2 = Vector2(1,1)
        self.layer: int = 0
        self.pos_ratio = (0,0)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: tuple):
        self.pos_ratio = (
            max(0.0, min(1.0, value[0])), 
            max(0.0, min(1.0, value[1]))
        )  

    @property
    def scale(self) -> Vector2 | None:
        return self._scale
        
    @scale.setter
    def scale(self, value: tuple):
        self._scale = Vector2(
            max(0, value[0]),
            max(0, value[1])
        )
        
    def update(self):
        screen_size = self.scene.screen.get_size()

        self._position = Vector2(
            screen_size[0] * self.pos_ratio[0],
            screen_size[1] * self.pos_ratio[1]
        )

        return super().update()