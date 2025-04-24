import pygame

# Cấu hình
GRID_SIZE = 10
CELL_SIZE = 40
MARGIN = 20
BOARD_WIDTH = GRID_SIZE * CELL_SIZE
WIDTH = BOARD_WIDTH * 2 + MARGIN * 3
HEIGHT = GRID_SIZE * CELL_SIZE + MARGIN * 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Ship - 2 Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

font = pygame.font.SysFont("Arial", 22)

# Load hình ảnh và âm thanh
ship_img = pygame.image.load("tau_ngam.png")
ship_img = pygame.transform.scale(ship_img, (CELL_SIZE, CELL_SIZE))
explosion_img = pygame.image.load("lua2.png")
explosion_img = pygame.transform.scale(explosion_img, (CELL_SIZE, CELL_SIZE))
cursor_img = pygame.image.load("ngom.png")
cursor_img = pygame.transform.scale(cursor_img, (30, 30))

pygame.mixer.init()
hit_sound = pygame.mixer.Sound("no.mp3") # Âm thanh khi bắn trúng tàu 
miss_sound = pygame.mixer.Sound("truot.mp3") # Âm thanh khi bắn trượt 

# Ẩn con trỏ mặc định
pygame.mouse.set_visible(False)

# Tạo lưới
def create_grid():
    grid = [] 
    for _ in range(GRID_SIZE):  
        row = []  
        for _ in range(GRID_SIZE):  
            row.append("~")  
        grid.append(row)  
    return grid 

# Khởi tạo
grids = [create_grid(), create_grid()]


# Vòng lặp chính
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
