import pygame
import sprites

class projectiles(sprites.sprites):

    def __init__(self, player, image, direction, enemies):
        sprites.sprites.__init__(self, image)
        self.speed = 4
        self.enemies = enemies      #takes in a list of enemies
        self.direction = direction
        self.rect.x, self.rect.y = player.rect.center

    def update(self):
        collision, enemy = self.collided()
        if self.checkCoord():       #make sure the projectile isnt out of bounds yet
            if not collision:
                if self.direction is "down":
                    self.rect.y+=self.speed
                if self.direction is "up":
                    self.rect.y-=self.speed
                if self.direction is "left":
                    self.rect.x-=self.speed
                if self.direction is "right":
                    self.rect.x+=self.speed
            else:
                if enemy.alive():
                    self.kill()     #kill the projectile, enemy
                    self.rect.center = (-5,-5)      #throw the projectile recet out to avoid unnecessary collision
                    enemy.kill()                    #do the same for the enemy sprite
                    enemy.rect.center = (-5, -5)
        else:
            self.kill()     #don't need to worry about the rect since its out of bounds
    
    def checkCoord(self):
        if self.rect.right > 0 and self.rect.left < 640 and self.rect.top < 480 \
           and self.rect.bottom > 0:
            return True
        return False
    
    def collided(self):
        for enemy in self.enemies:      #check the entire list for collision
            print(enemy)
            if self.rect.colliderect(enemy.rect):
                return (True, enemy)        #if collision, return the collided sprite
        return (False, None)
