import pygame
import levels
import sprites
import projectiles
print(pygame.__path__)
pygame.init()

def animGen(animation):     #helps the move function to generate the next image in the animation sequence
    x = 0
    a = 0
    order = (animation[0], animation[1], animation[2], animation[1])    #order of which the animation should be played
    while True:
        if x > len(order)-1:
            x = 0
        yield order[x]
        a+=1
        if a == 15:     #used to slow down the animation
            x+=1
            a = 0

def move(key, sprite, *animGens, animations):       #can probably be thrown in an update function
    uAnim, dAnim, lAnim, rAnim = animGens

    if key[pygame.K_DOWN]:
        if sprite.rect.y < 480-16-sprite.rect.height:
            sprite.rect.y+=2
        sprite.image = next(dAnim)
        return "down"
    if key[pygame.K_UP]:
        if sprite.rect.y > 16:
            sprite.rect.y-=2
        sprite.image = next(uAnim)
        return "up"
    if key[pygame.K_LEFT]:
        if sprite.rect.x > 16:
            sprite.rect.x-=2
        sprite.image = next(lAnim)
        return "left"
    if key[pygame.K_RIGHT]:
        if sprite.rect.x < 640-16-sprite.rect.width:
            sprite.rect.x+=2
        sprite.image = next(rAnim)
        return "right"
    else:
        sprite.image = animations[1][1]
        return "down"


#--------------------Set some variables-------------------
width = 640
height = 480
size = width, height
screen = pygame.display.set_mode(size)  #opens the physical screen
clock = pygame.time.Clock()     #keeps track of the fps and stuff


#--------------Create some sprite variables--------------
player = sprites.sprites('Character/DownAnim/Down2.png')
enemy = sprites.sprites('Character/DownAnim/Down2.png')
player.isType = "player"
leftAnim = player.loadAnimSprite('Character/LeftAnim')
rightAnim = player.loadAnimSprite('Character/RightAnim')
upAnim = player.loadAnimSprite('Character/UpAnim')
downAnim = player.loadAnimSprite('Character/DownAnim')
element = ['projectiles/fireProj.png', 'projectiles/iceProj.png', 'projectiles/lightProj.png']
uAnim = animGen(upAnim)
dAnim = animGen(downAnim)
lAnim = animGen(leftAnim) 
rAnim = animGen(rightAnim)
enemy.center(width, height)
magic = pygame.sprite.Group()
enemies = [enemy]
enemyGroup = pygame.sprite.Group(enemies)

#-----------------------Load images-----------------------
img = pygame.image.load('level/bot_wall.jpg').convert()
wallDown = pygame.image.load('level/Side_Walls_05.jpg').convert()
sFloor = pygame.image.load('level/Left_edge_floor.jpg').convert()
floor = pygame.image.load('level/floor.jpg').convert()
tFloor = pygame.image.load('level/Top_edge_floor.jpg').convert()
cFloor = pygame.image.load('level/Left_corner_floor.jpg').convert()


#----------Put character in starting position------------
player.rect.x = int(width/2)
player.rect.y = int(height-player.rect.height-20)


#---------------------Game Loop--------------------------
tabCount = 0
chosenElement = element[0]      #defualt to fire
while 1:

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
                magic.add(projectiles.projectiles(player, chosenElement, direction, enemies))
                
                

    screen.fill((0,0,0))                #reset screen, for clean animation

    levels.makeLevel(screen, img, wallDown, sFloor, floor, tFloor, cFloor)
    direction = move(pygame.key.get_pressed(), player, uAnim, dAnim, lAnim, rAnim,
                     animations = (upAnim, downAnim, leftAnim, rightAnim))

    magic.update()          #projectiles group
    enemyGroup.draw(screen)     #same as blit, but draws the entire group
    magic.draw(screen)          #draws all projectiles to screen
    screen.blit(player.image, player.rect)      #will put the 'hero' in its own group soon
    pygame.display.flip()   #ACTUALLY display all the images
    clock.tick(60)      #all animation and timing is based on this 60fps counter
