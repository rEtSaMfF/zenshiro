import pygame
from EnemySword import*
from PlayerBullet import *
from PlayerSword import *
from PlayerBomb import *

class MeleeEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y,hspeed,vspeed,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-16,y-16,32,64)
        self.hspd=hspeed
        self.vspd=vspeed
        self.hpmax=10
        self.hp=self.hpmax
        self.hasSword=False
        self.alive=True
        self.imageind=0.0
    def update(self):
        addind=0.0
        addind+=self.game.scrollspeed
        addind+=self.vspd
        addind+=abs(self.hspd/4)
        self.imageind+=(addind/10)
        #moving
        new_rect=self.rect.move(self.hspd,self.vspd)
        if new_rect.left<120:
            self.hspd+=.5
        elif new_rect.right>360:
            self.hspd-=.5
        self.rect.move_ip(self.hspd,self.vspd)
        if self.rect.top>490:
            self.game.removeEnemy(self)
            self.alive=False
        if self.hp<=0:
            self.game.removeEnemy(self)
            self.alive=False
            self.game.player.kills+=1
            self.game.player.score+=self.hpmax*10
            self.game.addExplosion(self.rect.left,self.rect.top)
        #sword timer
        if self.hasSword!=True:
            self.sword()
    def draw(self,screen):
        drect=pygame.Rect((math.floor(self.imageind)%7)*32,0,32,64)
        screen.blit(self.game.spr_Samurai,self.rect,drect)
    def collision(self,other):
        if isinstance(other,PlayerBullet):
            self.hp-=other.damage
            self.game.removePlayerBullet(other)
        if isinstance(other,PlayerSword):
            self.hp-=other.damage
            if other.player.shoottimer>8:
                other.player.shoottimer=8
        if isinstance(other,PlayerBomb):
            self.hp-=other.damage          
    def sword(self):
        self.game.addEnemySword(64,32,self)
        self.hasSword=True