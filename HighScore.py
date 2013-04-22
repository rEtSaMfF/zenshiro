import sys, pygame
from pygame.locals import *

class HighScore():
    def __init__(self, font, size):
        self.font = font
        self.width = size[0]
        self.height = size[1]
        self.rendered = []
        self.poses = []
        self.rendered2 = []
        self.poses2 = []
        self.rendered.append(self.font.render("Press [Enter] to return to the main menu", 1, (0, 100, 255)))
        self.poses.append((75, 450))
        try:
            f = open('HighScores.txt')
        except IOError:
            return
        s = f.read()
        s = s[:-1]
        s = s.split("\n")
        b = []
        for a in s:
            b.append(a.split("\t"))
        for a in b:
            a[0] = int(a[0])
        b = sorted(b, reverse=True)
        b = b[:10]
        # self.names = ""
        # for a in b:
            # self.names = self.names + a[1] + "\n"
        # self.scores = ""
        # for a in b:
            # self.scores = self.scores + str(a[0]) + "\n"
        # print self.names
        # print self.scores
        for a in b:
            self.rendered.append(self.font.render(a[1], 1, (0, 100, 255)))
            self.rendered.append(self.font.render(str(a[0]), 1, (0, 100, 255)))
        for a in range(len(b)):
            self.poses.append((50, self.height/2 - (-a*25) - 80))
            self.poses.append((500, self.height/2 - (-a*25) - 80))
        for a in range(len(b)):
            self.rendered.append(self.font.render(str(a+1)+".", 1, (0,0,0)))
            self.poses.append((5, self.height/2 - (-a*25) - 80))

def show_highscore(font, screen, size, background):
    hs = HighScore(font, size)
    screen.blit(background, (0, 0))
    for item, pos in zip(hs.rendered, hs.poses):
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