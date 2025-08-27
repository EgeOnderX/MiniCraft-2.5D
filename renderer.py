import pygame
from config import TILE_SIZE, BLOCK_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCKS
from blocks import soil_blocks
from worlds import World

class Renderer:
    def __init__(self, screen, world: World):
        self.screen = screen
        self.world = world

    def get_screen_polygon(self, x, y, z):
        iso_size = TILE_SIZE
        offset_y = z * BLOCK_HEIGHT

        cx = (x - y) * iso_size // 2 - self.world.camera_x + SCREEN_WIDTH // 2
        cy = (x + y) * iso_size // 4 - self.world.camera_y + SCREEN_HEIGHT // 2 - offset_y

        # üst yüz poligonu
        return [
            (cx, cy),
            (cx + iso_size // 2, cy + iso_size // 4),
            (cx, cy + iso_size // 2),
            (cx - iso_size // 2, cy + iso_size // 4)
        ]
    def render(self):
        for z in range(self.world.size_z):
            for y in range(self.world.size_y):
                for x in range(self.world.size_x):
                    block = self.world.tile_map[x][y][z]
                    if block != 0:
                        self.draw_cube(x, y, z, block)

    def draw_cube(self, x, y, z, block):
        color = BLOCKS[block] if block != 4 else soil_blocks.get((x, y, z), BLOCKS[4])
        iso_size = TILE_SIZE
        offset_y = z * BLOCK_HEIGHT

        cx = (x - y) * iso_size // 2 - self.world.camera_x + SCREEN_WIDTH // 2
        cy = (x + y) * iso_size // 4 - self.world.camera_y + SCREEN_HEIGHT // 2 - offset_y

        # üst yüz
        pygame.draw.polygon(self.screen, color, [
            (cx, cy),
            (cx + iso_size // 2, cy + iso_size // 4),
            (cx, cy + iso_size // 2),
            (cx - iso_size // 2, cy + iso_size // 4)
        ])

        # sol yüz
        left_color = (max(color[0] - 30, 0), max(color[1] - 30, 0), max(color[2] - 30, 0))
        pygame.draw.polygon(self.screen, left_color, [
            (cx - iso_size // 2, cy + iso_size // 4),
            (cx, cy + iso_size // 2),
            (cx, cy + iso_size // 2 + BLOCK_HEIGHT),
            (cx - iso_size // 2, cy + iso_size // 4 + BLOCK_HEIGHT)
        ])

        # sağ yüz
        right_color = (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0))
        pygame.draw.polygon(self.screen, right_color, [
            (cx + iso_size // 2, cy + iso_size // 4),
            (cx, cy + iso_size // 2),
            (cx, cy + iso_size // 2 + BLOCK_HEIGHT),
            (cx + iso_size // 2, cy + iso_size // 4 + BLOCK_HEIGHT)
        ])

        # kenar çizgisi
        pygame.draw.polygon(self.screen, (0, 0, 0), [
            (cx, cy),
            (cx + iso_size // 2, cy + iso_size // 4),
            (cx, cy + iso_size // 2),
            (cx - iso_size // 2, cy + iso_size // 4)
        ], 1)

        # --- Ağaç kütüğü çizgileri (4 yan yüz + 4 adet yatay çizgi) ---
        if block == 1:
            # sol yüz çizgileri
            for i in range(1, 5):
                y_offset = i * BLOCK_HEIGHT // 5
                pygame.draw.line(
                    self.screen,
                    (100, 50, 0),
                    (cx - iso_size // 2, cy + iso_size // 4 + y_offset),
                    (cx, cy + iso_size // 2 + y_offset),
                    1
                )
            # sağ yüz çizgileri
            for i in range(1, 5):
                y_offset = i * BLOCK_HEIGHT // 5
                pygame.draw.line(
                    self.screen,
                    (100, 50, 0),
                    (cx + iso_size // 2, cy + iso_size // 4 + y_offset),
                    (cx, cy + iso_size // 2 + y_offset),
                    1
                )
            # ön yüz çizgileri
            for i in range(1, 5):
                y_offset = i * BLOCK_HEIGHT // 5
                pygame.draw.line(
                    self.screen,
                    (100, 50, 0),
                    (cx - iso_size // 2, cy + iso_size // 4 + y_offset),
                    (cx + iso_size // 2, cy + iso_size // 4 + y_offset),
                    1
                )
            # arka yüz çizgileri
            for i in range(1, 5):
                y_offset = i * BLOCK_HEIGHT // 5
                pygame.draw.line(
                    self.screen,
                    (100, 50, 0),
                    (cx - iso_size // 4, cy + iso_size // 8 + y_offset),
                    (cx + iso_size // 4, cy + iso_size // 8 + y_offset),
                    1
                )
