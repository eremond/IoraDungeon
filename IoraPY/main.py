import pygame
import levels
import sprites
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


def move(key, sprite, *animGens, animations):
    uAnim, dAnim, lAnim, rAnim = animGens

    if key[pygame.K_DOWN]:
        if sprite.rect.y < 480-16-sprite.rect.height:
            sprite.rect.y+=2
        return next(dAnim)
    elif key[pygame.K_UP]:
        if sprite.rect.y > 16:
            sprite.rect.y-=2
        return next(uAnim)
    elif key[pygame.K_LEFT]:
        if sprite.rect.x > 16:
            sprite.rect.x-=2
        return next(lAnim)
    elif key[pygame.K_RIGHT]:
        if sprite.rect.x < 640-16-sprite.rect.width:
            sprite.rect.x+=2
        return next(rAnim)
    else:
        return animations[1][1]


#--------------------Set some variables-------------------
width = 640
height = 480
size = width, height
screen = pygame.display.set_mode(size)  #opens the physical screen
clock = pygame.time.Clock()     #keeps track of the fps and stuff
#--------------Create some sprite variables--------------
player = sprites.sprites('Character/DownAnim/Down2.png')
player.isType = "player"
leftAnim = player.loadAnimSprite('Character/LeftAnim')
rightAnim = player.loadAnimSprite('Character/RightAnim')
upAnim = player.loadAnimSprite('Character/UpAnim')
downAnim = player.loadAnimSprite('Character/DownAnim')
uAnim = animGen(upAnim)
dAnim = animGen(downAnim)
lAnim = animGen(leftAnim) 
rAnim = animGen(rightAnim)

#-----------------------Load images-----------------------
img = pygame.image.load('images/bot_wall.jpg').convert()

wallDown = pygame.image.load('images/Side_Walls_05.jpg').convert()

sFloor = pygame.image.load('images/Left_edge_floor.jpg').convert()

floor = pygame.image.load('images/floor.jpg').convert()

tFloor = pygame.image.load('images/Top_edge_floor.jpg').convert()

cFloor = pygame.image.load('images/Left_corner_floor.jpg').convert()



#----------Put character in starting position------------
player.rect.x = int(width/2)
player.rect.y = int(height-player.rect.height-20)

#---------------------Game Loop--------------------------
while 1:
    xCounter = yCounter = 0
    for event in pygame.event.get():    #event handler, just used to quit for now
        if event.type == pygame.QUIT:
            exit()

    screen.fill((0,0,0))                #reset screen, for clean animation

    levels.makeLevel(screen, img, wallDown, sFloor, floor, tFloor, cFloor)
    screen.blit(move(pygame.key.get_pressed(), player, uAnim, dAnim, lAnim, rAnim,
                     animations = (upAnim, downAnim, leftAnim, rightAnim)), player.rect)

    pygame.display.flip()
    clock.tick(60)
