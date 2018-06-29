import os
import pygame

class sprites(pygame.sprite.Sprite):
    def __init__(self, image):     #image should be a string to the path of the image
        pygame.sprite.Sprite.__init__(self)
        self.isType = "" #"type(obj) is type" can also be used in tandem
        self.image = pygame.image.load(image).convert_alpha()   #convert_alpha creates transparent background
        self.rect = self.image.get_rect()

    def transformImage(self, img, x, y):
        self.image = pygame.transform.scale(img, (x, y)) #x, y is new size of image

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
            images.append(pygame.image.load(path + os.sep + file).convert_alpha())
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
