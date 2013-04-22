import pygame
import random
import math
from EnemyBullet import *
from PlayerBullet import *
from PlayerSword import *
from Fireball import *
class Miniboss(pygame.sprite.Sprite):
    def __init__(self,x,y,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-320,y-16,32,32)
        self.hspd=4
        self.vspd=1
        self.emergetime=60
        self.hpmax=150
        self.hp=self.hpmax
        self.bulletspeed=8
        self.shootalarm=30
        self.shootalarmmax=30
        self.fireballalarm=35
        self.fireballalarmmax=35
        self.volleytimer=0
        self.aimdir=0
        self.game.stopScrolling()
        self.game.addMinibossBody(self,self.game)
    def update(self):
        #moving
        new_rect=self.rect.move(self.hspd,self.vspd)
        if new_rect.left<120:
            if(self.hspd<0):
                self.hspd=-self.hspd
        elif new_rect.right>360:
            if(self.hspd>0):
                self.hspd=-self.hspd
        self.emergetime-=1
        if self.emergetime<=0:
            self.vspd=0
        self.rect.move_ip(self.hspd,self.vspd)
        if self.rect.top>480:
            self.game.removeEnemy(self)
        if self.hp<=0:
            self.game.removeBoss(self)
            self.game.minidefeated=True
            self.game.finaltimer+=600
            self.game.resumeScrolling()
            self.game.player.kills+=1
            self.game.player.score+=self.hpmax*10
            self.game.bar.progress+=10
            self.game.explode.play(loops=0, maxtime=0)
            self.game.addExplosion(self.rect.left,self.rect.top)
        #shooting
        self.shootalarm-=1
        if self.shootalarm<=0:
            shottype=random.randint(0,3)
            self.shootalarm=self.shootalarmmax
            self.shoot(shottype)
        #fireballin'
        self.fireballalarm-=1
        if self.fireballalarm<=0:
            self.fireballalarm=self.fireballalarmmax
            self.fire()
            

    def draw(self,screen):
        screen.blit(self.game.spr_Miniboss,self.rect)
        self.health_surf = pygame.image.load("./images/healthbar.png").convert_alpha()
        self.health_rect=self.health_surf.get_rect()
        if self.hp>=0:
            self.newhealth_surf=pygame.transform.scale(self.health_surf,(self.health_rect.right*(self.hp*2),self.health_rect.bottom))
        self.health_rect.top = 0
        self.health_rect.right=200
        self.game.screen.blit(self.newhealth_surf,self.health_rect)
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
            
    def fire(self):
        if self.volleytimer!=3:
            self.game.addFireball(self.rect.centerx, self.rect.bottom,0,8)
            self.volleytimer+=1
        elif self.volleytimer==3:
            self.game.addFireball(self.rect.centerx-10, self.rect.bottom,-2,8)
            self.game.addFireball(self.rect.centerx-20, self.rect.bottom,-4,8)
            self.game.addFireball(self.rect.centerx+10, self.rect.bottom,2,8)
            self.game.addFireball(self.rect.centerx+20, self.rect.bottom,4,8)
            self.game.addFireball(self.rect.centerx, self.rect.bottom,0,8)
            self.volleytimer=0
    def aim(self,x,y):
        self.aimdir=math.atan2(self.rect.centerx-x,self.rect.centery-y)+math.pi
		