import pygame
import os
import background
import sprites
import projectiles
import player
import level
import titleScreen
import time
from randlevels import genlevel

print(pygame.__path__)
pygame.init()

# IoraPy/


def start():
    ### First Room Stuff
    gemtype = ''
    hp = player.health
    tabCount = 0
    chosenElement = element[0]      #defualt to fire

    while not title.isFinished():
        screen.fill((0,0,0))
        title.startTitle(screen)
        pygame.display.flip()
    printer = 0

    ### Room Loop
    while not level1.isComplete(exitGroup):

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
                    allSprites.add(projectiles.projectiles(player, chosenElement, enemies,chests, player.rect.center,gemtype))
                    magic.add(projectiles.projectiles(player, chosenElement, enemies,chests, player.rect.center,gemtype))

        screen.fill((0,0,0))                #reset screen, for clean animation

        ### On-Screen Text
        background.makeBackground(screen, img, wallDown, sFloor, floor, tFloor, cFloor)
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        for x in range(0,player.health):
            screen.blit(heart, (0+(16*x), 0)) #Display HP.
        screen.blit(pygame.image.load(element[tabCount]).convert(), (0,16)) #Display element.
        #Now service player after everything else.
        player.update(pygame.key.get_pressed()) #Update player
        if (player.health>0 and player.invinc%2==0):
            screen.blit(player.image, player.rect) #Draw them if necessary
        myfont = pygame.font.SysFont('Comic Sans MS', 35)
        textsurface = myfont.render('Level 1 - Room 1', False, (255, 255, 255))
        screen.blit(textsurface,(425,0))
        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = myfont.render('Welcome to the dungeon', False, (255, 255, 255))
        screen.blit(textsurface,(425,25))
        if level1.isComplete(heroGroup):
            myfont = pygame.font.SysFont('Comic Sans MS', 50)
            textsurface = myfont.render('Dead already?!', False, (255, 255, 255))
            screen.blit(textsurface,(100,300))
        ### Exit Portal
        if level1.isComplete(enemyGroup):
            for sp in por:
                sp.target = player
                sp.rect.center = (300,300)
                allSprites.add(sp)
                textsurface = myfont.render('Exit has appeared!', False, (255, 255, 255))
                screen.blit(textsurface,(200,350))
        ### Keeps room running
        allSprites.update(pygame.key.get_pressed())
        allSprites.draw(screen)
        pygame.display.flip()   #ACTUALLY display all the images
        clock.tick(60)      #all animation and timing is based on this 60fps counte


def levelgen(screen,layout,title,sub_title,conditions,L):
    ### RoomS Design
    L2 = layout
    bulletLoops = 0
    skip = 0
    bossBulletTarget = [player]
        #--------------Create some sprite variables--------------
    allSprites = pygame.sprite.Group()
    enemies = []
    gems = []
    chests = []
    chest1 = []
    chest2 = []
    chest3 = []
    hp = player.health
    por = []
    levelgen = level.level(L2, enemies,chests,por,screen)
    levelgen.makeLevel()
    element = ['projectiles/fireProj.png', 'projectiles/iceProj.png', 'projectiles/lightProj.png']
    magic = pygame.sprite.Group()
    obstacles = levelgen.boxes
    obstacleGroup = pygame.sprite.Group()
    for spr in levelgen.boxes:
        allSprites.add(spr)
        obstacleGroup.add(spr)
        player.obstacles.append(spr)
    allSprites.add(player)
    heroGroup = pygame.sprite.Group(player)
    for chest in chests:
        if (chest.type != 'red' and chest.type != 'blue'):
            chest.target = player
        if (chest.type=='portal'):
            chest1.append(chest)
        if (chest.type=='item'):
            chest2.append(chest)
        if (chest.type=='dmg'):
            chest3.append(chest)
        if (chest.type=='red'):
            gems.append(chest)
        if (chest.type=='blue'):
            gems.append(chest)
        allSprites.add(chest)
    for sp in por:
        sp.target = player
        allSprites.add(sp)
    for enemy in enemies:
        enemy.target = player
        enemy.enemies = enemies #For them to check collision with one another.
        allSprites.add(enemy)
    exitGroup = pygame.sprite.Group(por)
    chest1Group = pygame.sprite.Group(chest1)
    chest2Group = pygame.sprite.Group(chest2)
    chest3Group = pygame.sprite.Group(chest3)
    enemyGroup = pygame.sprite.Group(enemies)
    gemsGroup = pygame.sprite.Group(gems)

    tabCount = 0
    chosenElement = element[0]      #defualt to fire
    gemtype = 'red'
    ### Room Loop
    while not levelgen.isComplete(exitGroup):
        pygame.event.pump()
        xCounter = yCounter = 0
        for event in pygame.event.get():    #event handler, checks for key presses (not holds)
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.K_0:
                skip = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    tabCount+=1
                    if tabCount >= len(element):
                        tabCount = 0
                    gemtype = elements[tabCount]
                    chosenElement = element[tabCount]
                    print(tabCount)
                elif event.key == pygame.K_SPACE and player.alive():
                    allSprites.add(projectiles.projectiles(player, chosenElement, enemies,chests, player.rect.center,gemtype))
                    magic.add(projectiles.projectiles(player, chosenElement, enemies,chests, player.rect.center,gemtype))
        screen.fill((0,0,0))                #reset screen, for clean animation
        background.makeBackground(screen, img, wallDown, sFloor, floor, tFloor, cFloor)
        if skip == 1:
            for sp in por:
                sp.target = player
                sp.rect.center = (300,350)
                allSprites.add(sp)
                sp.kill()
        ### Exit Portal
        if conditions == 'chest':
            if levelgen.isComplete(chest1Group):
                for sp in por:
                    sp.target = player
                    sp.rect.center = (300,350)
                    allSprites.add(sp)
                    myfont = pygame.font.SysFont('Comic Sans MS', 50)
                    textsurface = myfont.render('Exit has appeared!', False, (255, 255, 255))
                    screen.blit(textsurface,(150,50))

        if conditions == 'kill-all':
            if levelgen.isComplete(enemyGroup):
                for sp in por:
                    sp.target = player
                    if (L==9):
                        sp.rect.center = (150,400)
                        allSprites.add(sp)
                        myfont = pygame.font.SysFont('Comic Sans MS', 25)
                        textsurface = myfont.render('C Ya!', False, (255, 255, 255))
                        screen.blit(textsurface,(30,400))
                    elif (L==5):
                        sp.rect.center = (150,350)
                        allSprites.add(sp)
                        myfont = pygame.font.SysFont('Comic Sans MS', 25)
                        textsurface = myfont.render('Did you order an exit?', False, (255, 255, 255))
                        screen.blit(textsurface,(30,300))
                    elif (L==3):
                        sp.rect.center = (200,350)
                        allSprites.add(sp)
                        myfont = pygame.font.SysFont('Comic Sans MS', 25)
                        textsurface = myfont.render('Not an exit', False, (255, 255, 255))
                        screen.blit(textsurface,(50,400))
                    else :
                        sp.rect.center = (300,350)
                        allSprites.add(sp)
                        myfont = pygame.font.SysFont('Comic Sans MS', 50)
                        textsurface = myfont.render('Exit has appeared!', False, (255, 255, 255))
                        screen.blit(textsurface,(100,300))

        if conditions == 'gems':
            if levelgen.isComplete(gemsGroup):
                for sp in por:
                    sp.target = player
                    sp.rect.center = (300,350)
                    allSprites.add(sp)
                    myfont = pygame.font.SysFont('Comic Sans MS', 50)
                    textsurface = myfont.render('The gods have been honored', False, (255, 255, 255))
                    screen.blit(textsurface,(100,300))
        for enemy in enemies:
            if hasattr(enemy, "boss_health"):
                if enemy.boss_health > 0:
                    bar = pygame.draw.rect(screen, (255, 0, 0), (220, 440, enemy.boss_health*10, 15))
                    if enemy.isType == "Orc":
                        if bulletLoops % 80 == 0:
                            allSprites.add(projectiles.projectiles(enemy, 'projectiles/boss_bullet.png', bossBulletTarget,chests, enemy.rect.center,'orc'))
                            enemy.direction = 'up'
                            allSprites.add(projectiles.projectiles(enemy, 'projectiles/boss_bullet.png', bossBulletTarget,chests, enemy.rect.center,'orc'))
                            enemy.direction = 'left'
                            allSprites.add(projectiles.projectiles(enemy, 'projectiles/boss_bullet.png', bossBulletTarget,chests, enemy.rect.center,'orc'))
                            enemy.direction = 'right'
                            allSprites.add(projectiles.projectiles(enemy, 'projectiles/boss_bullet.png', bossBulletTarget,chests, enemy.rect.center,'orc'))
                            enemy.direction = 'down'
                            bulletLoops = 0
                    elif enemy.isType == "Tenta":
                        if bulletLoops % 40 == 0:
                            enemy.direction = 'right'
                            allSprites.add(projectiles.projectiles(enemy, 'projectiles/flame_projectile.png', bossBulletTarget, chests, enemy.rect.center, 'orc'))
                            enemy.direction = 'left'
                            allSprites.add(projectiles.projectiles(enemy, 'projectiles/flame_projectile.png', bossBulletTarget, chests, enemy.rect.center, 'orc'))
                            enemy.direction = 'right'
                    elif enemy.isType == "Cat_Staff":
                        cloop = 0
                        if bulletLoops % 180 == 0:
                            enemy.currentAnim = enemy.catThrow
                        if enemy.currentAnim == enemy.catThrow:
                            enemy.catloop += 1
                            if enemy.catloop % 24 == 0:
                                enemy.direction = "targeting"
                                allSprites.add(projectiles.projectiles(enemy, 'projectiles/cat_projectile.png', bossBulletTarget, chests, enemy.rect.center, 'cat_staff'))
                            if enemy.catloop % 48 == 0:
                                enemy.currentAnim = enemy.catIdle
                                enemy.catloop = 0
                else:
                    bar = ""
        ### On-Screen Text
        if levelgen.isComplete(heroGroup):
            myfont = pygame.font.SysFont('Comic Sans MS', 50)
            textsurface = myfont.render('Mr.Stark I dont feel so good...', False, (255, 255, 255))
            screen.blit(textsurface,(100,400))

        if conditions == 'chest' and levelgen.isComplete(chest3Group):
            myfont = pygame.font.SysFont('Comic Sans MS', 20)
            textsurface = myfont.render('Radiation Effects : -2 HP', False, (255, 255, 255))
            screen.blit(textsurface,(50,30))
        if conditions != 'gems' and L != 5 and levelgen.isComplete(chest2Group):
            myfont = pygame.font.SysFont('Comic Sans MS', 20)
            textsurface = myfont.render('Health Bonus : +1 HP', False, (255, 255, 255))
            screen.blit(textsurface,(50,40))
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        for x in range(0,player.health):
            screen.blit(heart, (0+(16*x), 0)) #Display HP.
        screen.blit(pygame.image.load(element[tabCount]).convert(), (0,16)) #Display element.
        #Now service player after everything else.
        player.update(pygame.key.get_pressed()) #Update player
        if (player.health>0 and player.invinc%2==0):
            screen.blit(player.image, player.rect) #Draw them if necessary
        myfont = pygame.font.SysFont('Comic Sans MS', 35)
        textsurface = myfont.render(title, False, (255, 255, 255))
        screen.blit(textsurface,(425,0))
        myfont = pygame.font.SysFont('Comic Sans MS', 25)
        textsurface = myfont.render(sub_title, False, (255, 255, 255))
        screen.blit(textsurface,(405,25))

        ### Loop Stuff
        allSprites.update(pygame.key.get_pressed())
        allSprites.draw(screen)
        pygame.display.flip()   #ACTUALLY display all the images
        bulletLoops = bulletLoops + 1
        clock.tick(60)      #all animation and timing is based on this 60fps counter
    for x in obstacleGroup.sprites():
        x.kill()
        x.rect.center = (-55,-55) #Put self out-of-bounds -- but not (-5,-5)

#START OF MAIN

print(pygame.__path__)
pygame.init()

### Level Layouts ###
L1 = [['-', '-', '-', 'X', 'X', '-', '-', '-', '-', 'X','X', '-', '-','-','-','!'],
      ['-', '-', '#', '-', 'X', '-', '-', '-', '-', 'X','-', '#', '-'],
      ['-', '-', '¡', '-', '#', '-', '-', '-', '-', '#','-', '¡', '-'],
      ['-', '-', '-', '-', '¡', '-', '-', '-', '-', '¡','-', '-', '-'],
      ['-', '-', '#', '-', '#', '-', '-', '-', '-', '#','-', '#', '-'],
      ['-', '-', '¡', '1', '-', '-', '-', '-', '-', '-','-', '¡', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '¡', '-', '-', '-', '-', '¡','-', '-', '-']]

L2 = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-','-','-','!'],
      ['-', '-', '¡', '-', '1', '-', '-', '-', '-', '-','1', '¡', '-'],
      ['-', '-', '-', '$', '-', '-', '%', '-', '-', '*','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '1', '-', '-', '-', '1', '-','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '¡', '-', '-', '-', '-', '-', '-', '-','-', '¡', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-']]

L4 = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-','-','-','!'],
      ['-', '-', '-', 'X', '-', '-', 'X', '-', '#', '-','-', '%', '-'],
      ['-', '-', '-', 'X', 'X', '-', 'X', '-', '-', 'X','¡', '-', '-'],
      ['-', '-', 'X', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '#', '-', '#', '-', '#', '-','#', '-', '-'],
      ['-', '-', '#', '-', '-', '-', '-', '-', '#', '-','-', '-', '-'],
      ['-', '¡', '-', '-', '-', '-', '-', '-', '-', '-','-', '#', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-']]

L5 = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-','-','-','!'],
      ['-', '-', '¡', '-', 'R', '-', '-', '-', '-', 'B','-', '¡', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '1', '-', '-', '-', '-', '-', '-', '-','-', '1', '-'],
      ['-', '-', '1', '-', '-', '-', '-', '-', '-', '-','-', '1', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '¡', '-', '-', '-', '-', '-', '-', '-','-', '¡', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-']]

L7 = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-','-','-','!'],
      ['-', '-', '-', 'X', 'X', '#', '#', '#', '-', '-','-', '#', '-'],
      ['-', '-', '-', 'X', 'X', '#', '¡', '#', '-', '1','1', '-', '-'],
      ['-', '-', '¡', '-', '-', '#', '¡', '#', '-', '1','1', '-', '-'],
      ['-', '#', '-', '-', '-', '#', '#', '#', '-', '-','-', '#', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '#', '-','-', '¡', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-']]

L3 = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-','-','-','!'],
      ['-', '#', '-', 'X', '-', '-', 'X', '-', '#', '-','-', '%', '-'],
      ['-', '-', '-', 'X', 'X', '-', 'X', '-', '#', '#','¡', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '#', '-', '-', '-', '-', '-', '-', '-','O', '-', '-'],
      ['-', '-', '-', '#', '-', '-', '-', '-', '#', '-','-', '-', '-'],
      ['-', '#', '-', '-', '-', '-', '-', '-', '#', '-','-', '%', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-']]

L6 = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-','-','-','!'],
      ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#','#', '#', '#'],
      ['-', '-', '-', '-', '-', '-', 'S', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['#', '#', '#', '#', '#', '#', '-', '#', '#', '#','#', '#', '#'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-']]

L8 = [['-', '¡', '-', '-', '-', '-', '-', '-', '-', '-','-', '¡', '-','-','-','!'],
      ['-', '¡', 'X', '-', '-', '¡', '¡', '¡', '-', '-','1', '¡', '-'],
      ['-', '-', '-', '-', '-', '¡', '%', '¡', '-', '-','-', '-', '-'],
      ['X', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '1'],
      ['X', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '1'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '¡', 'X', '-', '-', '-', '-', '-', '-', '-','1', '¡', '-'],
      ['-', '¡', '-', '-', '-', '-', '-', '-', '-', '-','-', '¡', '-']]

L9 = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-','-','-','!'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','~', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-']]



#####################


#--------------------Set some variables-------------------
himitsu = open(os.path.join('himitsu', 'passes.txt'), 'r')
lValue = int(himitsu.read())
himitsu.close()
width = 640
height = 480
center = ((480/2), (640/2))
size = width, height
screen = pygame.display.set_mode(size)  #opens the physical screen
clock = pygame.time.Clock()     #keeps track of the fps and stuff
check = 1


### Level 1 -Room 1 Loop
while check != 0:
    L1 = [['-', '-', '-', 'X', 'X', '-', '-', '-', '-', 'X','X', '-', '-','-','-','!'],
          ['-', '-', '#', '-', 'X', '-', '-', '-', '-', 'X','-', '#', '-'],
          ['-', '-', '¡', '-', '#', '-', '-', '-', '-', '#','-', '¡', '-'],
          ['-', '-', '-', '-', '¡', '-', '-', '-', '-', '¡','-', '-', '-'],
          ['-', '-', '#', '-', '#', '-', '-', '-', '-', '#','-', '#', '-'],
          ['-', '-', '¡', '1', '-', '-', '-', '-', '-', '-','-', '¡', '-'],
          ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-','-', '-', '-'],
          ['-', '-', '-', '-', '¡', '-', '-', '-', '-', '¡','-', '-', '-']]



    #--------------Create some sprite variables--------------
    allSprites = pygame.sprite.Group()
    enemies = []
    por = []
    chests = []
    chest1 = []
    chest2 = []
    chest3 = []
    level1 = level.level(L1, enemies,chests,por,screen)
    level1.makeLevel()
    element = ['projectiles/fireProj.png', 'projectiles/iceProj.png', 'projectiles/lightProj.png']
    elements = ['red','blue','light']
    magic = pygame.sprite.Group()
    obstacles = level1.boxes
    obstacleGroup = pygame.sprite.Group()
    for spr in level1.boxes:
        allSprites.add(spr)
        obstacleGroup.add(spr)
    player = player.player('Character/DownAnim/Down2.png', obstacles, (width/2, height-50))
    allSprites.add(player)
    heroGroup = pygame.sprite.Group(player)
    for sp in por:
        sp.target = player
        allSprites.add(sp)
    for enemy in enemies:
        enemy.target = player
        enemy.enemies = enemies #For them to check collision with one another.
        allSprites.add(enemy)
    enemyGroup = pygame.sprite.Group(enemies)
    exitGroup = pygame.sprite.Group(por)

    #-----------------------Load images-----------------------
    img = pygame.image.load('images/bot_wall.jpg').convert()
    wallDown = pygame.image.load('images/Side_Walls_05.jpg').convert()
    sFloor = pygame.image.load('images/Left_edge_floor.jpg').convert()
    floor = pygame.image.load('images/floor.jpg').convert()
    tFloor = pygame.image.load('images/Top_edge_floor.jpg').convert()
    cFloor = pygame.image.load('images/Left_corner_floor.jpg').convert()
    heart = pygame.image.load('HUD/heart.png').convert().convert_alpha()
    title = titleScreen.titleScreen(lValue)
    hp = player.health
    start()
    for x in obstacleGroup.sprites():
        x.kill()
        x.rect.center = (-55,-55) #Put self out-of-bounds -- but not (-5,-5)
    if title.endless == 1:
        while 1:
            R1 = genlevel()
            levelgen(screen,R1,'Endless', 'Endless', 'kill-all',0)
    else:
        levelgen(screen,L2, 'Level 1 Room 2','Get some hair on your chest','chest',2)
        levelgen(screen,L3, 'Level 1 Room 3','I hate this guy','kill-all',6)
        levelgen(screen,L4, 'Level 2 Room 1','Flame fun','kill-all',3)
        levelgen(screen,L5, 'Level 2 Room 2','Honor the gods','gems',4)
        levelgen(screen,L6, 'Level 2 Room 3', 'Getting tight', 'kill-all', 7)
        levelgen(screen,L7, 'Level 3 Room 1','Why cant we just get along?','kill-all',5)
        levelgen(screen,L8, 'Level 3 Room 2', 'Slime friends', 'kill-all', 8)
        levelgen(screen,L9, 'Level 3 Room 3', ':3c', 'kill-all', 9)


    exit()
