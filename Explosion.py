import pygame
import math

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.origsurf=self.game.spr_Explosion
        self.xloc=x
        self.yloc=y
        self.rect=pygame.Rect(x-4,y-4,32,32)
        self.hspd=0
        self.vspd=self.game.scrollspeed
        self.lifetime=8
        self.imageind=0.0
    def update(self):
        self.lifetime-=1
        #moving
        self.rect.move_ip(self.hspd,self.vspd)
        if self.lifetime<=0:
            self.game.removeExplosion(self)
        addind=0.0
        addind+=self.game.scrollspeed
        addind+=self.vspd
        addind+=abs(self.hspd/4)
        self.imageind+=(addind/10)
    def draw(self,screen):
        drect=pygame.Rect((math.floor(self.imageind)%4)*32,0,32,32)
        screen.blit(self.game.spr_Explosion,self.rect,drect)
    def collision(self,other):
        if isinstance(other,Player):
            self.game.removeEnemy(self)
        if isinstance(other,PlayerBomb):
            self.game.removeEnemy(self)