import pygame
import random
import math
class MinibossBody(pygame.sprite.Sprite):
    def __init__(self,mini,creator):
        pygame.sprite.Sprite.__init__(self)
        self.miniboss=mini
        self.rect=pygame.Rect(self.miniboss.rect.centerx,self.miniboss.rect.top,160,96)
        self.game=creator
        self.rect=pygame.Rect(0,-164,480,164)
        self.hspd=0
        self.vspd=1
        self.emergetime=164
        self.imageind=0.0
    def update(self):
        self.rect.centerx=self.miniboss.rect.right+145
        self.rect.top=self.miniboss.rect.top
        if self.miniboss.hp<=0:
            self.game.removeBossBase(self)
            self.game.addExplosion(self.rect.left,self.rect.top)
        addind=0.0
        addind+=self.game.scrollspeed
        addind+=self.vspd*-1
        addind+=abs(self.hspd/4)
        self.imageind+=(addind/10)
            
    def draw(self,screen):
        drect=pygame.Rect((math.floor(self.imageind)%10)*160,0,160,96)
        screen.blit(self.game.spr_MinibossBody,self.rect,drect)
    def reduceHealth(self,damage):
        self.hp-=damage