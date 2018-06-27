import os
import math
import pygame
from pygame.locals import *

class sprite(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, s=20, image=""):
        super(GameObject, self).__init__()
        if not image:
            image = self.image
        setRect(image, s)
        self.rect.x = x
        self.rect.y = y
        self.isType = "" #"type(obj) is type" can also be used in tandem

    def setRect(self, img, s):
        self.image = pygame.transform.scale(pygame.image.load(img), (s, s)) #s is size of rect
        self.rect = self.image.get_rect()

    def getTop(self):
        return self.rect.top
    def getBottom(self):
        return self.rect.bottom
    def getLeft(self):
        return self.rect.left
    def getRight(self):
        return self.rect.right

    def loadAnimSprite(self, path):
        images = []
        for file in os.listdir(path):
            image = pygame.image.load(path + os.sep + file).convert()
            images.append(image)
        return images

  """ def canMove(self, xCh, yCh, group):
        old_pos = self.rect.x, self.rect.y
        self.rect.x += xCh
        self.rect.y += yCh
        collided_with = pygame.sprite.spritecollideany(self, group)
        if not collided_with:
            self.rect.x = old_pos[0]
            self.rect.y = old_pos[1]
            return True, xCh, yCh, None
        self.rect.y = old_pos[1]
        if pygame.sprite.spritecollideany(self, group):
            xCh = 0
        self.rect.y += yCh
        self.rect.x = old_pos[0]
        if pygame.sprite.spritecollideany(self, group):
            yCh = 0
        if not xCh == 0 and not yCh == 0:
            xCh = 0
            yCh = 0
        self.rect.x = old_pos[0]
        self.rect.y = old_pos[1]
        return False, xCh, yCh, collided_with """


