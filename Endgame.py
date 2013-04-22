import sys
import pygame
import Menu
from Menu import *
from pygame.locals import *


class Endgame():
    def __init__(self, font, size):
        self.font = font
        self.width = size[0]
        self.height= size[1]
        self.rendered = []
        self.poses = []
        self.howtos = (""
        , ""
        , "                     The End?"
        , ""
        , "  As the dragon's head explodes, Zenshiro braces"
		, "  himself for the ride back to NeoTokyo. A quick"
		, "  glint of light catches Zenshiro's eye. It's an escape"
		, "  pod blasting off from the dragon's ruined body."
		, "  The insignia on the side is strangely familiar"
		, "  to Zenshiro. 'Brother, I thought you were dead!'"
		, "  thought Zenshiro."
        , ""
        , ""
        , "  'It seems we are destined to meet again, and soon...'")
        for string in range(0,len(self.howtos)):
            self.rendered.append(self.font.render(self.howtos[string], 1, (255, 255, 255)))
        for num in range(0, len(self.howtos)):
            self.poses.append((self.width / 2 - 335, self.height / 2 - (-num * 25) - 275))

def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0),
                    ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
    pygame.draw.rect(screen, (255,255,255),
                    ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),
                    ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.flip()
               
def saveScore(name, score):
    f = open('HighScores.txt', 'a')
    #f.write(name + '\t' + str(score) + '\n')
    f.write(str(score) + '\t' + name + '\n')
    f.close()
        
def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass
        
def enterName(self):
    # Getting player name
    font = self.game.font
    textplease = font.render("Please type your name now", 1, (0,0,0))
    textpleasepos = (self.width/4, self.height/2-70)
    background = pygame.image.load('images/title.png').convert_alpha()
    self.game.screen.blit(background,(0,0))
    self.game.screen.blit(textplease, textpleasepos)
    pygame.display.flip()
    getname=True
    current_string = []
    while getname:
        if len(current_string)>=25:
            getname=False
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == K_RETURN and len(current_string)>=1: # change this when we don't want blank names
            getname=False
        elif inkey == K_MINUS:
            current_string.append("_")
        elif inkey == K_SPACE:
            current_string.append(" ")
        elif inkey == K_RSHIFT or inkey == K_LSHIFT or inkey >127 or inkey < 97:
            continue
        elif inkey>=97 and inkey <= 127:
            current_string.append(chr(inkey-32))
        else:
            current_string.append(chr(inkey))
        display_box(self.game.screen, string.join(current_string,""))
    name=string.join(current_string,"")
    saveScore(name,self.score)
    textname = font.render(name, 1, (0,0,0))
    textnamepos = (0,self.height-60)
    textscore = font.render("Score: " + str(self.score), 1, (0,0,0))
    textscorepos = (0,self.height-30)  
    Menu.show_menu()
               
def gameOver(self):
    background = pygame.image.load('images/GameOver.png').convert_alpha()
    self.game.screen.blit(background,(0,0))
    pygame.mixer.music.load("sounds/failure.wav")
    pygame.mixer.music.play()
    font = pygame.font.Font(None, 50)
    
    textcont = font.render("CONTINUE", 1, (255,255,255))
    textcontpos = (self.width * .7, self.height/2-10)
    textquit = font.render("QUIT", 1, (255,255,255))
    textquitpos = (self.width * .7, self.height/2+20)
    pygame.display.flip()
    pointer = pygame.image.load("images/pointer.gif").convert()
    cont = True
    pointpos = (self.width* .65, self.height /2)
    pygame.display.flip()
    
    # continue or main menu?
    while 1:
        self.game.screen.blit(background,(0,0))
        #self.game.screen.blit(textname, textnamepos)
        #self.game.screen.blit(textscore, textscorepos)
        self.game.screen.blit(textcont, textcontpos)
        self.game.screen.blit(textquit, textquitpos)
        self.game.screen.blit(pointer, pointpos)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    sys.exit()
                if event.key==pygame.K_q:
                    sys.exit()
                if event.key == K_DOWN or event.key == K_UP:
                    if cont:
                        textcont = font.render("CONTINUE", 1, (255,255,255))
                        textquit = font.render("QUIT", 1, (200,200,200))
                        pointpos = (self.width* .65, self.height /2+30)
                    else:
                        textcont = font.render("CONTINUE", 1, (200,200,200))
                        textquit = font.render("QUIT", 1, (255,255,255))
                        pointpos = (self.width* .65, self.height /2)
                    cont=not cont
                elif event.key == K_RETURN:
                    if cont:
                        self.lives = 3
                        self.score = 0
                        self.bombs = 3
                        self.swords = 100
                        self.new=0
                        return
                    else:
                        enterName(self)
            
def show_end(game):
    font = game.font
    screen = game.screen
    size = [screen.get_rect().width,screen.get_rect().height]
    game.screen.fill((0,0,0))
    end = Endgame(font, size)
    for item, pos in zip(end.rendered, end.poses):
        screen.blit(item, pos)
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    enterName(game.player)
                if event.key == K_BACKSPACE:
                    enterName(game.player)
                if event.key == K_ESCAPE:
                    sys.exit()
                if event.key == K_q:
                    sys.exit()