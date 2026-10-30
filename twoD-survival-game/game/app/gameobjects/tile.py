from game.package import (
    Gameobject,
    Transform,
    SimpleSpriteRenderer
)

    
class Tile(Gameobject):

    SCALE = 3
        
    def __init__(self, engine, scene, kwargs) -> None:
        super().__init__(engine, scene, kwargs)
        
        transform: Transform = self.add_component(Transform)
        transform.position = kwargs["position"]
        transform.layer = kwargs["layer"]

        self.add_component(
            component_class= SimpleSpriteRenderer, 
            surface= kwargs["surface"]
        )

    