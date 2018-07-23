import pygame


titles = ["Iora Dungeon", "IORA", "Iora's Dungeon"]
menuChoice = 0
menuStrings = [["Start", "Exit", "Endless"], ["KILL", "kill"], ["...", "."]]
finished = False

class titleScreen:
    def __init__(self, secret):
        self.font = pygame.font.Font('font/Connectionserif.otf',32)
        self.titleCard = self.font.render(titles[secret], True, (255,255,255))
        self.titleCardRect = self.titleCard.get_rect()
        self.titleCardRect.center = (640/2, 480/2)
        self.secret = secret
        self.choices = self.font.render(menuStrings[self.secret][menuChoice], True, (255,255,255))
        self.choicesRect = self.choices.get_rect()
        self.choicesRect.center = ((640/2), (480/2)+60)
        self.endless = 0 # Used to tell if the endless mode should launch instead
    def startTitle(self, screen):
        global finished
        global menuChoice
        pygame.event.pump()
        self.choices = self.font.render(menuStrings[self.secret][menuChoice], True, (255,255,255))
        screen.blit(self.titleCard, self.titleCardRect)
        screen.blit(self.choices,self.choicesRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if menuChoice == 1:
                        menuChoice = 0
                        break
                    elif menuChoice == 2:
                        menuChoice = 1
                        break
                    elif menuChoice == 0:
                        menuChoice = 2
                        break
                    #menuChoice+=1
                elif event.key == pygame.K_DOWN:
                    if menuChoice == 1:
                        menuChoice = 2
                        break
                    elif menuChoice == 2:
                        menuChoice = 0
                        break
                    elif menuChoice == 0:
                        menuChoice = 1
                        break

                elif event.key == pygame.K_RETURN:
                    if menuChoice == 0:
                        finished = True
                        break
                    elif menuChoice == 1:
                        exit()
                    elif menuChoice == 2:
                        finished = True
                        self.endless = 1



    def isFinished(self):
        global finished
        return finished
