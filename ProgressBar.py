import pygame
import random
import math
class ProgressBar(pygame.sprite.Sprite):
    def __init__(self,x,y,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.nextupdate=0
        self.progress=0
    def update(self):
        if self.game.scrollspeed!=0:
            self.nextupdate+=1
        if self.nextupdate>=12:
            self.progress+=1
    def draw(self,screen):
        screen.blit(self.game.spr_Dragon_Turret,self.rect)
        self.health_surf = pygame.image.load("./images/progressbar.png").convert_alpha()
        self.health_rect=self.health_surf.get_rect()
        if self.hp>=0:
            self.newhealth_surf=pygame.transform.scale(self.health_surf,(self.health_rect.right*(self.progress*2),self.health_rect.bottom))
        self.health_rect.top = 0
        self.health_rect.right=200
        self.game.screen.blit(self.newhealth_surf,self.health_rect)