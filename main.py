import pygame, sys, random

# --- Ayarlar ---
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
TILE_SIZE = 32
MAP_SIZE_X = 32
MAP_SIZE_Y = 32
MAP_SIZE_Z = 32
FPS = 60
BLOCK_HEIGHT = 16
CAMERA_SPEED = 8  # ekran kaydırma hızı

# --- Pygame başlat ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2.5D Sandbox 16x16x16")
clock = pygame.time.Clock()

# --- Renkler ---
WHITE  = (255,255,255)
BROWN  = (139,69,19)
GREEN  = (34,139,34)
BLUE   = (0,0,255)

def random_soil_color():
    r = random.randint(139,160)
    g = random.randint(69,100)
    b = random.randint(19,60)
    return (r,g,b)

# --- Blok sözlüğü ---
BLOCKS = {1:BROWN, 2:GREEN, 3:BLUE}  # diğerleri sabit
soil_blocks = {}  # (x,y,z) -> renk
water_blocks = set()  # su için aktif bloklar

# --- Harita ---
tile_map = [[[0 for _ in range(MAP_SIZE_Z)] for _ in range(MAP_SIZE_Y)] for _ in range(MAP_SIZE_X)]

# --- Başlangıç tabanı ---
for x in range(MAP_SIZE_X):
    for y in range(MAP_SIZE_Y):
        tile_map[x][y][0] = 4
        soil_blocks[(x,y,0)] = random_soil_color()

# --- Tree spawn ---
tree_x = random.randint(2, MAP_SIZE_X-3)
tree_y = random.randint(2, MAP_SIZE_Y-3)
for z in range(1,4):
    tile_map[tree_x][tree_y][z] = 1
for dx in range(-1,2):
    for dy in range(-1,2):
        for dz in range(4,6):
            tx, ty, tz = tree_x+dx, tree_y+dy, dz
            if 0<=tx<MAP_SIZE_X and 0<=ty<MAP_SIZE_Y and tz<MAP_SIZE_Z:
                tile_map[tx][ty][tz]=2

selected_block = 1

# --- Kamera kaydırma ---
camera_x, camera_y = 0, 0

# --- Çizim fonksiyonu ---
def draw_cube(x, y, z, block):
    color = BLOCKS[block] if block!=4 else soil_blocks[(x,y,z)]
    iso_size = TILE_SIZE
    offset_y = z*BLOCK_HEIGHT

    # ekran kaydırma offseti uygula
    cx = (x - y) * iso_size // 2 - camera_x + SCREEN_WIDTH//2
    cy = (x + y) * iso_size // 4 - camera_y + SCREEN_HEIGHT//2 - offset_y

    # üst yüz
    pygame.draw.polygon(screen, color, [
        (cx, cy),
        (cx+iso_size//2, cy+iso_size//4),
        (cx, cy+iso_size//2),
        (cx-iso_size//2, cy+iso_size//4)
    ])
    # sol
    pygame.draw.polygon(screen, (max(color[0]-30,0), max(color[1]-30,0), max(color[2]-30,0)), [
        (cx-iso_size//2, cy+iso_size//4),
        (cx, cy+iso_size//2),
        (cx, cy+iso_size//2 + BLOCK_HEIGHT),
        (cx-iso_size//2, cy+iso_size//4 + BLOCK_HEIGHT)
    ])
    # sağ
    pygame.draw.polygon(screen, (max(color[0]-50,0), max(color[1]-50,0), max(color[2]-50,0)), [
        (cx+iso_size//2, cy+iso_size//4),
        (cx, cy+iso_size//2),
        (cx, cy+iso_size//2 + BLOCK_HEIGHT),
        (cx+iso_size//2, cy+iso_size//4 + BLOCK_HEIGHT)
    ])
    # kenar
    pygame.draw.polygon(screen, (0,0,0), [
        (cx, cy),
        (cx+iso_size//2, cy+iso_size//4),
        (cx, cy+iso_size//2),
        (cx-iso_size//2, cy+iso_size//4)
    ],1)

# --- Su mekaniği ---
def update_water():
    moves = []
    for x,y,z in list(water_blocks):
        if z>0 and tile_map[x][y][z-1]==0:
            moves.append((x,y,z,z-1))
        else:
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx,ny = x+dx, y+dy
                if 0<=nx<MAP_SIZE_X and 0<=ny<MAP_SIZE_Y:
                    nz=0
                    while nz<MAP_SIZE_Z and tile_map[nx][ny][nz]!=0:
                        nz+=1
                    if nz<MAP_SIZE_Z and nz<z:
                        moves.append((x,y,z,nz))
    for x,y,z1,z2 in moves:
        tile_map[x][y][z1]=0
        tile_map[x][y][z2]=3
        water_blocks.discard((x,y,z1))
        water_blocks.add((x,y,z2))

# --- Oyun döngüsü ---
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_1: selected_block=1
            elif event.key==pygame.K_2: selected_block=2
            elif event.key==pygame.K_3: selected_block=3
            elif event.key==pygame.K_4: selected_block=4
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()
            clicked = False
            for x in range(MAP_SIZE_X):
                for y in range(MAP_SIZE_Y):
                    # en üstteki blok
                    for z in reversed(range(MAP_SIZE_Z)):
                        if tile_map[x][y][z]!=0:
                            top_z=z
                            break
                    else:
                        top_z=-1
                    if top_z==-1: continue

                    cx = (x - y) * TILE_SIZE //2 - camera_x + SCREEN_WIDTH//2
                    cy = (x + y) * TILE_SIZE //4 - camera_y + SCREEN_HEIGHT//2 - top_z*BLOCK_HEIGHT
                    bbox = pygame.Rect(cx-TILE_SIZE//2, cy, TILE_SIZE, TILE_SIZE//2)
                    if bbox.collidepoint(mx,my):
                        clicked=True
                        if event.button==1:  # ekle
                            if top_z+1<MAP_SIZE_Z:
                                tile_map[x][y][top_z+1]=selected_block
                                if selected_block==3:
                                    water_blocks.add((x,y,top_z+1))
                                elif selected_block==4:
                                    soil_blocks[(x,y,top_z+1)] = random_soil_color()
                        elif event.button==3:  # sil
                            if tile_map[x][y][top_z]==3:
                                water_blocks.discard((x,y,top_z))
                            tile_map[x][y][top_z]=0
                        break
                if clicked: break

    # WASD ile kamera kaydırma
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        camera_y -= CAMERA_SPEED
    if keys[pygame.K_s]:
        camera_y += CAMERA_SPEED
    if keys[pygame.K_a]:
        camera_x -= CAMERA_SPEED
    if keys[pygame.K_d]:
        camera_x += CAMERA_SPEED

    # su mekaniği
    update_water()

    # çizim
    screen.fill(WHITE)
    for z in range(MAP_SIZE_Z):
        for y in range(MAP_SIZE_Y):
            for x in range(MAP_SIZE_X):
                block = tile_map[x][y][z]
                if block!=0:
                    draw_cube(x,y,z,block)

    pygame.display.flip()
    clock.tick(FPS)
