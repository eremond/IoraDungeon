import pygame
import sprites
import projectiles
import pygame
import enemy
import boss
import portal
import chest

class level():
	def __init__(self, design, enemies,chests,portal,screen):	  #design is a 2d list
		self.boxGroup = pygame.sprite.Group()
		self.boxes = []
		self.enemies = enemies
		self.design = design
		self.chests = chests
		self.screen = screen
		self.exit = portal
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
					self.enemies.append(enemy.enemy('Enemies/slime.png', (xSpot, ySpot), self.boxes, 0)) #Last parameter is enemy type.
				elif y is '1':
					self.enemies.append(enemy.enemy('Enemies/flame.png', (xSpot, ySpot), self.boxes, 1))
				elif y is 'O':
					self.enemies.append(boss.boss('Enemies/orc.png', (xSpot, ySpot), self.boxes))
				elif y is 'S':
					self.enemies.append(boss.boss('Enemies/yellow_tenta.png', (xSpot, ySpot), self.boxes))
				elif y is '~':
					self.enemies.append(boss.boss('Enemies/cat_staff/cat_idle/cat_idle1.png', (xSpot, ySpot), self.boxes))
				elif y is '¡':
					self.boxes.append(sprites.sprites('Obstacles/torch.gif', (xSpot, ySpot)))
					self.boxGroup.add(self.boxes[counter])
				elif y is '!':
					self.exit.append(portal.portal('images/portal.png', (xSpot, ySpot), self.boxes))
				elif y is '*':
					self.chests.append(chest.chest('Obstacles/chest.png', (xSpot, ySpot), self.boxes,1,self.screen))
				elif y is '%':
					self.chests.append(chest.chest('Obstacles/chest.png', (xSpot, ySpot), self.boxes,2,self.screen))
				elif y is '$':
					self.chests.append(chest.chest('Obstacles/chest.png', (xSpot, ySpot), self.boxes,3,self.screen))
				elif y is 'R':
					self.chests.append(chest.chest('Obstacles/red.png', (xSpot, ySpot), self.boxes,4,self.screen))
				elif y is 'B':
					self.chests.append(chest.chest('Obstacles/blue.png', (xSpot, ySpot), self.boxes,5,self.screen))
				xSpot+=48
			xSpot=0
			ySpot+=58
		#Reset counters to iterate through again -- this time for spawning enemies.
		#(Obstacles list must be passed in for each enemy.)
		#Leaving this in case something breaks
		"""
		xSpot = 16
		ySpot = 16
		for x in self.design:
			for y in x:
				if y is 'X':
					self.enemies.append(enemy.enemy('Enemies/slime.png', (xSpot, ySpot), self.boxes))
				if y is 'O':
					self.enemies.append(boss.boss('Enemies/orc.png', (xSpot, ySpot), self.boxes))
				xSpot+=48
			xSpot=0
			ySpot+=58"""

	def isComplete(self, enemyGroup):		   #checks to see if all enemies are cleared out
		print(enemyGroup)
		if not enemyGroup:
			return True
		return False
