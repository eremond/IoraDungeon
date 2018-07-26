import pygame
import player
import sprites
import enemy
import projectiles

"""class boss_bullet(pygame.sprite.Sprite): # only for use with boss class; currently not working...

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("projectiles/boss_bullet.png")
        self.speedy = 3
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > 480:
            self.kill()
"""

class boss(sprites.sprites):

    def __init__(self, image, position, obstacles):
        sprites.sprites.__init__(self, image, position)
        self.boss_health = 20   # 20 health by default
        self.speed = 1
        self.loop = 0
        self.index = 0
        self.target = ""
        self.obstacles = obstacles
        self.orientation = 'left'
        self.direction = 'down'
        if image == 'Enemies/orc.png':
            self.isType = "Orc"
        if image == 'Enemies/yellow_tenta.png':
            self.isType = "Tenta"
        if image == 'Enemies/cat_staff/cat_idle/cat_idle1.png':
            self.isType = "Cat_Staff"
            self.catIdle = self.loadAnimSprite('Enemies/cat_staff/cat_idle')
            self.catThrow = self.loadAnimSprite('Enemies/cat_staff/cat_throw')
            self.animFrames = 6
            self.currentFrame = 0
            self.currentAnim = self.catIdle
            self.boss_health = 20
            self.catloop = 1
            self.moveloop = 0
            self.action = "Idle"

    def update(self, *args):
        # We want bosses to move more slowly, take more hits, and spawn projectiles/enemies


        if self.target.alive():

            collision = self.rect.colliderect(self.target.rect)
            if not collision:
                if self.isType is "Orc":
                    self.speed = 1
                    if self.rect.y<self.target.rect.y and self.inBoundsDown():
                        self.rect.y = self.rect.y + self.speed
                    elif self.rect.y>self.target.rect.y and self.inBoundsUp():
                        self.rect.y = self.rect.y - self.speed
                    if self.rect.x>self.target.rect.x and self.inBoundsLeft():
                        self.rect.x = self.rect.x - self.speed
                        if self.orientation == 'right':
                            self.image = pygame.transform.flip(self.image, True, False)
                        self.orientation = 'left'
                    elif self.rect.x<self.target.rect.x and self.inBoundsRight():
                        self.rect.x = self.rect.x + self.speed
                        if self.orientation == 'left':
                            self.image = pygame.transform.flip(self.image, True, False)
                        self.orientation = 'right'
                if self.isType is "Tenta":
                    self.speed = 2

                    if self.loop < 60:
                        self.rect.x = self.rect.x - self.speed
                        self.rect.y = self.rect.y + self.speed
                    elif self.loop > 60 and self.loop < 120:
                        self.rect.x = self.rect.x + self.speed
                        self.rect.y = self.rect.y + self.speed
                    elif self.loop > 120 and self.loop < 180:
                        self.rect.x = self.rect.x + self.speed
                        self.rect.y = self.rect.y - self.speed
                    elif self.loop > 180 and self.loop < 240:
                        self.rect.x = self.rect.x - self.speed
                        self.rect.y = self.rect.y - self.speed
                    elif self.loop > 240:
                        self.loop = 0
                    self.loop += 1

                if self.isType is "Cat_Staff":
                    self.speed = 2
                    self.update_frame()
                    if self.loop == 180:
                        self.currentAnim = self.catThrow
                    if self.loop > 180:
                        self.catloop += 1
                    if self.catloop % 42 == 0:
                        self.currentAnim = self.catIdle
                        self.loop = 0
                        self.catloop = 0
                    if self.moveloop < 180:
                        self.rect.x = self.rect.x - self.speed
                    elif self.moveloop > 180 and self.moveloop < 360:
                        self.rect.x = self.rect.x + self.speed
                    elif self.moveloop > 360:
                        self.moveloop = 0
                    self.moveloop += 1

            elif self.target.invinc == 0:
                self.target.health -= 1
                self.target.invinc = 60
                self.target.kb = 4
                if self.rect.y<self.target.rect.y and self.inBoundsDown():
                    self.target.kbdy = 20
                elif self.rect.y>self.target.rect.y and self.inBoundsUp():
                    self.target.kbdy = -20
                if self.rect.x>self.target.rect.x and self.inBoundsLeft():
                    self.target.kbdx = -20
                elif self.rect.x<self.target.rect.x and self.inBoundsRight():
                    self.target.kbdx = 20

    def update_frame(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """
        self.currentFrame += 1
        if self.currentFrame >= self.animFrames:
            self.currentFrame = 0
            self.index = (self.index + 1) % len(self.currentAnim)
            self.image = self.currentAnim[self.index]

    def inBoundsDown(self):
        return self.rect.bottom < 480 - 16 and not self.checkTop()

    def inBoundsUp(self):
        return self.rect.top > 16 and not self.checkBottom()

    def inBoundsLeft(self):
        return self.rect.left > 16 and not self.checkRight()

    def inBoundsRight(self):
        return self.rect.right < 640 - 16 and not self.checkLeft()

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
