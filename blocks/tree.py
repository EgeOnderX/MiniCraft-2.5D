class Tree:
    @staticmethod
    def spawn(tile_map, tree_x, tree_y, big=False):
        size_z = len(tile_map[0][0])

        # başlangıç z konumunu belirle (toplam blok yüksekliğini bul)
        base_z = 0
        for z in range(size_z):
            if tile_map[tree_x][tree_y][z] != 0:
                base_z = z + 1  # mevcut bloğun üstüne çık
        if big:
            trunk_height = 5
            leaf_start = base_z + trunk_height
            leaf_height = 3
            leaf_radius = 2
        else:
            trunk_height = 3
            leaf_start = base_z + trunk_height
            leaf_height = 2
            leaf_radius = 1

        # gövde
        for z in range(base_z, base_z + trunk_height):
            if z < size_z:
                tile_map[tree_x][tree_y][z] = 1

        # yaprak
        for dx in range(-leaf_radius, leaf_radius+1):
            for dy in range(-leaf_radius, leaf_radius+1):
                for dz in range(leaf_start, leaf_start + leaf_height):
                    tx, ty, tz = tree_x+dx, tree_y+dy, dz
                    if 0 <= tx < len(tile_map) and 0 <= ty < len(tile_map[0]) and tz < size_z:
                        tile_map[tx][ty][tz] = 2