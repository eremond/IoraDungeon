import sprites
import pygame
import os

class player(sprites.sprites):

    def __init__(self, image, obstacles, position):	 #image should be a string to the path of the image
        sprites.sprites.__init__(self, image, position)
        self.health = 3
        self.obstacles = obstacles
        self.direction = 'down'
        self.hit = False
        self.speed = 2
        self.leftAnim = self.loadAnimSprite('Character/LeftAnim')
        self.rightAnim = self.loadAnimSprite('Character/RightAnim')
        self.upAnim = self.loadAnimSprite('Character/UpAnim')
        self.downAnim = self.loadAnimSprite('Character/DownAnim')
        self.animQueue = [[self.leftAnim[0], self.leftAnim[1], self.leftAnim[2], self.leftAnim[1]],
                            [self.rightAnim[0], self.rightAnim[1], self.rightAnim[2], self.rightAnim[1]],
                            [self.upAnim[0], self.upAnim[1], self.upAnim[2], self.upAnim[1]],
                            [self.downAnim[0], self.downAnim[1], self.downAnim[2], self.downAnim[1]]]
        self.whichAnim = 3          #default to down animation
        self.animPos = [0,0,0,0]    #left,right,up,down
        self.timer = 0

    def update(self, keys):
        for num in range(len(self.animPos)):
            if self.animPos[num] > 3:
                self.animPos[num] = 0
        if self.health == 0:
            self.kill()
        if keys[pygame.K_DOWN]:
            if self.inBoundsDown():
                self.rect.y+=self.speed
            self.image = self.animQueue[3][self.animPos[3]]
            self.direction = "down"
            self.whichAnim = 3
            if self.timer >= 10:
                self.animPos[3]+=1
                self.timer = 0
            self.timer+=1
        elif keys[pygame.K_UP]:
            if self.inBoundsUp():
                self.rect.y-=self.speed
            self.image = self.animQueue[2][self.animPos[2]]
            self.direction = "up"
            self.whichAnim = 2
            if self.timer >= 10:
                self.animPos[2]+=1
                self.timer = 0
            self.timer+=1
        elif keys[pygame.K_LEFT]:
            if self.inBoundsLeft():
                self.rect.x-=self.speed
            self.image = self.animQueue[0][self.animPos[0]]
            self.direction = "left"
            self.whichAnim = 0
            if self.timer >= 10:
                self.animPos[0]+=1
                self.timer = 0
            self.timer+=1
        elif keys[pygame.K_RIGHT]:
            if self.inBoundsRight():
                self.rect.x+=self.speed
            self.image = self.animQueue[1][self.animPos[1]]
            self.direction = "right"
            self.whichAnim = 1
            if self.timer >= 10:
                self.animPos[1]+=1
                self.timer = 0
            self.timer+=1
        else:
            self.image = self.animQueue[self.whichAnim][1]       #idle state of the direction
            self.timer = 0

    def inBoundsDown(self):
        return self.rect.bottom < 480-16 and not self.checkTop()# and self.notInObject(obstacle)
    
    def inBoundsUp(self):
        return self.rect.top > 16 and not self.checkBottom()# and self.notInObject(obstacle)

    def inBoundsLeft(self):
        return self.rect.left > 16 and not self.checkRight() # and self.notInObject(obstacle)

    def inBoundsRight(self):
        return self.rect.right < 640-16 and not self.checkLeft()

    def checkLeft(self):
        hit = False
        for obstacle in self.obstacles:
            if self.rect.collidepoint(obstacle.rect.midleft) or \
                    self.rect.collidepoint(obstacle.rect.topleft) or \
                    self.rect.collidepoint(obstacle.rect.bottomleft):
                hit = True
        return hit

    def checkRight(self):
        hit = False
        for obstacle in self.obstacles:
            if self.rect.collidepoint(obstacle.rect.midright) or \
                    self.rect.collidepoint(obstacle.rect.topright) or \
                    self.rect.collidepoint(obstacle.rect.bottomright):
                hit = True
        return hit
    
    def checkTop(self):
        hit = False
        for obstacle in self.obstacles:
            if self.rect.collidepoint(obstacle.rect.midtop) or \
                    self.rect.collidepoint(obstacle.rect.topleft) or \
                    self.rect.collidepoint(obstacle.rect.topright):
                hit = True
        return hit

    def checkBottom(self):
        hit = False
        for obstacle in self.obstacles:
            if self.rect.collidepoint(obstacle.rect.midbottom) or \
                    self.rect.collidepoint(obstacle.rect.bottomleft) or \
                    self.rect.collidepoint(obstacle.rect.bottomright):
                hit = True
        return hit
