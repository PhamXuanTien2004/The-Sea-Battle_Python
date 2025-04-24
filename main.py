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

# Vòng lặp chính
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
