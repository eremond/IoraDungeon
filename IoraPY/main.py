import pygame
import os
import background
import sprites
import projectiles
import player
import level
import titleScreen

print(pygame.__path__)
pygame.init()

# IoraPy/
#--------------------Set some variables-------------------
himitsu = open('himitsu/passes.txt', 'r')
lValue = int(himitsu.read())
himitsu.close()
width = 640
height = 480
center = ((480/2), (640/2))
size = width, height
screen = pygame.display.set_mode(size)  #opens the physical screen
clock = pygame.time.Clock()     #keeps track of the fps and stuff
L1 = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-'],
      ['-', 'X', '-', 'X', '-', '-', 'X', '-', 'X', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]


#--------------Create some sprite variables--------------
allSprites = pygame.sprite.Group()
enemies = []
level1 = level.level(L1, enemies)
level1.makeLevel()
element = ['projectiles/fireProj.png', 'projectiles/iceProj.png', 'projectiles/lightProj.png']
magic = pygame.sprite.Group()
obstacles = level1.boxes
obstacleGroup = pygame.sprite.Group()
for spr in level1.boxes:
    allSprites.add(spr)
    obstacleGroup.add(spr)
player = player.player('Character/DownAnim/Down2.png', obstacles, (width/2, height-50))
allSprites.add(player)
heroGroup = pygame.sprite.Group(player)
for enemy in enemies:
	enemy.target = player
	allSprites.add(enemy)
enemyGroup = pygame.sprite.Group(enemies)

#-----------------------Load images-----------------------
img = pygame.image.load('images/bot_wall.jpg').convert()
wallDown = pygame.image.load('images/Side_Walls_05.jpg').convert()
sFloor = pygame.image.load('images/Left_edge_floor.jpg').convert()
floor = pygame.image.load('images/floor.jpg').convert()
tFloor = pygame.image.load('images/Top_edge_floor.jpg').convert()
cFloor = pygame.image.load('images/Left_corner_floor.jpg').convert()
title = titleScreen.titleScreen(lValue)
#---------------------Game Loop--------------------------
tabCount = 0
chosenElement = element[0]      #defualt to fire
while 1:

    while not title.isFinished():
        screen.fill((0,0,0))
        title.startTitle(screen)
        pygame.display.flip()

    while not level1.isComplete(enemyGroup):
        pygame.event.pump()

        xCounter = yCounter = 0
        for event in pygame.event.get():    #event handler, checks for key presses (not holds)
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    tabCount+=1
                    if tabCount >= len(element):
                        tabCount = 0
                    chosenElement = element[tabCount]
                    print(tabCount)
                elif event.key == pygame.K_SPACE and player.alive():
                    allSprites.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))
                    magic.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))
                
                

        screen.fill((0,0,0))                #reset screen, for clean animation

        background.makeBackground(screen, img, wallDown, sFloor, floor, tFloor, cFloor)

        allSprites.update(pygame.key.get_pressed())
        allSprites.draw(screen)
        pygame.display.flip()   #ACTUALLY display all the images
        clock.tick(60)      #all animation and timing is based on this 60fps counter
    exit()
