import pygame
import player
import sprites
import enemy
import projectiles
import random

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

    def __init__(self, image, position, babies, target):        #babies is a cute way of saying lesser enemies
        sprites.sprites.__init__(self, image, position)
        self.img = image        #only for testing, can be removed when we add more bosses
        self.pos = position     #same with this
        self.boss_health = 20   # 20 health by default
        self.speed = 1
        self.target = target    #what the boss needs to attack
        self.enemies = babies
        #bosses don't need to check for obstacles:
        #theyre the only thing in the level
        #self.obstacles = obstacles
        self.orientation = 'left'
        self.direction = 'down'
    
    def update(self, *args):
        # We want bosses to move more slowly, take more hits, and spawn projectiles/enemies


        if self.target.alive():
            collision = self.rect.colliderect(self.target.rect)
            if not collision:
                if self.rect.y < self.target.rect.y and self.inBoundsDown():
                    self.rect.y = self.rect.y + self.speed
                elif self.rect.y > self.target.rect.y and self.inBoundsUp():
                    self.rect.y = self.rect.y - self.speed
                if self.rect.x > self.target.rect.x and self.inBoundsLeft():
                    self.rect.x = self.rect.x - self.speed
                    if self.orientation == 'right':
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.orientation = 'left'
                elif self.rect.x < self.target.rect.x and self.inBoundsRight():
                    self.rect.x = self.rect.x + self.speed
                    if self.orientation == 'left':
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.orientation = 'right'

            elif self.target.invinc == 0:
                self.target.health -= 1
                self.target.invinc = 60
                self.target.kb = 4
                if self.rect.y < self.target.rect.y and self.inBoundsDown():
                    self.target.kbdy = 20
                elif self.rect.y > self.target.rect.y and self.inBoundsUp():
                    self.target.kbdy = -20
                if self.rect.x > self.target.rect.x and self.inBoundsLeft():
                    self.target.kbdx = -20
                elif self.rect.x < self.target.rect.x and self.inBoundsRight():
                    self.target.kbdx = 20

        #Maybe some they have different frames and knockback

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
        for enemy in self.enemies:
            if self.rect.collidepoint(enemy.rect.midleft) or \
                    self.rect.collidepoint(enemy.rect.topleft) or \
                    self.rect.collidepoint(enemy.rect.bottomleft):
                hit = True
        return hit

    def checkRight(self):
        hit = False
        for enemy in self.enemies:
            if self.rect.collidepoint(enemy.rect.midright) or \
                    self.rect.collidepoint(enemy.rect.topright) or \
                    self.rect.collidepoint(enemy.rect.bottomright):
                hit = True
        return hit

    def checkTop(self):
        hit = False
        for enemy in self.enemies:
            if self.rect.collidepoint(enemy.rect.midtop) or \
                    self.rect.collidepoint(enemy.rect.topleft) or \
                    self.rect.collidepoint(enemy.rect.topright):
                hit = True
        return hit

    def checkBottom(self):
        hit = False
        for enemy in self.enemies:
            if self.rect.collidepoint(enemy.rect.midbottom) or \
                    self.rect.collidepoint(enemy.rect.bottomleft) or \
                    self.rect.collidepoint(enemy.rect.bottomright):
                hit = True
        return hit