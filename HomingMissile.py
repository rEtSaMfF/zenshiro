import pygame
import math
from PlayerSword import *
from Player import *
from PlayerBomb import *
from PlayerBullet import *

class HomingMissile(pygame.sprite.Sprite):
    def __init__(self,x,y,hspeed,vspeed,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-4,y-4,4,8)
        self.newrect=self.rect
        self.hspd=hspeed
        self.vspd=vspeed
        self.damage=2
        self.reflected=0
        self.aimdir=0
        self.bulletspeed=6
        self.missile_surf=self.game.spr_Missile
        self.temp=self.missile_surf
        self.imageind=0.0
    def update(self):
        
        addind=0.0
        addind+=self.game.scrollspeed
        addind+=self.vspd
        addind+=abs(self.hspd/4)
        self.imageind+=(addind/10)
        self.drect=pygame.Rect((math.floor(self.imageind)%2)*4,0,4,8)
        #aiming
        tox=self.game.player.rect.centerx
        toy=self.game.player.rect.centery
        self.aim(tox,toy)        
        #moving
        tvspd=math.sin(self.aimdir)*self.bulletspeed
        self.rect.move_ip(tvspd,self.vspd)
        if self.rect.top>480:
            self.game.removeEnemy(self)
    def draw(self,screen):
        screen.blit(self.temp,self.newrect)
    def collision(self,other):
        if isinstance(other,PlayerSword):
            self.game.removeEnemy(self)
            self.game.explode.play(loops=0, maxtime=0)
        if isinstance(other,PlayerBomb):
            self.game.removeEnemy(self)
            self.game.explode.play(loops=0, maxtime=0)
    def aim(self,x,y):
        self.aimdir=math.atan2(self.rect.centerx-x,self.rect.centery-y)+math.pi
        self.aimdir2=self.aimdir*(180/math.pi)
        self.temp=pygame.Surface(self.rect.size,pygame.SRCALPHA)
        self.temp.blit(self.missile_surf,self.missile_surf.get_rect(),self.drect)
        self.temp=pygame.transform.rotate(self.temp,self.aimdir2)
        self.temprect=self.temp.get_rect()
        self.newrect=pygame.Rect(self.rect.centerx-self.temprect.centerx,self.rect.centery-self.temprect.centery,self.temprect.width,self.temprect.height)