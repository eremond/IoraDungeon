import pygame
import background
import sprites
import projectiles
import player
import level
print(pygame.__path__)
pygame.init()


#--------------------Set some variables-------------------
width = 640
height = 480
center = ((480/2), (640/2))
size = width, height
screen = pygame.display.set_mode(size)  #opens the physical screen
clock = pygame.time.Clock()     #keeps track of the fps and stuff
L1 = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '#', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]


#--------------Create some sprite variables--------------
allSprites = pygame.sprite.Group()
level1 = level.level(L1)
level1.makeLevel()
enemy = sprites.sprites('Character/DownAnim/Down2.png', center)
allSprites.add(enemy)
element = ['projectiles/fireProj.png', 'projectiles/iceProj.png', 'projectiles/lightProj.png']
magic = pygame.sprite.Group()
enemies = [enemy]
obstacles = level1.boxes
enemyGroup = pygame.sprite.Group(enemies)
obstacleGroup = pygame.sprite.Group()
for spr in level1.boxes:
    allSprites.add(spr)
    obstacleGroup.add(spr)
player = player.player('Character/DownAnim/Down2.png', obstacles, (width/2, height-50))
allSprites.add(player)
heroGroup = pygame.sprite.Group(player)


#-----------------------Load images-----------------------
img = pygame.image.load('level/bot_wall.jpg').convert()
wallDown = pygame.image.load('level/Side_Walls_05.jpg').convert()
sFloor = pygame.image.load('level/Left_edge_floor.jpg').convert()
floor = pygame.image.load('level/floor.jpg').convert()
tFloor = pygame.image.load('level/Top_edge_floor.jpg').convert()
cFloor = pygame.image.load('level/Left_corner_floor.jpg').convert()

#---------------------Game Loop--------------------------
tabCount = 0
chosenElement = element[0]      #defualt to fire
while 1:

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
                elif event.key == pygame.K_SPACE:
                    allSprites.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))
                    magic.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))
                
                

        screen.fill((0,0,0))                #reset screen, for clean animation

        background.makeBackground(screen, img, wallDown, sFloor, floor, tFloor, cFloor)

        allSprites.update(pygame.key.get_pressed())
        allSprites.draw(screen)
        pygame.display.flip()   #ACTUALLY display all the images
        clock.tick(60)      #all animation and timing is based on this 60fps counter
    exit()
