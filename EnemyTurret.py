import pygame
from EnemyBullet import *
from PlayerBullet import *
from PlayerSword import *
import math

class EnemyTurret(pygame.sprite.Sprite):
    def __init__(self,x,y,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-16,y-16,32,32)
        self.hspd=0
        self.vspd=0
        self.hpmax=26
        self.hp=self.hpmax
        #shooting stuff
        self.shootalarmmax=48
        self.shootalarm=self.shootalarmmax
        self.bulletspeed=6
        self.aimdir=0
        self.imageind=0.0
    def update(self):
        #moving
        self.vspd=self.game.scrollspeed
        self.rect.move_ip(self.hspd,self.vspd)
        
        if self.rect.top>480:
            self.game.removeEnemy(self)
        if self.hp<=0:
            self.game.removeEnemy(self)
            self.game.player.kills+=1
            self.game.player.score+=self.hpmax*10
            self.game.explode.play(loops=0, maxtime=0)
            self.game.addExplosion(self.rect.left,self.rect.top)
        #aiming
        tox=self.game.player.rect.centerx
        toy=self.game.player.rect.centery
        self.aim(tox,toy)
        
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
        drect=pygame.Rect((math.floor(self.imageind)%6)*32,0,32,32)
        screen.blit(self.game.spr_EnemyTurret,self.rect,drect)
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
        thspd=math.cos(self.aimdir)*self.bulletspeed
        tvspd=math.sin(self.aimdir)*self.bulletspeed
        self.game.addEnemyBullet(self.rect.centerx,self.rect.centery,tvspd,thspd)
    def aim(self,x,y):
        self.aimdir=math.atan2(self.rect.centerx-x,self.rect.centery-y)+math.pi