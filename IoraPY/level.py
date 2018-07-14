import pygame
import sprites
import projectiles
import pygame
import enemy

class level():
	def __init__(self, design, enemies):	  #design is a 2d list
		self.boxGroup = pygame.sprite.Group()
		self.boxes = []
		self.enemies = enemies
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
				elif y is 'X':
					self.enemies.append(enemy.enemy('Enemies/slime.png', (xSpot, ySpot), self.boxes))
				xSpot+=48
			xSpot=0
			ySpot+=58
		#Reset counters to iterate through again -- this time for spawning enemies.
		#(Obstacles list must be passed in for each enemy.)
		# Leaving this in case something breaks
		'''
		xSpot = 16
		ySpot = 16
		for x in self.design:
			for y in x:
				if y is 'X':
					self.enemies.append(enemy.enemy('Enemies/slime.png', (xSpot, ySpot), self.boxes))
				xSpot+=48
			xSpot=0
			ySpot+=58'''
			
	def isComplete(self, enemyGroup):		   #checks to see if all enemies are cleared out
		print(enemyGroup)
		if not enemyGroup:
			return True
		return False
