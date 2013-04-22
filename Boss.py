import pygame
import random
import math
from EnemyBullet import *
from PlayerBullet import *
from PlayerSword import *
from Endgame import *
import Endgame

class Boss(pygame.sprite.Sprite):
    def __init__(self,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(0,-164,480,164)
        self.hspd=0
        self.vspd=1
        self.emergetime=164
        self.hpmax=800
        self.hp=self.hpmax
        self.weaktimermax=300
        self.weaktimer=self.weaktimermax
        self.currentweak=0
        self.game.stopScrolling()
        self.beatenCounter=0
        
    def update(self):
        self.weaktimer-=1
        if(self.weaktimer<=0):
            self.changeVuln()
            self.weaktimer=self.weaktimermax
        #moving
        if self.emergetime==164:  
            self.game.addEye(128,-128,self,self.game)
            self.game.addEye(287,-128,self,self.game)
            self.game.addMouth(212,-64,self,self.game)
        new_rect=self.rect.move(self.hspd,self.vspd)
        self.emergetime-=1
        if self.emergetime<=0:
            self.vspd=0
        self.rect.move_ip(self.hspd,self.vspd)
        if self.hp<=0:
            self.game.minidefeated=True
            self.game.resumeScrolling()
            self.game.player.kills+=1
            self.game.player.score+=self.hpmax*10
            self.beatenCounter+=1
        if self.beatenCounter>0:
            if self.beatenCounter%8==1:
                self.game.addExplosion(random.randint(40,440),random.randint(0,180))
        if self.beatenCounter>=60:
            self.game.removeBossBase(self)
            show_end(self.game)
            
    def draw(self,screen):
        screen.blit(self.game.spr_BossBody,self.rect)
        self.health_surf = pygame.image.load("./images/healthbar.png").convert_alpha()
        self.health_rect=self.health_surf.get_rect()
        if self.hp>=0:
            self.newhealth_surf=pygame.transform.scale(self.health_surf,(int(math.floor(self.health_rect.right*(self.hp/2))),self.health_rect.bottom))
        self.health_rect.top = 0
        self.health_rect.right=50
        self.game.screen.blit(self.newhealth_surf,self.health_rect)
        
    def collision(self,other):
        self.hp=self.hp
        
    def reduceHealth(self,damage):
        self.hp-=damage
        
    def changeVuln(self):
        self.game.changeVuln()