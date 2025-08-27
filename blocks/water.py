from blocks import water_blocks

class Water:
    block_id = 3


def spawn_pond(tile_map, water_blocks, x, y, width=3, height=3):
    if width == 3 and height == 3:
        return
    """Kare göl spawn, tek blok yüksekliğinde, toprağın hemen altında"""
    max_x = len(tile_map)
    max_y = len(tile_map[0])
    max_z = len(tile_map[0][0])

    # Eğer gölün tamamı kenarlara 2 bloktan yakınsa göl spawn etmeyi iptal et
    if (x - width // 2 < 2 or
        y - height // 2 < 2 or
        x + width // 2 >= max_x - 2 or
        y + height // 2 >= max_y - 2):
        return  # Kenara çok yakınsa göl oluşmaz

    for dx in range(-(width // 2), width // 2 + 1):
        for dy in range(-(height // 2), height // 2 + 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < max_x and 0 <= ny < max_y:
                # Toprağın üstündeki ilk dolu bloğu bul
                for z in reversed(range(1, max_z)):
                    if tile_map[nx][ny][z-1] != 0 and tile_map[nx][ny][z] == 0:
                        # Gölü toprağın bir bloğunun altına koy
                        tile_map[nx][ny][z-1] = Water.block_id
                        water_blocks.add((nx, ny, z-1))
                        break
