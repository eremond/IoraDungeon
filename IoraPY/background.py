import os
import pygame
import time
print(pygame.__path__)
pygame.init()

def makeBackground(screen, walls, sideWalls, sideFloor, floor, topFloor, cornerFloor):
    walls = pygame.transform.scale(walls, (16,16))
    sideWalls = pygame.transform.scale(sideWalls, (16,16))
    sideFloor = pygame.transform.scale(sideFloor, (16,16))
    floor = pygame.transform.scale(floor, (16,16))
    topFloor = pygame.transform.scale(topFloor, (16,16))
    cornerFloor = pygame.transform.scale(cornerFloor, (16,16))

    xCounter = yCounter = 0

    screen.blit(cornerFloor, (16,16))   #top-left corner
    screen.blit(pygame.transform.rotate(cornerFloor,270), (608,16))  #top-right corner
    screen.blit(pygame.transform.rotate(cornerFloor,180), (608,448))   #bottom-right corner
    screen.blit(pygame.transform.rotate(cornerFloor,90), (16,448))   #bottom-left corner

    xCounter = 16                       #draw the walls
    for x in range(38):
        screen.blit(pygame.transform.rotate(sideWalls,90), (xCounter,yCounter))
        xCounter+=16

    yCounter = 464
    xCounter = 16
    for x in range(38):
        screen.blit(pygame.transform.rotate(sideWalls,90), (xCounter,yCounter))
        xCounter+=16
    
    yCounter = 0                        #draw the side walls
    xCounter = 0
    for x in range(30):
        screen.blit(sideWalls, (xCounter, yCounter))
        yCounter+=16
    
    xCounter = 624
    yCounter = 0
    for x in range(30):
        screen.blit(sideWalls, (xCounter, yCounter))
        yCounter+=16

    yCounter = 16
    xCounter = 32
    for x in range(36):                 #draw top-edge floors
        screen.blit(topFloor, (xCounter, yCounter))
        xCounter+=16
    
    yCounter = 448
    xCounter = 32
    for x in range(36):
        screen.blit(pygame.transform.rotate(topFloor,180),(xCounter,yCounter))
        xCounter+=16
    
    yCounter = 32                       #draw side-edge floors
    xCounter = 16
    for x in range(26):
        screen.blit(sideFloor,(xCounter,yCounter))
        yCounter+=16
    
    yCounter = 32
    xCounter = 608
    for x in range(26):
        screen.blit(pygame.transform.rotate(sideFloor,180),(xCounter,yCounter))
        yCounter+=16

    xCounter = 32
    yCounter = 32
    for x in range(36):                 #fill in the floor
        yCounter=32
        for y in range(26):
            screen.blit(floor, (xCounter, yCounter))
            yCounter+=16
        xCounter+=16
