import pygame, sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, TILE_SIZE, BLOCK_HEIGHT
from renderer import Renderer
from worlds import World
from blocks import soil_blocks, water_blocks

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MiniCraft-2.5D")
clock = pygame.time.Clock()

world = World()
renderer = Renderer(screen, world)
selected_block = 1
def point_in_polygon(px, py, poly):
    """Bir noktanın poligonun içinde olup olmadığını kontrol eder"""
    n = len(poly)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi + 1e-6) + xi):
            inside = not inside
        j = i
    return inside
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_1: selected_block=1
            elif event.key==pygame.K_2: selected_block=2
            elif event.key==pygame.K_3: selected_block=3
            elif event.key==pygame.K_4: selected_block=4
            elif event.key == pygame.K_5:
                selected_block = 5  # stone

            elif event.key==pygame.K_F1:
                world.save_map("map1")
            elif event.key==pygame.K_F2:
                world = World()  # yeni map
                renderer.world = world
            elif event.key==pygame.K_F3:
                name = input("Enter map name: ")
                world.load_map(name)

    if event.type == pygame.MOUSEBUTTONDOWN:

        mx, my = pygame.mouse.get_pos()

        clicked_block = None

        max_z = -1

        for x in range(world.size_x):

            for y in range(world.size_y):

                for z in reversed(range(world.size_z)):  # en üstten başla

                    if world.tile_map[x][y][z] != 0:

                        poly = renderer.get_screen_polygon(x, y, z)

                        if point_in_polygon(mx, my, poly):

                            if z > max_z:
                                clicked_block = (x, y, z)

                                max_z = z

                            break  # bu (x,y) için daha aşağıya bakma

        if clicked_block:

            x, y, z = clicked_block

            if event.button == 1:  # sol tık = ekle

                if z + 1 < world.size_z:
                    world.tile_map[x][y][z + 1] = selected_block

            elif event.button == 3:  # sağ tık = sil

                world.tile_map[x][y][z] = 0

    # Kamera ve su
    keys = pygame.key.get_pressed()
    world.update_camera(keys)
    world.update_water()

    # Çizim
    screen.fill(WHITE)
    renderer.render()
    pygame.display.flip()
    clock.tick(FPS)