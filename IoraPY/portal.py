import pygame
import player
import sprites

class portal(sprites.sprites):

	def __init__(self, image, position, obstacles):
		sprites.sprites.__init__(self, image, position)
		self.speed = 1
		self.target = "" #Begins with none -- defined by main.py
		self.obstacles = obstacles

	def update(self, *args):
		if self.target.alive(): #Don't do anything if the target (player) is dead.
			collision = self.rect.colliderect(self.target.rect) #Check collision with target (player)
			if collision: #If no collision, move...
				self.kill()
				self.rect.center = (-55,-55) #Put self out-of-bounds -- but not (-5,-5)

	def inBoundsDown(self):
		return self.rect.bottom < 480-16 and not self.checkTop()

	def inBoundsUp(self):
		return self.rect.top > 16 and not self.checkBottom()

	def inBoundsLeft(self):
		return self.rect.left > 16 and not self.checkRight()

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
