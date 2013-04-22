import pygame
from PlayerBomb import *

class Laser(pygame.sprite.Sprite):
    def __init__(self,x,y,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.laser_surf=self.game.spr_Laser
        self.original=self.laser_surf
        self.rect=self.laser_surf.get_rect()
        self.centerx=x
        self.centery=y
        self.damage=100
        self.lifetime=90
        self.rotatetime=30
        self.angle=0
    def update(self):
        self.lifetime-=1
        self.rotatetime-=1
        if self.lifetime<=0:
            self.game.removeEnemy(self)
        if self.rotatetime>=0:
            self.rotate()
    def draw(self,screen):
        if self.angle>=0:
            self.rect.topleft=(self.centerx,self.centery)
        elif self.angle<0:
            self.rect.topright=(self.centerx,self.centery)
        screen.blit(self.laser_surf,self.rect)
    def collision(self,other):
        if isinstance(other,PlayerBomb):
            self.game.removeEnemy(self)
    def rotate(self):
        if(self.centerx<240):
            self.angle+=1
        elif(self.centerx>240):
            self.angle-=1
        self.laser_surf=pygame.transform.rotate(self.original,self.angle)
        self.rect=self.laser_surf.get_rect()
        