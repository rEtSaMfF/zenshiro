import pygame
import random
import math
from EnemyBullet import *
from PlayerBullet import *
from PlayerSword import *
class Eye(pygame.sprite.Sprite):
    def __init__(self,x,y,boss,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.boss=boss
        self.xpos=x
        self.rect=pygame.Rect(x,y,64,64)
        self.hspd=0
        self.vspd=1
        self.emergetime=164
        self.hpmax=200
        self.hp=self.hpmax
        self.bulletspeed=8
        self.shootalarm=30
        self.shootalarmmax=30
        self.laseralarm=180
        self.laseralarmmax=600
        self.aimdir=0
        self.currentweakspot=1
    def update(self):
        #moving
        new_rect=self.rect.move(self.hspd,self.vspd)
        self.emergetime-=1
        if self.emergetime<=0:
            self.vspd=0
        self.rect.move_ip(self.hspd,self.vspd)
        if self.hp<=0:
            self.game.removeBoss(self)
            #self.game.resumeScrolling()
            self.game.player.kills+=1
            self.game.player.score+=self.hpmax*10
            self.game.eyeDeath()
            self.game.explode.play(loops=0, maxtime=0)
            self.game.addExplosion(self.rect.left,self.rect.top)
        #shooting
        if self.currentweakspot>0:
            self.shootalarm-=1
            if self.shootalarm<=0:
                shottype=random.randint(0,3)
                self.shootalarm=self.shootalarmmax
                self.shoot(shottype)
        #lasers
        self.laseralarm-=1
        if self.laseralarm<=0:
           self.laseralarm=self.laseralarmmax
           self.laser()
            

    def draw(self,screen):
        if self.xpos<240:
            if self.currentweakspot==1:
                screen.blit(self.game.spr_BossEyeL,self.rect)   
            if self.currentweakspot==-1:
                screen.blit(self.game.spr_BossEyeLDeact,self.rect)
        if self.xpos>240:
            if self.currentweakspot==1:
                screen.blit(self.game.spr_BossEyeR,self.rect)   
            if self.currentweakspot==-1:
                screen.blit(self.game.spr_BossEyeRDeact,self.rect)
    def collision(self,other):
        if self.currentweakspot>0:
            if isinstance(other,PlayerBullet):
                self.hp-=other.damage
                self.boss.reduceHealth(other.damage)
                self.game.removePlayerBullet(other)
            if isinstance(other,PlayerSword):
                self.hp-=other.damage
                self.boss.reduceHealth(other.damage)
                if other.player.shoottimer>8:
                    other.player.shoottimer=8
            if isinstance(other,PlayerBomb):
                self.hp-=other.damage
                self.boss.reduceHealth(other.damage)
    def shoot(self,type):
        if type==0:
            self.game.addEnemyBullet(self.rect.centerx,self.rect.bottom,0,8)
            self.game.addEnemyBullet(self.rect.centerx-10,self.rect.bottom,-1,8)
            self.game.addEnemyBullet(self.rect.centerx+10,self.rect.bottom,1,8)
        elif type==1:
            self.game.addEnemyBullet(self.rect.centerx, self.rect.bottom, 0, 4)
            self.game.addEnemyBullet(self.rect.centerx-10,self.rect.bottom,-1,4)
            self.game.addEnemyBullet(self.rect.centerx+10,self.rect.bottom,1,4)
        elif type==2:
            tox=self.game.player.rect.centerx
            toy=self.game.player.rect.centery
            self.aim(tox,toy)
            thspd=math.cos(self.aimdir)*self.bulletspeed
            tvspd=math.sin(self.aimdir)*self.bulletspeed
            self.game.addEnemyBullet(self.rect.centerx,self.rect.centery,tvspd,thspd)
            self.game.addEnemyBullet(self.rect.centerx-10,self.rect.centery-10,tvspd,thspd)
            self.game.addEnemyBullet(self.rect.centerx+10,self.rect.centery-10,tvspd,thspd)
        elif type==3:
            self.game.addHomingMissile(self.rect.centerx,self.rect.centery,0,8)
            self.game.addHomingMissile(self.rect.centerx-30,self.rect.centery-30,0,8)
            self.game.addHomingMissile(self.rect.centerx+30, self.rect.centery-30,0,8)
            
    def laser(self):
            self.game.addLaserLead(self.rect.centerx, self.rect.centery)
            
    #def fire(self):
      #  if self.volleytimer!=3:
        #    self.game.addFireball(self.rect.centerx, self.rect.bottom,0,8)
          #  self.volleytimer+=1
        #elif self.volleytimer==3:
          #  self.game.addFireball(self.rect.centerx-10, self.rect.bottom,-1,8)
            #self.game.addFireball(self.rect.centerx-20, self.rect.bottom,-2,8)
           # self.game.addFireball(self.rect.centerx+10, self.rect.bottom,1,8)
            #self.game.addFireball(self.rect.centerx+20, self.rect.bottom,2,8)
            #self.game.addFireball(self.rect.centerx, self.rect.bottom,0,8)
            #self.volleytimer=0
    def aim(self,x,y):
        self.aimdir=math.atan2(self.rect.centerx-x,self.rect.centery-y)+math.pi
    def changeVuln(self):
        self.currentweakspot=-self.currentweakspot
		