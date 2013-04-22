import pygame
import sys
from PlayerBullet import *
from Enemy import *
from Menu import *
from LaserLead import *
from MeleeEnemy import *
from Powerup import *
from Endgame import *
import Endgame
import Menu
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.width=self.game.screen_rect.right
        self.height=self.game.screen_rect.bottom
        self.rect=pygame.Rect(x-16,y-16,32,32)
        self.invuln=60
        self.alive=True
        #Movement stuff
        self.movehspd=4
        self.movevspd=4
        self.addhspd=8
        self.addvspd=8
        self.hspd=0
        self.vspd=0
        self.spritetype=0
        #Jumping
        self.jumping=False
        self.jumpmetermax=90
        self.jumpmeter=self.jumpmetermax
        #Shooting stuff
        self.shoottimer=0
        self.shoottimermgun=6
        self.shoottimersgun=18
        self.shoottimersword=12
        self.swordchargermax=18
        self.shootmode=1
        self.swordcharger=self.swordchargermax
        self.swordreset=0
        self.swordmax=4
        #Bombing Stuff
        self.bombtimer=0
        self.bombtimermax=120
        #Controls list(action1=shoot,action2=sword,action3=jump,action4=bomb)
        #value>0 means pressed, value==1 means just pressed
        self.controls={"up":0,"down":0,"left":0,"right":0,"action1":0,"action2":0,"action3":0,"action4":0,"action5":0}
        #Sprite Stuff
        self.imageind=0.0
        #SideBar Stuff
        self.newlife=1000
        self.lifethreshold=1500
        self.score=0
        self.lives=3
        self.kills=0
        self.bombs=3
        self.swords=100
        self.new=0
        self.swoosh = pygame.mixer.Sound("./Sounds/Sword1.wav")
        self.pew = pygame.mixer.Sound("./Sounds/Shot1.wav")
        self.fwoosh=pygame.mixer.Sound("./Sounds/Jetpack1.wav")
        self.pwing=pygame.mixer.Sound("./Sounds/Lifeup1.wav")
    def update(self):
        if self.new==0:
            self.new=1
            pygame.mixer.music.load('sounds/test.ogg')
            pygame.mixer.music.play(-1)
        if self.lives<=0:
            gameOver(self)
        if self.score>=self.newlife:
            self.lives+=1
            self.newlife+=self.lifethreshold
            self.pwing.play(loops=0, maxtime=0)
        if self.invuln>0:
            self.invuln-=1
        else:
            self.alive=True
            
        if self.jumping==True:
            self.fwoosh.play(loops=0, maxtime=0)
        if self.jumping==False:
            self.fwoosh.stop()
        #Movement
        ##hspd and vspd are being reset to 0, but later they can be used for momentum
        ##also, we might want to slow down diagonal movement at some point
        self.hspd=0
        self.vspd=0
        if self.controls["up"]>0:
            if self.controls["up"]>3:
                self.vspd-=self.addvspd
            else:
                self.vspd-=self.movevspd
        if self.controls["down"]>0:
            if self.controls["down"]>3:
                self.vspd+=self.addvspd
            else:
                self.vspd+=self.movevspd
        if self.controls["left"]>0:
            if self.controls["left"]>3:
                self.hspd-=self.addhspd
            else:
                self.hspd-=self.movehspd
        if self.controls["right"]>0:
            if self.controls["right"]>3:
                self.hspd+=self.addhspd
            else:
                self.hspd+=self.movehspd
        new_rect=self.rect.move(self.hspd,self.vspd)
        
        #increase imageind for animation
        addind=0.0
        addind+=self.game.scrollspeed
        addind+=self.vspd
        addind+=abs(self.hspd/4)
        self.imageind+=(addind/10)
    
        #so we can't move off dragon
        if new_rect.left<=48-8:
            new_rect.left=48-8
        if new_rect.right>=self.width*.75-16+8:
            new_rect.right=self.width*.75-16+8
        if new_rect.top<=0:
            new_rect.top=0
        if new_rect.bottom>=self.height:
            new_rect.bottom=self.height
        self.rect=new_rect
        
        #Jumping
        if self.jumping:
            if self.jumpmeter<=0:
                self.jumping=False
                self.spritetype=0
            if self.controls["action3"]>0:
                self.jumpmeter-=3
                self.game.addFirePart(self.rect.centerx-6,self.rect.top-16,random.randint(-6,2)/10,10,6)
                self.game.addFirePart(self.rect.centerx,self.rect.top-28,random.randint(-4,4)/10,12,6)
                self.game.addFirePart(self.rect.centerx+6,self.rect.top-16,random.randint(-2,6)/10,10,6)
            else:
                self.jumping=False
                self.spritetype=0
        else:
            self.jumpmeter=min((self.jumpmeter+1,self.jumpmetermax))
            if self.controls["action3"]==1:
                if self.jumpmeter>=self.jumpmetermax:
                    self.jumping=True
                    self.spritetype=2
                
        
        self.shoottimer-=1
        #Sword Recharging
        if self.swords<100:
            self.swordcharger-=1
            if self.swordcharger<=0:
                self.swords+=1
                self.swordcharger=self.swordchargermax
        #Swording
        self.swordreset-=1
        if self.controls["action2"]==1:
            if self.swords>=5:
                if self.swordreset<=0:
                    self.sword()
                    self.swords-=5
                    self.swordreset=self.swordmax
                self.spritetype=1
        #Shooting
        if self.controls["action5"]==1:
            self.shootmode*=-1
        if self.controls["action1"]>0:
            if self.shoottimer<=0:
                if self.shootmode>0:
                    self.shoottimer=self.shoottimermgun
                elif self.shootmode<0:
                    self.shoottimer=self.shoottimersgun
                self.shoot()
                
        #Bombing
        self.bombtimer-=1
        if self.controls["action4"]>0:
            if self.bombs>=1 and self.bombtimer<=0:
                self.bombtimer=self.bombtimermax
                self.bomb()
                self.spritetype=0
    def draw(self,screen):
        #blink for invuln
        if self.invuln>0:
            if self.invuln%4==0:
                return 0;
        ##draw sword ready indicator (placeholder)
        if self.swords>=5 and self.swordreset<=0:
            temp=pygame.Rect(self.rect.centerx+12,self.rect.top-32,4,32)
            screen.blit(self.game.spr_PlayerSwordIdle,temp)
        ##draw player
        if self.spritetype<=1:
            drect=pygame.Rect((math.floor(self.imageind)%4)*32,self.spritetype*64,32,64)
        if self.spritetype==2:
            drect=pygame.Rect(0,self.spritetype*64,32,64)
            self.spritetype=3
        if self.spritetype==3:
            drect=pygame.Rect((math.floor(self.imageind)%2)*32,self.spritetype*64,32,64)
        if self.jumping:
            tsurf=self.game.spr_playerwalk.subsurface(drect)
            ttsurf=pygame.transform.scale(tsurf,(40,80))
            screen.blit(ttsurf,self.rect.move(0-6,-32-10))
        else:
            screen.blit(self.game.spr_playerwalk,self.rect.move(0,-32),drect)
        ##draw jumping fuel bar (placeholder)
        if self.jumpmeter<self.jumpmetermax:
            col=(40,20,230)
        else:
            col=(255,255,255)
        pygame.draw.rect(screen,col,pygame.Rect(self.rect.centerx-12,self.rect.bottom+2,24*(float(self.jumpmeter)/float(self.jumpmetermax)),6),0)
        pygame.draw.rect(screen,(10,10,10),pygame.Rect(self.rect.centerx-12,self.rect.bottom+2,24,6),1)
        
    def shoot(self):
        self.pew.play(loops=0,maxtime=0)
        if self.shootmode>0:
            self.game.addPlayerBullet(self.rect.centerx,self.rect.top,0,-22)
        if self.shootmode<0:
            self.game.addPlayerBullet(self.rect.centerx,self.rect.top,0,-22)
            self.game.addPlayerBullet(self.rect.centerx-4,self.rect.top,-4,-22)
            self.game.addPlayerBullet(self.rect.centerx+4,self.rect.top,4,-22)
            self.game.addPlayerBullet(self.rect.centerx+8,self.rect.top,8,-22)
            self.game.addPlayerBullet(self.rect.centerx-8,self.rect.top,-8,-22)
    def sword(self):
        self.swoosh.play(loops=0,maxtime=0)
        self.game.addPlayerSword(64,32,4,self)
    def bomb(self):
        self.game.addPlayerBomb(1280,480,30,self)
        self.bombs-=1
        self.invuln=30
    def collision(self,other,type):
        if type==0: #enemies
            if self.jumping==False:
                if isinstance(other,LaserLead)==False:
                    self.game.removeEnemy(other)
                    if isinstance(other,MeleeEnemy)==True:
                        other.alive=False
                    if isinstance(other,Powerup)==False:
                        if self.invuln<=0:
                            self.alive=False
                            self.invuln=60
                            self.lives-=1
                            if self.bombs<3:
                                self.bombs+=1
                            self.game.addExplosion(self.rect.left,self.rect.top)
                            if self.swords<=75:
                                self.swords+=25
                            else:
                                self.swords=100
                            self.game.explode.play(loops=0, maxtime=0)
                    elif isinstance(other,Powerup):
                        self.lives+=1
                        self.bombs+=1
                        self.game.removePowerup(other)
        elif type==1: #obstacles
            if self.jumping==False:
                if self.invuln<=0:
                    self.alive=False
                    self.invuln=60
                    self.lives-=1
                    self.game.addExplosion(self.rect.left,self.rect.top)
                    if self.bombs<3:
                        self.bombs+=1
                    if self.swords<=75:
                        self.swords+=25
                    else:
                        self.swords=100
        elif type==2: #bosses
            if self.jumping==False:
                if self.invuln<=0:
                    self.alive=False
                    self.invuln=60
                    self.lives-=1
                    self.game.addExplosion(self.rect.left,self.rect.top)
                    if self.bombs<3:
                        self.bombs+=1
                    if self.swords<=75:
                        self.swords+=25
                    else:
                        self.swords=100