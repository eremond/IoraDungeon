import pygame
import os
import background
import sprites
import projectiles
import player
import level
import titleScreen
import boss
import fade
import enemy

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
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', 'X', '#', 'X', '-', '-', 'X', '-', 'X', '-', '-', '#'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]

L3 = [['-', '-', '-', 'X', 'X', 'X', 'X', 'X', '-', '-', '-', '-', '-'],
      ['-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '#', '-', '#', '#', '-', '#', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#']]

L5 = [['-', '-', '-', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '-', '-', '-'],
      ['-', '-', '-', '#', 'X', 'X', 'X', 'X', 'X', '#', '-', '-', '-'],
      ['-', '-', '-', '-', 'X', 'X', 'X', 'X', 'X', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '#', '-', '-', '-', '#', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', 'X', 'X', 'X', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]

#--------------Create some sprite variables--------------
allSprites = pygame.sprite.Group()
enemies = []
bosses = []
bossGroup = pygame.sprite.Group()
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
boss1 = boss.boss('Enemies/orc.png', (400, 32+64), [], player)
for Enemy in enemies:
    Enemy.target = player
    allSprites.add(Enemy)
enemyGroup = pygame.sprite.Group(enemies)
bossBulletTarget = [player]
bulletLoops = 0
bossGroup.add(boss1)
bosses.append(boss1)

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

#--------------------LEVEL ONE--------------------------

    while not level1.isComplete(enemyGroup):
        pygame.event.pump()

        for event in pygame.event.get():    #event handler, checks for key presses (not holds)
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    tabCount+=1
                    if tabCount >= len(element):
                        tabCount = 0
                    chosenElement = element[tabCount]
                elif event.key == pygame.K_SPACE and player.alive():
                    allSprites.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center, tabCount))
                    magic.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))   
        
        screen.fill((0,0,0))                #reset screen, for clean animation

        background.makeBackground(screen, img, wallDown, sFloor, floor, tFloor, cFloor)

        allSprites.update(pygame.key.get_pressed())
        allSprites.draw(screen)
        pygame.display.flip()   #ACTUALLY display all the images
        clock.tick(60)      #all animation and timing is based on this 60fps counter 
  
#--------------BOSS ROOM (LVL 2)-------------------
    startBossRoom = True
    if startBossRoom:       #first boss, so we don't have to clear the boss group
        player.center = (width/2, height-50)
        player.direction = 'up'     #reset player to spawn point and facing up
        player.obstacles = []
        allSprites = pygame.sprite.Group()
        allSprites.add(boss1)
        enemies.append(boss1)
        allSprites.add(player)
        bulletLoops = 0
    
    while boss1.alive():
        pygame.event.pump()

        for event in pygame.event.get():    #event handler, checks for key presses (not holds)
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    tabCount+=1
                    if tabCount >= len(element):
                        tabCount = 0
                    chosenElement = element[tabCount]
                elif event.key == pygame.K_SPACE and player.alive():
                    allSprites.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))
   
        screen.fill((0,0,0))
        background.makeBackground(screen, img, wallDown, sFloor, floor, tFloor, cFloor)
        allSprites.update(pygame.key.get_pressed())
        allSprites.draw(screen)
        if boss1.alive():
            healthBar = pygame.draw.rect(screen, (255, 0, 0), (220, 440, boss1.boss_health*10, 15))
            if bulletLoops % 120 == 0:
                baby1 = enemy.enemy('Enemies/slime.png', (boss1.rect.x - 10, boss1.rect.y), [])       #spawn mini monsters
                baby2 = enemy.enemy('Enemies/slime.png', (boss1.rect.x + 10, boss1.rect.y), [])
                baby1.target = baby2.target = player
                allSprites.add(baby1)
                allSprites.add(baby2)
                enemies.append(baby1)
                enemies.append(baby2)
            if bulletLoops % 60 == 0:
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                boss1.direction = 'up'
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                boss1.direction = 'left'
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                boss1.direction = 'right'
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))                           
                boss1.direction = 'down'
        else:
            healthBar = ""
            startBossRoom = False

        pygame.display.flip()
        clock.tick(60)
        bulletLoops+=1
    #boss is killed! set the flag, start the next level.

#--------------------LEVEL THREE--------------------------
    startBossRoom = False
    #new level, reset EVERYTHING
    if not startBossRoom:
        enemies.clear()
        level3 = level.level(L3, enemies)       #remake the new level, then put it into the next loop!
        level3.makeLevel()
        obstacles = level3.boxes
        obstacleGroup = pygame.sprite.Group(obstacles)
        enemyGroup = pygame.sprite.Group(enemies)
        allSprites = pygame.sprite.Group()
        allSprites.add(player)
        for stuff in obstacles:
            allSprites.add(stuff)
        for moreStuff in enemies:
            moreStuff.target = player
            allSprites.add(moreStuff)
        player.obstacles = obstacles
        player.rect.center = (width/2, height-50)
        level1.isPuzzleDone = False
    #fade.fadeOut(screen, 400)

    while not level3.isComplete(enemyGroup):        #start level 3's game loop
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
                elif event.key == pygame.K_SPACE and player.alive():
                    allSprites.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))
                    magic.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))          

        screen.fill((0,0,0))                #reset screen, for clean animation

        background.makeBackground(screen, img, wallDown, sFloor, floor, tFloor, cFloor)

        allSprites.update(pygame.key.get_pressed())
        allSprites.draw(screen)
        pygame.display.flip()   #ACTUALLY display all the images
        clock.tick(60)      #all animation and timing is based on this 60fps counter

#--------------BOSS ROOM (LVL 4)-------------------

    startBossRoom = True
    if startBossRoom:       #will have to clear boss group, but jsut using one boss for now, so its cool
        player.center = (width/2, height-50)
        player.direction = 'up'     #reset player to spawn point and facing up
        player.obstacles = []
        allSprites = pygame.sprite.Group()
        boss1.__init__(boss1.img, boss1.pos, [], player)
        bossGroup.add(boss1)
        allSprites.add(boss1)
        enemies.append(boss1)
        allSprites.add(player)
        bulletLoops = 0
    
    while boss1.alive():        #just using the same boss for now, will change later
        pygame.event.pump()

        for event in pygame.event.get():    #event handler, checks for key presses (not holds)
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    tabCount+=1
                    if tabCount >= len(element):
                        tabCount = 0
                    chosenElement = element[tabCount]
                elif event.key == pygame.K_SPACE and player.alive():
                    allSprites.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))
   
        screen.fill((0,0,0))
        background.makeBackground(screen, img, wallDown, sFloor, floor, tFloor, cFloor)
        allSprites.update(pygame.key.get_pressed())
        allSprites.draw(screen)
        if boss1.alive():
            healthBar = pygame.draw.rect(screen, (255, 0, 0), (220, 440, boss1.boss_health*10, 15))
            if bulletLoops % 120 == 0:
                baby1 = enemy.enemy('Enemies/slime.png', (boss1.rect.x - 10, boss1.rect.y), [])       #spawn mini monsters
                baby2 = enemy.enemy('Enemies/slime.png', (boss1.rect.x + 10, boss1.rect.y), [])
                baby1.target = baby2.target = player
                allSprites.add(baby1)
                allSprites.add(baby2)
                enemies.append(baby1)
                enemies.append(baby2)
            if bulletLoops % 60 == 0:
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                boss1.direction = 'up'
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                boss1.direction = 'left'
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                boss1.direction = 'right'
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))                           
                boss1.direction = 'down'
        else:
            healthBar = ""
            startBossRoom = False

        pygame.display.flip()
        clock.tick(60)
        bulletLoops+=1
        
    #boss is killed! set the flag, start the next level.

#--------------------LEVEL FIVE--------------------------
    startBossRoom = False
    #new level, reset EVERYTHING
    if not startBossRoom:
        enemies.clear()
        level5 = level.level(L5, enemies)       #remake the new level, then put it into the next loop!
        level5.makeLevel()
        obstacles = level5.boxes
        obstacleGroup = pygame.sprite.Group(obstacles)
        enemyGroup = pygame.sprite.Group(enemies)
        allSprites = pygame.sprite.Group()
        allSprites.add(player)
        for stuff in obstacles:
            allSprites.add(stuff)
        for moreStuff in enemies:
            moreStuff.target = player
            allSprites.add(moreStuff)
        player.obstacles = obstacles
        player.rect.center = (width/2, height-50)
        bulletLoops = 0
        level1.isPuzzleDone = False
    #fade.fadeOut(screen, 400)

    #onto level 5!
    while not level5.isComplete(enemyGroup):        #start level 5's game loop
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
                elif event.key == pygame.K_SPACE and player.alive():
                    allSprites.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))        

        screen.fill((0,0,0))                #reset screen, for clean animation

        background.makeBackground(screen, img, wallDown, sFloor, floor, tFloor, cFloor)

        allSprites.update(pygame.key.get_pressed())
        allSprites.draw(screen)
        pygame.display.flip()   #ACTUALLY display all the images
        bulletLoops += 1
        clock.tick(60)      #all animation and timing is based on this 60fps counter

#-------------------------FINAL BOSS-------------------------
    #if any of you can beat this one, MADDDDD props.
    startBossRoom = True
    if startBossRoom:       #will have to clear boss group, but just using one boss for now, so its cool
        player.center = (width/2, height-50)
        player.direction = 'up'     #reset player to spawn point and facing up
        player.obstacles = []
        allSprites = pygame.sprite.Group()
        boss1.__init__(boss1.img, boss1.pos, [], player)
        boss2 = boss.boss(boss1.img, (boss1.pos[0] - 30, boss1.pos[1]), [], player)
        boss3 = boss.boss(boss1.img, (boss1.pos[0] + 30, boss1.pos[1]), [], player)
        bossGroup.add(boss1)
        bossGroup.add(boss2)        #creating MULTIPLE bosses (of the same orc type though!)
        bossGroup.add(boss3)
        allSprites.add(boss1)
        allSprites.add(boss2)
        allSprites.add(boss3)
        enemies.append(boss1)
        enemies.append(boss2)
        enemies.append(boss3)
        allSprites.add(player)
        bulletLoops = 0
    
    while boss1.alive() and boss2.alive() and boss3.alive():        #just using the same boss for now, will change later
        pygame.event.pump()

        for event in pygame.event.get():    #event handler, checks for key presses (not holds)
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    tabCount+=1
                    if tabCount >= len(element):
                        tabCount = 0
                    chosenElement = element[tabCount]
                elif event.key == pygame.K_SPACE and player.alive():
                    allSprites.add(projectiles.projectiles(player, chosenElement, enemies, player.rect.center))
   
        screen.fill((0,0,0))
        background.makeBackground(screen, img, wallDown, sFloor, floor, tFloor, cFloor)
        allSprites.update(pygame.key.get_pressed())
        allSprites.draw(screen)
        if boss1.alive():
            healthBar = pygame.draw.rect(screen, (255, 0, 0), (220, 440, boss1.boss_health*10, 15))
            if bulletLoops % 120 == 0:
                baby1 = enemy.enemy('Enemies/slime.png', (boss1.rect.x - 10, boss1.rect.y), [])       #spawn mini monsters
                baby2 = enemy.enemy('Enemies/slime.png', (boss1.rect.x + 10, boss1.rect.y), [])
                baby1.target = baby2.target = player
                allSprites.add(baby1)
                allSprites.add(baby2)
                enemies.append(baby1)
                enemies.append(baby2)
            if bulletLoops % 60 == 0:
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                allSprites.add(projectiles.projectiles(boss2, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                allSprites.add(projectiles.projectiles(boss3, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                boss1.direction = 'up'
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                allSprites.add(projectiles.projectiles(boss2, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                allSprites.add(projectiles.projectiles(boss3, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                boss1.direction = 'left'
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                allSprites.add(projectiles.projectiles(boss2, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                allSprites.add(projectiles.projectiles(boss3, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                boss1.direction = 'right'
                allSprites.add(projectiles.projectiles(boss1, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                allSprites.add(projectiles.projectiles(boss2, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))
                allSprites.add(projectiles.projectiles(boss3, 'projectiles/boss_bullet.png', bossBulletTarget, boss1.rect.center))                           
                boss1.direction = 'down'
        else:
            healthBar = ""
            startBossRoom = False

        pygame.display.flip()
        clock.tick(60)
        bulletLoops+=1
    exit()
