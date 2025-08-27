import random
from blocks import soil_blocks

class Soil:
    block_id = 4

    @staticmethod
    def create(x, y, z):
        soil_blocks[(x, y, z)] = (
            random.randint(139,160),
            random.randint(69,100),
            random.randint(19,60)
        )
        return Soil.block_id
