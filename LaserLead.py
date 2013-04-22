import pygame
from PlayerBomb import *

class LaserLead(pygame.sprite.Sprite):
    def __init__(self,x,y,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.laser_surf=self.game.spr_LeadLaser
        self.original=self.laser_surf
        self.rect=self.laser_surf.get_rect()
        self.centerx=x
        self.centery=y
        self.damage=100
        self.lifetime=60
        self.angle=0
    def update(self):
        self.lifetime-=1
        if self.lifetime<=0:
            self.game.removeEnemy(self)
            self.game.addLaser(self.centerx,self.centery)
    def draw(self,screen):
        self.rect.topleft=(self.centerx,self.centery)
        screen.blit(self.laser_surf,self.rect)
    def collision(self,other):
        if isinstance(other,PlayerBomb):
            self.game.removeEnemy(self)