import pygame
from EnemyBullet import *
from PlayerBullet import *
from PlayerSword import *
from PlayerBomb import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,hspeed,vspeed,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-16,y-16,32,32)
        self.hspd=hspeed
        self.vspd=vspeed
        self.hpmax=15
        self.hp=self.hpmax
        self.shootalarm=25
        self.shootalarmmax=25
        self.imageind=0.0
    def update(self):
        #moving
        new_rect=self.rect.move(self.hspd,self.vspd)
        if new_rect.left<120:
            self.hspd+=.5
        elif new_rect.right>360:
            self.hspd-=.5
        self.rect.move_ip(self.hspd,self.vspd)
        if self.rect.top>480:
            self.game.removeEnemy(self)
        if self.hp<=0:
            self.game.removeEnemy(self)
            self.game.player.kills+=1
            self.game.player.score+=self.hpmax*10
            self.game.explode.play(loops=0, maxtime=0)
            self.game.addExplosion(self.rect.left,self.rect.top)
        #shooting
        self.shootalarm-=1
        if self.shootalarm<=0:
            self.shootalarm=self.shootalarmmax
            self.shoot()
            
        addind=0.0
        addind+=self.game.scrollspeed
        addind+=self.vspd
        addind+=abs(self.hspd/4)
        self.imageind+=(addind/10)
    def draw(self,screen):
        drect=pygame.Rect((math.floor(self.imageind)%10)*32,0,32,32)
        screen.blit(self.game.spr_Oni1,self.rect,drect)
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
    def shoot(self):
        self.game.addEnemyBullet(self.rect.centerx,self.rect.bottom,0,8)