from pygame import *
from sys import *
from Game import *
from Story import *
from Instructions import *
from Credits import *
from HighScore import *
import os

pygame.init()
font = pygame.font.Font(None, 36)
SCREEN = WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode(SCREEN)
background = pygame.image.load('images/title2.png').convert_alpha()

class Menu():
    def __init__(self):
        self.values = ("Start", "Story", "Instructions", "High Scores", "Credits", "Quit")
        self.start = font.render(self.values[0], 1, (200, 200, 200))
        self.story = font.render(self.values[1], 1, (255, 255, 255))
        self.howto = font.render(self.values[2], 1, (255, 255, 255))
        self.highscores = font.render(self.values[3], 1, (255, 255, 255))
        self.credits = font.render(self.values[4], 1, (255, 255, 255))
        self.quit = font.render(self.values[5], 1, (255, 255, 255))
        self.pointer = pygame.image.load("images/pointer.gif").convert()
        self.items = [self.start, self.story, self.howto, self.highscores, self.credits, self.quit]
        self.poses = [(WIDTH * .70, HEIGHT / 2 - 40)
		            ,(WIDTH * .70, HEIGHT / 2 - 20)
                    ,(WIDTH * .70, HEIGHT / 2)
                    ,(WIDTH * .70, HEIGHT / 2 + 20 )
                    ,(WIDTH * .70, HEIGHT / 2 + 40)
                    ,(WIDTH * .70, HEIGHT / 2 + 60)]
        self.pointloc = 0
        self.pointpos = [WIDTH * .70 - 20, self.poses[self.pointloc][1] + 5]
    
    def up(self):
        if self.pointloc == 0:
            self.items[self.pointloc] = font.render(self.values[self.pointloc], 1, (255, 255, 255))
            self.pointloc = len(self.items) - 1
            self.pointpos = [WIDTH * .70 - 20, self.poses[self.pointloc][1] + 6]
            self.items[self.pointloc] = font.render(self.values[self.pointloc], 1, (200, 200, 200))

            
        else:
            self.items[self.pointloc] = font.render(self.values[self.pointloc], 1, (255, 255, 255))
            self.pointloc -= 1
            self.pointpos = [WIDTH * .70 - 20, self.poses[self.pointloc][1] + 6]
            self.items[self.pointloc] = font.render(self.values[self.pointloc], 1, (200, 200, 200))
            
    
    def down(self):
        if self.pointloc == len(self.items) - 1:
            self.items[self.pointloc] = font.render(self.values[self.pointloc], 1, (255, 255, 255))
            self.pointloc = 0
            self.pointpos = [WIDTH * .70 - 20, self.poses[self.pointloc][1] + 6]
            self.items[self.pointloc] = font.render(self.values[self.pointloc], 1, (200, 200, 200))
        else:
            self.items[self.pointloc] = font.render(self.values[self.pointloc], 1, (255, 255, 255))
            self.pointloc += 1
            self.pointpos = [WIDTH * .70 - 20, self.poses[self.pointloc][1] + 6]
            self.items[self.pointloc] = font.render(self.values[self.pointloc], 1, (200, 200, 200))
    
    def execute(self):
        if self.pointloc == 0:
            g=Game()
            while g.cont:
                g.clock.tick(30)
                g.process_events()
                g.update()
                g.collisions()
                g.draw()
                pygame.display.flip()
                
            pygame.quit()
                
           
        elif self.pointloc == 1:
            show_story(font, screen, SCREEN, background)
        elif self.pointloc == 2:
            show_howto(font, screen, SCREEN, background)
        elif self.pointloc == 3:
            show_highscore(font, screen, SCREEN, background)
        elif self.pointloc == 4:
		    show_credits(font, screen, SCREEN, background)
        elif self.pointloc == 5:
            sys.exit()

def show_menu():
    game = Menu()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    sys.exit()
                if event.key==pygame.K_q:
                    sys.exit()
                if event.key == K_DOWN:
                    game.down()
                elif event.key == K_UP:
                    game.up()
                elif event.key == K_RETURN:
                    game.execute()
        
        screen.blit(background, (0, 0))
        for item, pos in zip(game.items, game.poses):
            screen.blit(item, pos)
        screen.blit(game.pointer, game.pointpos)
    
        pygame.display.flip()
        pygame.time.delay(100)
