SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
TILE_SIZE = 32
BLOCK_HEIGHT = 16
FPS = 60
CAMERA_SPEED = 8

WHITE  = (255,255,255)
BROWN  = (139,69,19)   # dirt
GREEN  = (34,139,34)
BLUE   = (0,0,255)
GRAY   = (100,100,100)  # taş rengi


# world

WORLD_SIZE_X = 45
WORLD_SIZE_Y = 45
WORLD_SIZE_Z = 16


BLOCKS = {
    1: BROWN,   # ağaç gövdesi
    2: GREEN,   # ağaç yaprak
    3: BLUE,    # su
    4: BROWN,   # soil/dirt
    5: GRAY     # taş
}