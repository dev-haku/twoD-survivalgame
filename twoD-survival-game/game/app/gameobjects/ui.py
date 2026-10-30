from game.package import Gameobject, Transform, RectTransform, Text


class PositionDisplay(Text):
    def __init__(self, engine, scene, kwargs):
        super().__init__(engine, scene, kwargs)

    def update(self):
        player = self.scene.get_gameobject("Player1")
        player_transform: Transform = player.get_component("Transform")

        self.set_text(f"{player_transform.position.x}|{player_transform.position.y}")

        return super().update()

class ChunkPositionDisplay(Text):
    def __init__(self, engine, scene, kwargs):
        super().__init__(engine, scene, kwargs)
    def update(self):
        world = self.scene.get_gameobject("World1")
        player_chunk_position = world._get_current_player_chunk_position()

        self.set_text(f"{player_chunk_position[0]}|{player_chunk_position[1]}")
        
        return super().update()

class HeartIcon(Gameobject):
    pass

class ItemSlot(Gameobject):
    pass 

class HealthBar(Gameobject):
    pass

class Hotbar(Gameobject):
    pass

class Toast(Gameobject):
    pass

class MessageWindow(Gameobject):
    pass

class Inventory(Gameobject):
    pass

class PauseMenu(Gameobject):
    pass

class SettingMenu(Gameobject):
    pass