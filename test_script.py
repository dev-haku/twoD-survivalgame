import json
import pygame

class ItemData:
    def __init__(self, target_item_id):
        with open("./items_data.json", "r") as f:
            self.items_data = json.load(f)

        self.id = target_item_id
        self.sprite = self.get_item_sprite()
        self.parameter = self.get_item_parameter()

    def get_item_sprite(self):
        for d in self.items_data["sprites"]:
            if d["id"] == self.id:
                return d
    
    def get_item_parameter(self):
        for d in self.items_data["parameters"]:
            if d["id"] == self.id:
                return d

class DropItem:
    def __init__(self, item_data):
        self.id = item_data.id
        sprite_data = item_data.sprite

        sprite_sheet_surface = pygame.image.load(sprite_data["sprite_sheet_image_path"])
        rect = pygame.Rect(
            sprite_data["offset"]["x"],
            sprite_data["offset"]["y"],
            sprite_data["size"]["width"],
            sprite_data["size"]["height"]
        )
        self.surface = sprite_sheet_surface.subsurface(rect).copy()


item_data = ItemData(target_item_id="apple")
item = DropItem(item_data)
print(item.surface)

