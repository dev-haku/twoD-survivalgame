from game.package import (
    Scene,
    Text
)

class TitleScene(Scene):

    def __init__(self, engine):
        super().__init__(engine)

        self.add_gameobject(
            gameobject_class= Text, 
            position= (0.5,0.35), 
            scale=(0.5,0.5), 
            layer= 1, 
            text= "TwoD Survival Game", 
            size=150,
            color=(255,255,255),
            init_active= True
        )

        self.add_gameobject(
            gameobject_class= Text, 
            position= (0.5,0.7), 
            scale= (0.25,0.25), 
            layer= 1, 
            text= "Press the Enter key to start the game",
            size= 100, 
            color= (255,255,255),
            init_active= True
        )

    def update(self):
        
        keys = self.engine.input_status.keys

        if keys.get("escape", False):
            self.engine.shutdown()

        if keys.get("return", False):
            self.engine.change_scene(1)

        return super().update()