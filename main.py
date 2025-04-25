import pygame
import random

# Cấu hình
GRID_SIZE = 10
CELL_SIZE = 40
MARGIN = 50
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

# hàm kiểm tra xem tàu mới định đặt có đè lên tàu cũ không
def is_overlapping(new_positions, existing_ships):
    for ship in existing_ships:
        for pos in ship["positions"]:
            for new_pos in new_positions:
                if new_pos == pos:
                    return True  # Trùng vị trí
    return False  # Không trùng

# Đặt tàu ngẫu nhiên
def place_ships():
    ship_sizes = [10]
    ships = []


    while len(ships) < len(ship_sizes):
        size = ship_sizes[len(ships)]
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        horizontal = random.choice([True, False]) # True: Đặt ngang, False: Đặt dọc. 

        positions = [] # lưu các tọa độ (row, col) mà tàu sẽ chiếm.
        valid = True # kiểm tra xem tàu có đặt hợp lệ không.

        for i in range(size):
            if horizontal:
                r = row         
                c = col + i     
            else:
                r = row + i     
                c = col   


            if r >= GRID_SIZE or c >= GRID_SIZE:
                valid = False
                break
            positions.append((r, c))

        if not valid:
            continue

        #  kiểm tra xem tàu mới định đặt có đè lên tàu cũ không   
        if is_overlapping(positions, ships):
            continue

        ships.append({ "positions": positions, "hit": [False]*size, "horizontal": horizontal })

    return ships

#  hàm kiểm tra xem người chơi đó đã thắng hay chưa, 
# tức là tất cả tàu của họ đã bị bắn trúng hết hay chưa.
def check_win(player):
    for ship in ships[player]:
        for hit in ship["hit"]:
            if not hit:
                return False
    return True


# Khởi tạo
grids = [create_grid(), create_grid()]
ships = [place_ships(), place_ships()]
current_player = 0
game_over = False
winner = None


#Vẽ lưới 
def draw_grid(player_index, offset_x):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = offset_x + col * CELL_SIZE
            y = MARGIN + row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

            cell_status = grids[player_index][row][col]
            if cell_status == "M":
                pygame.draw.circle(screen, BLUE, rect.center, 6)
            elif cell_status == "H":
                pygame.draw.circle(screen, RED, rect.center, 6)

# Vẽ tàu đã bị phá hủy
def draw_destroyed_ship(ship, offset_x):
    first_cell = ship["positions"][0]
    ship_length = len(ship["positions"])
    x = offset_x + first_cell[1] * CELL_SIZE
    y = MARGIN + first_cell[0] * CELL_SIZE

    if ship["horizontal"]:
        img = pygame.transform.scale(ship_img, (CELL_SIZE * ship_length, CELL_SIZE))
    else:
        img = pygame.transform.rotate(ship_img, -90)
        img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE * ship_length))

    screen.blit(img, (x, y))

    # Hiệu ứng nổ ở giữa tàu
    mid_index = ship_length // 2
    mid_row, mid_col = ship["positions"][mid_index]
    exp_x = offset_x + mid_col * CELL_SIZE
    exp_y = MARGIN + mid_row * CELL_SIZE
    screen.blit(explosion_img, (exp_x, exp_y))
      
#Vẽ tàu nếu đã được phá 
def draw_ships_if_destroyed(player_index, offset_x):
    for ship in ships[player_index]:
        if all(ship["hit"]):
            draw_destroyed_ship(ship, offset_x)

#Hiển thị lượt người chơi
def draw_current_turn_label():
    label = font.render(f"Player {current_player + 1}", True, BLACK)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT - 35))

#Vẽ bảng người chơi
def draw_player_boards():
    for player_index in [0, 1]:
        offset_x = MARGIN + player_index * (BOARD_WIDTH + MARGIN)
        draw_grid(player_index, offset_x)
        draw_ships_if_destroyed(player_index, offset_x)
        
#Hiển thị màn hình
def display():
    screen.fill(WHITE)
    draw_player_boards()
    draw_current_turn_label()
    if game_over:
        draw_winner_label()
    draw_custom_cursor()
    pygame.display.flip()
        
#Hiện thị người chơi thắng
def draw_winner_label():
    msg = font.render(f"Player {winner + 1} win!", True, GREEN)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 0))

#Hiển thị hình ảnh con trỏ mới    
def draw_custom_cursor():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(cursor_img, (mouse_x - 15, mouse_y - 15))

# Xử lý khi click
def handle_click (pos):
    #Tạo biến toàn cục
    global current_player, game_over, winner
    
    #Nếu game over thì kết thúc
    if(game_over): 
        return
    
    #Xác định đối thủ là 0 - 1
    opponent = 1 - current_player
    
    offset_x = MARGIN + opponent * (BOARD_WIDTH + MARGIN)
    
    #Chia vị trí click chuột thành 2 thành phần x và y 
    x,y = pos
    
    #Kiểm tra xem có click vào bảng của đối thủ không
    if offset_x <= x <= offset_x + BOARD_WIDTH and MARGIN <= y <= HEIGHT - MARGIN:
        #Tính tọa độ theo bảng lưới 
        col = (x - offset_x) // CELL_SIZE
        row = (y - MARGIN)   // CELL_SIZE
        if grids[opponent][row][col] == "~":
            hit_any = False
            for ship in ships[opponent]:
                if (row, col) in ship["positions"]:
                    idx = ship["positions"].index((row, col))
                    ship["hit"][idx] = True
                    grids[opponent][row][col] = "H"
                    hit_sound.play()
                    hit_any = True
                    if check_win(opponent):
                        game_over = True
                        winner = current_player
                    break
            if not hit_any:
                grids[opponent][row][col] = "M"
                miss_sound.play()
                current_player = opponent
    
# Vòng lặp chính
running = True
while running:
    display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

pygame.quit()
