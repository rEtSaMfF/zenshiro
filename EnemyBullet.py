import pygame
from PlayerSword import *
from Player import *
from PlayerBomb import *
from PlayerBullet import *

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self,x,y,hspeed,vspeed,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-4,y-4,8,8)
        self.hspd=hspeed
        self.vspd=vspeed
        self.damage=2
        self.reflected=0
        self.imageind=0.0
    def update(self):
        addind=0.0
        addind+=self.game.scrollspeed
        addind+=self.vspd
        addind+=abs(self.hspd/4)
        self.imageind+=(addind/10)
        #moving
        self.rect.move_ip(self.hspd,self.vspd)
        if self.rect.top>480:
            self.game.removeEnemy(self)
    def draw(self,screen):
        drect=pygame.Rect((math.floor(self.imageind)%3)*8,0,8,8)
        screen.blit(self.game.spr_EnemyBullet,self.rect,drect)
    def collision(self,other):
        if isinstance(other,PlayerSword):
            self.game.addPlayerBullet(self.rect.centerx,self.rect.centery,self.hspd*-1,self.vspd*-1)
            self.game.removeEnemy(self)
            if other.player.shoottimer>8:
                other.player.shoottimer=8
        if isinstance(other,PlayerBomb):
            self.game.removeEnemy(self)