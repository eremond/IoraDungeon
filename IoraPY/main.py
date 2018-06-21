
#A quick and dirty usage of pygame's screen and event system to create movement
#Animation and tile-maps to be added shortly

# +++ Building on the scroll test, I am testing animation for movement on the same file

import os
import pygame
import time
import levels
print(pygame.__path__)
pygame.init()

#--------------------Set some variables-------------------
width = 640
height = 480
size = width, height
screen = pygame.display.set_mode(size)  #opens the physical screen

#-----------------------Load images-----------------------
img = pygame.image.load('C:\\Users\\Andrew\\Desktop\\IoraPY\\images\\bot_wall.jpg').convert()
#img = pygame.transform.scale(img, (16,16))
#imgRect = img.get_rect()

wallDown = pygame.image.load('C:\\Users\\Andrew\\Desktop\\IoraPY\\images\\Side_Walls_05.jpg').convert()
#wallDown = pygame.transform.scale(wallDown, (16,16))
#wallRect = wallDown.get_rect()

sFloor = pygame.image.load('C:\\Users\\Andrew\\Desktop\\IoraPY\\images\\Left_edge_floor.jpg').convert()

floor = pygame.image.load('C:\\Users\\Andrew\\Desktop\\IoraPY\\images\\floor.jpg').convert()

tFloor = pygame.image.load('C:\\Users\\Andrew\\Desktop\\IoraPY\\images\\Top_edge_floor.jpg').convert()

cFloor = pygame.image.load('C:\\Users\\Andrew\\Desktop\\IoraPY\\images\\Left_corner_floor.jpg').convert()
#-------------Position the images in the world------------
#imgRect.topleft = (0,0)
#imgRect2 = imgRect.copy()
#imgRect2.center = (5, 100)

##---------------------Game Loop--------------------------
counter = 0
while 1:
    xCounter = yCounter = 0
    for event in pygame.event.get():    #event handler, just used to quit for now
        if event.type == pygame.QUIT:
            exit()

    screen.fill((0,0,0))                #reset screen, for clean animation

    levels.makeLevel(screen, img, wallDown, sFloor, floor, tFloor, cFloor)

    pygame.display.flip()
    #screen.blit(img, (0,0))
    #pygame.display.flip()   #displays the images onto the screen


'''Some experimenting with wrapping the character around the screen
    if imgRect.top > height:
        bRect.bottom=0
    if imgRect.bottom < 0:
        bRect.top=height
    if imgRect.left > width:
        bRect.right=0
    if imgRect.right < 0:
        bRect.left = width
'''