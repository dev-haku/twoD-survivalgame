from .core import Scene
from .core import Gameobject
from .core import Component


from .gameobjects.world.square import Square
from .gameobjects.ui import Image, Text

from .components.transform import Transform
from .components.transform import RectTransform
from .components.sprite_renderer import SpriteRenderer
from .components.sprite_renderer import SimpleSpriteRenderer
from .components.animator import Animator
from .components.collider import Collider
from .components.timer import Timer

print("loaded game package")