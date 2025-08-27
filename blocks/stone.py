import random

stone_blocks = {}  # (x,y,z) -> renk

class Stone:
    block_id = 5  # config'deki ID

    @staticmethod
    def create(x, y, z):
        stone_blocks[(x, y, z)] = (
            random.randint(90, 120),
            random.randint(90, 120),
            random.randint(90, 120)
        )
        return Stone.block_id
