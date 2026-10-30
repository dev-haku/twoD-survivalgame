from dataclasses import dataclass
from enum import StrEnum, Enum
import pathlib
import pygame
import warnings

from game.paths import ASSET_DIR
from game.package.core.gameobject import Gameobject
from game.app.gameobjects.tile import Tile
from game.app.gameobjects.prop import Prop
from game.app.gameobjects.drop_item import DropItem


class ThingIDs(StrEnum):

    WATER_TILE = "water_tile"
    STONE_TILE  = "stone_tile"
    SAND_TILE  = "sand_tile"
    GRASS_TILE  = "grass_tile"
    TUNDRA_TILE = "tundra_tile"
    STEPPE_TILE = "steppe_tile"

    TREE = "tree"
    ROCK = "rock"
    TORCH = "torch"
    CHEST = "chest"

    SLASH_EFFECT = "slash_effect"
    DAMAGE_EFFECT = "damage_effect"
    FIREBALL_EFFECT = "fireball_effect"

    APPLE = "apple"
    WOOD = "wood"
    STONE = "stone"
    WOOD_SWORD = "wood_sword"


TILE_SIZE = 16
ITEM_SIZE = 10

class SheetType(StrEnum):
    TILE = "tile"
    ITEM = "item"
    PROP = "prop"
    EFFECT = "effect"

SHEETPATHS: dict[SheetType, pathlib.Path] = {
    SheetType.TILE : ASSET_DIR / "image" / "sprite_sheet" / "tiles.png",
    SheetType.ITEM : ASSET_DIR / "image" / "sprite_sheet" / "items.png",
    SheetType.PROP : ASSET_DIR / "image" / "sprite_sheet" / "props.png",
    SheetType.EFFECT : ASSET_DIR / "image" / "sprite_sheet" / "effects.png"
}

@dataclass(frozen=True)
class Sprite:
    sheet_path: pathlib.Path
    x: int
    y: int
    w: int
    h: int

    def get_source_sheet(self) -> pygame.Surface:
        return pygame.image.load(self.sheet_path)
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def build_surface(self):
        return self.get_source_sheet().subsurface(self.get_rect())


class EffectType(StrEnum):
    HEALTH = "health"
    DAMAGE = "damage"

@dataclass(frozen=True)
class Effect:
    type: EffectType
    amount: int

    @classmethod
    def damage(cls, amount: int) -> "Effect":
        return cls(EffectType.DAMAGE, amount)

    @classmethod
    def health(cls, amount: int) -> "Effect":
        return cls(EffectType.HEALTH, amount)
    
class ActionType(StrEnum):
    ATTACK = "attack"
    EAT = "eat"

@dataclass(frozen=True)
class Action:
    type: ActionType
    effects: tuple[Effect, ...] = ()

    @classmethod
    def eat(cls, *effects: Effect) -> "Action":
        return cls(ActionType.EAT, effects)

    @classmethod
    def attack(cls, *effects: Effect) -> "Action":
        return cls(ActionType.ATTACK, effects)

@dataclass(frozen=True)
class ItemDef:
    sprite: Sprite
    action: Action | None = None


@dataclass(frozen=True)
class DropItem:
    thingID: ThingIDs
    max_drop_count: int
    drop_rate: float

    def __post_init__(self):
        if not (0.0 <= self.drop_rate <= 1.0):
            raise ValueError(f"drop_rate は 0.0〜1.0 が必要です: {self.drop_rate}")
        if self.max_drop_count < 0:
                    raise ValueError(f"max_drop_count は0以上が必要です: {self.max_drop_count}")

@dataclass(frozen=True)
class DropItems:
    
    drop_items: tuple[DropItem, ...]

    @classmethod
    def of(cls,*drop_items: DropItem) -> "DropItems":
        return cls(drop_items)


@dataclass(frozen=True)
class EntityStats:
    max_health: int = 0
    drop_items: DropItems = DropItems.of()

@dataclass(frozen=True)
class EntityState:
    is_attackable: bool = False
    is_flammable: bool = False

@dataclass(frozen=True)
class EntityDef:
    gameobject_class: type[Gameobject]
    sprite: Sprite
    stats: EntityStats = EntityStats()
    state: EntityState = EntityState()

    def __post_init__(self):
        if not (isinstance(self.gameobject_class, type) and issubclass(self.gameobject_class, Gameobject)):
            raise TypeError(f"Gameobjectのクラスが必要です: {self.gameobject_class!r}")

        if not isinstance(self.sprite, Sprite):
            raise TypeError(f"Sprite が必要です: {self.sprite!r}")

        if not isinstance(self.stats, EntityStats):
            raise TypeError(f"EntityStats が必要です: {self.entity_stats!r}")

        if not isinstance(self.state, EntityState):
            raise TypeError(f"EntityState が必要です: {self.entity_state!r}")


@dataclass(frozen=True)
class ThingDef:
    entity_def: EntityDef | None = None
    item_def: ItemDef | None = None
    

THING_DEFS: dict[ThingIDs, ThingDef] = {
    ThingIDs.WATER_TILE : ThingDef(
        entity_def= EntityDef(
            gameobject_class=Tile, 
            sprite=Sprite(SHEETPATHS[SheetType.TILE], 16*2, 0, 16, 16)
        )
    ),
    ThingIDs.STONE_TILE : ThingDef(
        entity_def= EntityDef(
            gameobject_class=Tile, 
            sprite=Sprite(SHEETPATHS[SheetType.TILE], 16*1, 0, 16, 16)
        )
    ),
    ThingIDs.SAND_TILE : ThingDef(
        entity_def= EntityDef(
            gameobject_class=Tile, 
            sprite=Sprite(SHEETPATHS[SheetType.TILE], 16*3, 0, 16, 16)
        )
    ),
    ThingIDs.STEPPE_TILE : ThingDef(
        entity_def= EntityDef(
            gameobject_class=Tile, 
            sprite=Sprite(SHEETPATHS[SheetType.TILE], 16*4, 0, 16, 16)
        )
    ),
    ThingIDs.TUNDRA_TILE : ThingDef(
        entity_def= EntityDef(
            gameobject_class=Tile, 
            sprite=Sprite(SHEETPATHS[SheetType.TILE], 16*6, 0, 16, 16)

        )
    ),
    ThingIDs.GRASS_TILE : ThingDef(
        entity_def= EntityDef(
            gameobject_class=Tile, 
            sprite=Sprite(SHEETPATHS[SheetType.TILE], 0, 0, 16, 16),
        )
    ),

    ThingIDs.TREE : ThingDef(
        entity_def= EntityDef(
            gameobject_class=Prop, 
            sprite=Sprite(SHEETPATHS[SheetType.PROP], 0, 0, 16, 16),
            state=EntityState(
                is_attackable=True, 
                is_flammable=True
            ),
            stats=EntityStats(
                max_health=10, 
                drop_items=DropItems.of(
                    DropItem(thingID=ThingIDs.WOOD, max_drop_count=10, drop_rate=1.0),
                    DropItem(thingID=ThingIDs.APPLE, max_drop_count=3, drop_rate=0.1),
                )
            )
        )
    ),

    ThingIDs.ROCK : ThingDef(
        entity_def= EntityDef(
            gameobject_class=Prop, 
            sprite=Sprite(SHEETPATHS[SheetType.PROP], 16, 0, 16, 16),
            state=EntityState(
                is_attackable=True, 
                is_flammable=False
            ),
            stats=EntityStats(
                max_health=10, 
                drop_items=DropItems.of(
                    DropItem(thingID=ThingIDs.STONE, max_drop_count=10, drop_rate=1.0),
                )
            )
        )
    ),

    ThingIDs.APPLE : ThingDef(
        item_def= ItemDef(
            sprite=Sprite(SHEETPATHS[SheetType.ITEM], 0, 0, 16, 16),
            action= Action.eat(Effect.health(1))
        )
    ),

    ThingIDs.WOOD : ThingDef(
        item_def= ItemDef(
            sprite=Sprite(SHEETPATHS[SheetType.ITEM], 16*2, 0, 16, 16)
        )
    ),

    ThingIDs.STONE : ThingDef(
        item_def= ItemDef(
            sprite=Sprite(SHEETPATHS[SheetType.ITEM], 16*2, 0, 16, 16)
        )
    ),
    
    ThingIDs.WOOD_SWORD : ThingDef(
        item_def= ItemDef(
            sprite=Sprite(SHEETPATHS[SheetType.ITEM], 0, 16*3, 16, 16),
            action= Action.attack(Effect.damage(1))
        )
    ),

}


missing = set(ThingIDs) - set(THING_DEFS)
for m in missing:
    print(f"未定義のエンティティ : {m!r}")

def validate_thing_defs() -> None:
    for thing_id, thing_def in THING_DEFS.items():
        if thing_def.entity_def is None:
            continue
        for d in thing_def.entity_def.stats.drop_items.drop_items:
            target = THING_DEFS.get(d.thingID)
            if target is None:
                raise ValueError(f"{thing_id!r}: ドロップ先 {d.thingID!r} が THING_DEFS に存在しません")
            if target.item_def is None:
                raise ValueError(f"{thing_id!r}: {d.thingID!r} はitemのthingIDではありません")

validate_thing_defs()