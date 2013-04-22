# -*- coding: cp1252 -*-
import sys, pygame
from pygame.locals import *

class Credits():
    def __init__(self, font, size):
        self.font = font
        self.width = size[0]
        self.height = size[1]
        self.rendered = []
        self.poses = []
        self.howtos = (""
                        , ""
                        , "                          Credits"
                        , "                        Team Schmucks"
                        , "     Programming           Sean McLoughlin"
                        , "                                       Calvin Spencer Kwok"
                        , "                                       Curtis Antolik"
                        , "                                       Jacob Knipfing"
                        , ""
                        , "     Art                             Patrick \"Smee\" Buford"
                        , "                                       Clyde Austin Drexler"
                        , "Music:Remix ofSilver Forest-technical difficulties"
						, "Bulletholes on Game Over Screen by"
						, "MacProductions on officialpsds.com"
						
                        , "Press [Enter] to return to the main menu")
        for string in range(0,len(self.howtos)): 
            self.rendered.append(self.font.render(self.howtos[string], 1, (0, 100, 255)))
        for num in range(0, len(self.howtos)):
            self.poses.append((self.width / 2 - 240, self.height / 2 - (-num * 25) - 140))

def show_credits(font, screen, size, background):
    crdts = Credits(font, size)
    screen.blit(background, (0, 0))
    for item, pos in zip(crdts.rendered, crdts.poses):
        screen.blit(item, pos)
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return
                if event.key == K_BACKSPACE:
                    return
                if event.key == K_ESCAPE:
                    sys.exit()
                if event.key == K_q:
                    sys.exit()