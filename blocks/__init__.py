# blocks/__init__.py
soil_blocks = {}    # (x,y,z) -> renk
water_blocks = set()  # su blokları
stone_blocks = {}
# Bloklar import edilir
from .soil import Soil
from .water import Water
from .tree import Tree
from .stone import Stone, stone_blocks
