import pygame
import player
import sprites

class chest(sprites.sprites):

	def __init__(self, image, position, obstacles,type,screen):
		sprites.sprites.__init__(self, image, position)
		self.speed = 1
		self.target = 'gem' #Begins with none -- defined by main.py
		self.obstacles = obstacles
		self.screen = screen
		if (type == 1):
			self.type = 'portal'
		if (type == 2):
			self.type = 'item'
		if (type == 3):
			self.type = 'dmg'
		if (type == 4):
			self.type = 'red'
		if (type == 5):
			self.type = 'blue'

	def update(self, *args):
		if self.target != 'gem':
			if self.target.alive(): #Don't do anything if the target (player) is dead.
				collision = self.rect.colliderect(self.target.rect) #Check collision with target (player)
				if collision: #If no collision, move...
					if self.type == 'dmg':
						self.target.health -= 2
					if self.type == 'item':
						self.target.health += 1
					self.kill()
					self.rect.center = (-55,-55) #Put self out-of-bounds -- but not (-5,-5)
