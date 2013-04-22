import pygame
from Player import *

class Fireball(pygame.sprite.Sprite):
    def __init__(self,x,y,hspeed,vspeed,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-4,y-4,12,12)
        self.hspd=hspeed
        self.vspd=vspeed
        self.damage=4
        self.imageind=0.0
    def update(self):
        #moving
        self.rect.move_ip(self.hspd,self.vspd)
        if self.rect.top>480:
            self.game.removeEnemy(self)
        addind=0.0
        addind+=self.game.scrollspeed
        addind+=self.vspd
        addind+=abs(self.hspd/4)
        self.imageind+=(addind/10)
    def draw(self,screen):
        drect=pygame.Rect((math.floor(self.imageind)%4)*12,0,12,12)
        screen.blit(self.game.spr_Fireball,self.rect,drect)
    def collision(self,other):
        if isinstance(other,Player):
            self.game.removeEnemy(self)
        if isinstance(other,PlayerBomb):
            self.game.removeEnemy(self)