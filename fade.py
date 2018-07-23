import pygame

def fadeOut(screen):
    i = 0
    timer = 256
    fadeScreen = screen
    fadeScreen.fill((0,0,0))
    while i < timer:
        screen.fill((0,0,0))
        #fadeScreen.set_alpha(timer)
        #screen.blit(fadeScreen, (0,0))
        #pygame.display.flip()
        timer-=1