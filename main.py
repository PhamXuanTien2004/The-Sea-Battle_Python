#Module import
import pygame

#Module Initialization
pygame.init()


#Game setting and variables
SCREENWIDTH = 800
SCREENHEIGHT = 600
ROWs = 10
COLS = 10
CELLSIZE = 50

#Pygame Display Initialization 
GAMESCREEN = pygame.display.set_mode((SCREENHEIGHT, SCREENHEIGHT))
pygame.display.set_caption('BATTLE SHIP')

#Main game Loop
RUNGAME = True
while RUNGAME:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNGAME = False
            
    pygame.display.update()
    
pygame.quit()


