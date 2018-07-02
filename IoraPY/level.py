import pygame
import sprites
import player
import projectiles
import pygame

class level():
    def __init__(self, design):      #design is a 2d list
        self.boxGroup = pygame.sprite.Group()
        self.boxes = []
        self.design = design
        self.isPuzzleDone = False
        


    def makeLevel(self):
        counter = 0
        xSpot = 16
        ySpot = 16
        for x in self.design:
            for y in x:
                print(y)
                if y is '#':
                    self.boxes.append(sprites.sprites('Obstacles/box.png', (xSpot, ySpot)))
                    self.boxGroup.add(self.boxes[counter])
                    counter+=1
                xSpot+=48
            xSpot=0
            ySpot+=58
            
    def isComplete(self, enemyGroup):           #checks to see if all enemies are cleared out
        print(enemyGroup)
        if not enemyGroup:
            return True
        return False
