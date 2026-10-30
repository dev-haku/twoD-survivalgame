import pygame

from game.package.core.gameobject import Gameobject
from game.package.components.transform import RectTransform
from game.package.components.sprite_renderer import SpriteRenderer


class Text(Gameobject):
    def __init__(self, engine, scene, kwargs):
        super().__init__(engine, scene, kwargs)

        position: tuple[int, int] = kwargs["position"]
        scale: float = kwargs["scale"]
        layer: int = kwargs["layer"]
        text: str = kwargs["text"]
        size: tuple[int, int] = kwargs["size"]
        color: tuple[int, int, int] = kwargs["color"]
        init_active: bool = kwargs["init_active"]

        self.active = init_active

        transform = self.add_component(RectTransform)
        transform.position = position
        transform.scale = scale
        transform.layer = layer
    
        self.font = pygame.font.SysFont(None, size)
        self.text: str = str(text) or "None"
        self.color: tuple[int,int,int] = color or (255,255,255)

        self.add_component(
            component_class= SpriteRenderer, 
            surface= self._get_text_surface()
        )

        self.flag = True

        self.dt = self.engine.delta_time
    
    def update(self):
        if self.flag == True:
            self.get_component("SpriteRenderer").set_surface(self._get_text_surface())
            self.flag = False

        return super().update()

    def set_text(self, text: str):
        self.text = str(text)
        self.flag = True

    def set_color(self, color: tuple[int,int,int]):
        self.color = tuple(color)
        self.flag = True

    def _get_text_surface(self) -> pygame.Surface:
        return self.font.render(self.text, True, self.color)
        