import sys, pygame
from pygame.locals import *

class Instructions():
    def __init__(self, font, size):
        self.font = font
        self.width = size[0]
        self.height= size[1]
        self.rendered = []
        self.poses = []
        self.howtos = (""
                        , ""
                        , "                     Instructions"
                        , ""
                        , "    Use the arrow keys to move around."
                        , ""
                        , "        Z: Shoot"
                        , "         X: Melee"
                        , "          C: Jump"
						, "           A: Switch Weapon"
                        , "           [SPACE]: Bomb"
                        , ""
                        , ""
                        , "  Press [Enter] to return to the main menu"
                        , "  Hit [ESCAPE] at any time to quit :(")
        for string in range(0,len(self.howtos)):
            self.rendered.append(self.font.render(self.howtos[string], 1, (0, 100, 255)))
        for num in range(0, len(self.howtos)):
            self.poses.append((self.width / 2 - 240, self.height / 2 - (-num * 25) - 140))

def show_howto(font, screen, size, background):
    instr = Instructions(font, size)
    screen.blit(background, (0, 0))
    for item, pos in zip(instr.rendered, instr.poses):
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