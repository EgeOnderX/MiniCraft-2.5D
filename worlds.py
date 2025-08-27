import random, json, os
import pygame
from blocks import soil_blocks, water_blocks
from blocks.tree import Tree
from blocks.water import spawn_pond
from config import WORLD_SIZE_X, WORLD_SIZE_Y, WORLD_SIZE_Z
from blocks.soil import Soil
from blocks.stone import stone_blocks

class World:
    def __init__(self, size_x=WORLD_SIZE_X, size_y=WORLD_SIZE_Y, size_z=WORLD_SIZE_Z):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.tile_map = [[[0 for _ in range(size_z)] for _ in range(size_y)] for _ in range(size_x)]
        self.camera_x = 0
        self.camera_y = 0
        self.occupied_by_trees = set()
        self.generate_base()

    def generate_base(self):
        """Zemin, taş, ağaç ve göl tabanını oluştur"""
        for x in range(self.size_x):
            for y in range(self.size_y):
                # Taş katmanları (0–3)
                for z in range(4):
                    self.tile_map[x][y][z] = 5  # taş
                # Dirt katmanı (4)
                self.tile_map[x][y][4] = 4
                Soil.create(x, y, 4)

        area = self.size_x * self.size_y
        tree_count = area // 128
        big_tree_every = 512
        possible_ponds = area // 256
        pond_count = sum(1 for _ in range(possible_ponds) if random.random() < 0.5)

        tree_placed = 0
        for _ in range(tree_count):
            for _ in range(50):
                tx = random.randint(2, self.size_x - 3)
                ty = random.randint(2, self.size_y - 3)

                occupied = any((tx, ty, z) in self.occupied_by_trees for z in range(self.size_z))
                if not occupied:
                    # Eğer tree_placed % big_tree_every == 0 ise büyük ağaç
                    big = (tree_placed % big_tree_every == 0)
                    Tree.spawn(self.tile_map, tx, ty, big=big)

                    for z in range(self.size_z):
                        self.occupied_by_trees.add((tx, ty, z))
                    tree_placed += 1
                    break

        # Gölleri ekle
        for _ in range(pond_count):
            px = random.randint(2, self.size_x - 3)
            py = random.randint(2, self.size_y - 3)
            spawn_pond(
                self.tile_map,
                water_blocks,
                px,
                py,
                width=random.randint(2, 4),
                height=random.randint(2, 4)
            )
    def update_water(self):
        moves = []
        for x, y, z in list(water_blocks):
            # önce aşağı
            if z > 0 and self.tile_map[x][y][z - 1] == 0:
                moves.append((x, y, z, z - 1))
            else:
                # yanlara akış
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size_x and 0 <= ny < self.size_y:
                        nz = 0
                        while nz < self.size_z and self.tile_map[nx][ny][nz] != 0:
                            nz += 1
                        if nz < self.size_z and nz < z:  # daha aşağıya akabilir
                            moves.append((x, y, z, nz))
                # çapraz yayılma (opsiyonel)
                for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size_x and 0 <= ny < self.size_y:
                        nz = 0
                        while nz < self.size_z and self.tile_map[nx][ny][nz] != 0:
                            nz += 1
                        if nz < self.size_z and nz < z:
                            moves.append((x, y, z, nz))
        # hareketi uygula
        for x, y, z1, z2 in moves:
            self.tile_map[x][y][z1] = 0
            self.tile_map[x][y][z2] = 3
            water_blocks.discard((x, y, z1))
            water_blocks.add((x, y, z2))

        for x,y,z1,z2 in moves:
            self.tile_map[x][y][z1] = 0
            self.tile_map[x][y][z2] = 3
            water_blocks.discard((x,y,z1))
            water_blocks.add((x,y,z2))

    # World içine ekle
    def place_block(self, x, y, z, block_id):
        """Player herhangi bir bloğu koyabilir ve ilgili sözlüğü günceller"""
        if 0 <= x < self.size_x and 0 <= y < self.size_y and 0 <= z < self.size_z:
            self.tile_map[x][y][z] = block_id

            # Blok tipine göre sözlüğü güncelle
            if block_id == 4:  # Soil
                from blocks.soil import Soil
                Soil.create(x, y, z)
            elif block_id == 5:  # Stone
                from blocks.stone import Stone
                Stone.create(x, y, z)
            elif block_id == 3:  # Su
                from blocks import water_blocks
                water_blocks.add((x, y, z))
            # Diğer bloklar eklenebilir

            return True
        return False
    def update_camera(self, keys):
        from config import CAMERA_SPEED
        if keys[pygame.K_w]: self.camera_y -= CAMERA_SPEED
        if keys[pygame.K_s]: self.camera_y += CAMERA_SPEED
        if keys[pygame.K_a]: self.camera_x -= CAMERA_SPEED
        if keys[pygame.K_d]: self.camera_x += CAMERA_SPEED

    def save_map(self, name="map1"):
        data = {"tile_map": self.tile_map, "soil_blocks": {str(k):v for k,v in soil_blocks.items()}}
        with open(f"{name}.json", "w") as f:
            json.dump(data, f)
        print(f"Map saved as {name}.json")

    def load_map(self, name):
        if not os.path.exists(f"{name}.json"):
            print("Map file not found!")
            return
        with open(f"{name}.json", "r") as f:
            data = json.load(f)
        self.tile_map = data["tile_map"]
        soil_blocks.clear()
        for k,v in data["soil_blocks"].items():
            x,y,z = eval(k)
            soil_blocks[(x,y,z)] = tuple(v)
        water_blocks.clear()
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    if self.tile_map[x][y][z]==3:
                        water_blocks.add((x,y,z))
        print(f"Map {name}.json loaded")
