import pygame
import math

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self,x,y,hspeed,vspeed,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-7,y-11,8,8)
        self.hspd=hspeed
        self.vspd=vspeed
        self.damage=5
        self.imageind=0.0
    def update(self):
        #moving
        self.rect.move_ip(self.hspd,self.vspd)
        if self.rect.top<-48:
            self.game.removePlayerBullet(self)
        addind=0.0
        addind+=self.game.scrollspeed
        addind+=self.vspd*-1
        addind+=abs(self.hspd/4)
        self.imageind+=(addind/10)
    def draw(self,screen):
        drect=pygame.Rect((math.floor(self.imageind)%3)*8,0,8,8)
        screen.blit(self.game.spr_PlayerBullet,self.rect,drect)