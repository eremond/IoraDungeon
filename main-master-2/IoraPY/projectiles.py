import pygame
import player
import sprites
import boss

class projectiles(sprites.sprites):

    def __init__(self, player, image, enemies, position, tabCount = 0):
        sprites.sprites.__init__(self, image, position)
        self.projectileType = tabCount          #tabCount is a variable used in main to cycle through
        self.speed = 4                          #the dif projectiles for player
        self.enemies = enemies      #takes in a list of enemies
        self.direction = player.direction
        self.rect.x, self.rect.y = player.rect.center

    def update(self, *args):
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
                    self.kill()     #kill the projectile
                    self.rect.center = (-5,-5)      #throw the projectile rect out to avoid unnecessary collision
                    if hasattr(enemy, 'boss_health'): #only if the enemy is a boss, the projectile ticks health down to zero
                        enemy.boss_health -= 10
                        if enemy.boss_health == 0:
                            enemy.kill()
                            enemy.rect.center = (-5, -5)
                    elif hasattr(enemy, 'health'): #essentially only if the 'enemy' is the player
                        enemy.health -= 1
                    elif enemy.typeTable.get(enemy.type) == self.projectileType or enemy.typeTable.get(enemy.type) == 0:
                        enemy.kill()                    #do the same for the enemy sprite
                        enemy.rect.center = (-5, -5)    #now supports type!
        else:
            self.kill()     #don't need to worry about the rect since its out of bounds
    
    def checkCoord(self):
        if self.rect.right > 0 and self.rect.left < 640 and self.rect.top < 480 \
           and self.rect.bottom > 0:
            return True
        return False
    
    def collided(self):
        for enemy in self.enemies:      #check the entire list for collision
            if self.rect.colliderect(enemy.rect):
                return (True, enemy)        #if collision, return the collided sprite
        return (False, None)
