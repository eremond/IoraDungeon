import pygame
import player
import sprites
import boss

class projectiles(sprites.sprites):

    def __init__(self, player, image, enemies,chests, position,type):
        sprites.sprites.__init__(self, image, position)
        self.speed = 4
        self.enemies = enemies      #takes in a list of enemies
        self.chests = chests
        self.direction = player.direction
        self.type = type
        self.rect.x, self.rect.y = player.rect.center
        self.player = player
        self.return_loop = 0

    def update(self, *args):
        collision, enemy = self.collided()
        collision_gem, gem = self.collided_gem()
        if self.checkCoord():       #make sure the projectile isnt out of bounds yet
            if (not collision and not collision_gem):
                if self.direction is "down":
                    self.rect.y+=self.speed
                if self.direction is "up":
                    self.rect.y-=self.speed
                if self.direction is "left":
                    self.rect.x-=self.speed
                if self.direction is "right":
                    self.rect.x+=self.speed
                if self.direction is "targeting":
                    self.speed = 3
                    if self.return_loop < 95:
                        if self.rect.y < self.enemies[0].rect.y:
                            self.rect.y+=self.speed
                        elif self.rect.y > self.enemies[0].rect.y:
                            self.rect.y -= self.speed
                        if self.rect.x > self.enemies[0].rect.x:
                            self.rect.x -= self.speed
                        elif self.rect.x < self.enemies[0].rect.x:
                            self.rect.x += self.speed
                    if self.return_loop >= 95:
                        if self.rect.y < self.player.rect.y:
                            self.rect.y+=self.speed
                        elif self.rect.y > self.player.rect.y:
                            self.rect.y -= self.speed
                        if self.rect.x > self.player.rect.x:
                            self.rect.x -= self.speed
                        elif self.rect.x < self.player.rect.x:
                            self.rect.x += self.speed
                        if self.rect.y == self.player.rect.y and self.rect.x == self.player.rect.x:
                            self.kill()
                            self.return_loop = 0
                    self.return_loop += 1
            elif(collision):
                if enemy.alive():
                    self.kill()     #kill the projectile, enemy
                    self.rect.center = (-5,-5)      #throw the projectile recet out to avoid unnecessary collision
                    if hasattr(enemy, 'boss_health'): #only if the enemy is a boss, the projectile ticks health down to zero
                        enemy.boss_health -= 1
                        if enemy.boss_health == 0:
                            enemy.kill()
                            enemy.rect.center = (-5, -5)
                    elif hasattr(enemy, 'health'): #essentially only if the 'enemy' is the player
                        enemy.health -= 1
            elif(collision_gem):
                self.kill()
                if gem.alive():
                    if (self.type == gem.type):
                        gem.kill()                    #do the same for the enemy sprite
                        gem.rect.center = (-5, -5)

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

    def collided_gem(self):
        for chest in self.chests:      #check the entire list for collision
            if self.rect.colliderect(chest.rect):
                return (True, chest)        #if collision, return the collided sprite
        return (False, None)
