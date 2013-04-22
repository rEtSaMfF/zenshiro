import pygame
import sys
import random
import math
from Player import *
from Enemy import *
from EnemyTurret import *
from MeleeEnemy import *
from Miniboss import *
from MissileTurret import *
from HomingMissile import *
from SideBar import *
from Boss import *
from Eye import *
from Mouth import *
from Spikes import *
from FireWave import *
from FirePillar import *
from Laser import *
from LaserLead import *
from FirePart import *
from Endgame import *
from Powerup import *
from MinibossBody import *
from Explosion import *

SCREEN = WIDTH, HEIGHT = 640,480
konamicode = [K_RETURN,K_UP,K_UP,K_DOWN,K_DOWN,K_LEFT,K_RIGHT,K_LEFT,K_RIGHT,K_b,K_a,K_RETURN]

class Game(object):
    def __init__(self):
        super(Game,self).__init__()
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.cont=True
        self.screen=pygame.display.set_mode(SCREEN)
        self.screen_rect=self.screen.get_rect()
        self.clock=pygame.time.Clock()
        self.scrollspeed=2
        self.scrollind=0
        self.hscrollspeed=18
        self.hscrollind=0
        self.diff=0
        self.lastspawned=0
        self.obstaclealarm=60
        
        
        #Miniboss Timer
        self.minitimer=600
        self.minidefeated=False
        self.minispawned=False
        self.finaltimer=self.minitimer*2
        self.finalspawned=False
        
        
        self.bar=SideBar(self,self.font)
        self.player=Player(300,200,self)
        self.playerbullets=pygame.sprite.Group()
        self.enemies=pygame.sprite.Group()
        self.obstacles=pygame.sprite.Group()
        self.bossparts=pygame.sprite.Group()
        self.bossbody=pygame.sprite.Group()
        self.particles=pygame.sprite.Group()
        self.powerups=pygame.sprite.Group()
        self.explosions=pygame.sprite.Group()
        
        #Controls are defined here.
        self.keysdict={pygame.K_UP:"up",pygame.K_DOWN:"down",pygame.K_LEFT:"left",pygame.K_RIGHT:"right",pygame.K_z:"action1",pygame.K_x:"action2",pygame.K_c:"action3",pygame.K_SPACE:"action4",pygame.K_a:"action5"}
        
        #Sprites
        self.spr_playerwalk = pygame.image.load('images/Zensiro_spritesheet.png').convert_alpha()
        self.spr_spikes = pygame.image.load('images/small spike.png').convert_alpha()
        self.spr_turret1=pygame.image.load('images/turret1.png').convert_alpha()
        self.spr_turret2=pygame.image.load('images/turret2.png').convert_alpha()
        self.spr_Oni1=pygame.image.load('images/oni1_animation.png').convert_alpha()
        self.spr_Oni2=pygame.image.load('images/Oni2.png').convert_alpha()
        self.spr_Miniboss=pygame.image.load('images/tengu_head.png').convert_alpha()
        self.spr_MinibossBody=pygame.image.load('images/Tengu_body_animation.png').convert_alpha()
        self.spr_Samurai=pygame.image.load('images/Samurai_jets3.png').convert_alpha()
        self.spr_Fireball=pygame.image.load('images/Fireball_bullet.png').convert_alpha()
        self.spr_Missile=pygame.image.load('images/Missle_bullet.png').convert_alpha()
        self.spr_FireWave=pygame.image.load('images/TempFireWave.png').convert_alpha()
        self.spr_FirePillar=pygame.image.load('images/TempFirePillar.png').convert_alpha()
        self.spr_PlayerBullet=pygame.image.load('images/Player_bullet.png').convert_alpha()
        self.spr_EnemySword=pygame.image.load('images/Enemy_sword.png').convert_alpha()
        self.spr_EnemyBullet=pygame.image.load('images/Enemy_bullet.png').convert_alpha()
        self.spr_Laser=pygame.image.load('images/Laser.png').convert_alpha()
        self.spr_LeadLaser=pygame.image.load('images/Lead_laser2.png').convert_alpha()
        self.spr_PlayerSword=pygame.image.load('images/sword_attack.png').convert_alpha()
        self.spr_PlayerSwordIdle=pygame.image.load('images/Zenshiro_swordimg.png').convert_alpha()
        self.spr_EnemyTurret=pygame.image.load('images/turret1_animation.png').convert_alpha()
        self.spr_MissileTurret=pygame.image.load('images/turret2_animation.png').convert_alpha()
        self.spr_BossEyeL=pygame.image.load('images/B_left_eye.png').convert_alpha()
        self.spr_BossEyeLDeact=pygame.image.load('images/B_left_eye_deactivate.png').convert_alpha()
        self.spr_BossEyeR=pygame.image.load('images/B_right_eye.png').convert_alpha()
        self.spr_BossEyeRDeact=pygame.image.load('images/B_right_eye_deactivate.png').convert_alpha()
        self.spr_BossMouth=pygame.image.load('images/B_mouth.png').convert_alpha()
        self.spr_PlayerBomb=pygame.image.load('images/Zenshiro_bomb.png').convert_alpha()
        self.spr_Explosion=pygame.image.load('images/Explosion_animation.png').convert_alpha()
        self.spr_BossBody=pygame.image.load('images/Boss.png').convert_alpha()
        #Tiles
        self.spr_tile=[
            pygame.image.load('images/scales5.png').convert_alpha(),
            pygame.image.load('images/scales2.png').convert_alpha(),
            pygame.image.load('images/scales3.png').convert_alpha(),
            pygame.image.load('images/scales1.png').convert_alpha(),
            pygame.image.load('images/scales4.png').convert_alpha(),
            pygame.image.load('images/scales6.png').convert_alpha()]
        
        self.tilelist=[4,1,1,1,1,1,1,1,2,3,3,3,3,3,3,3,3,3,3,3,3]
        
        self.tilesurf=pygame.Surface((32*len(self.tilelist)*3,32))
        i=0
        while(i<len(self.tilelist)):
            self.tilesurf.blit(self.spr_tile[self.tilelist[i]],pygame.Rect(i*32,0,0,0))
            i+=1
        self.tilesurf.blit(self.tilesurf,(32*len(self.tilelist)*1,0))
        #self.tilesurf.blit(self.tilesurf,(32*len(self.tilelist)*2,0))
        self.hofflist=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
        self.enemyalarm=15
        
        self.addObstacle(256,32,0)
        
        # for codes
        self.codestate = 0
        self.explode = pygame.mixer.Sound("./Sounds/Explosion1.wav")
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                #self.cont=False
            if event.type==pygame.KEYDOWN:
                if event.key != konamicode[self.codestate]:
                    self.codestate = 0
                if event.key == konamicode[self.codestate]:
                    self.codestate += 1
                if self.codestate == len(konamicode):
                    self.codestate = 0
                    self.konamicode()
                if event.key==pygame.K_ESCAPE:
                    sys.exit()
                    #self.cont=False
                if event.key==pygame.K_f:
                    self.screen=pygame.display.set_mode(SCREEN, pygame.FULLSCREEN)
                if event.key==pygame.K_q:
                    sys.exit()
                # testing keys
                if event.key==pygame.K_p:
                    #spawn final boss
                    self.addBoss(self)
                if event.key==K_o:
                    #spawn miniboss
                    self.addMiniboss(320,16,self)
                if event.key==K_m:
                    Menu.show_menu()
                if event.key==K_n:
                    show_end(self)
        for tkey in self.keysdict:
            if pygame.key.get_pressed()[tkey]:
                self.player.controls[self.keysdict[tkey]]+=1
            else:
                self.player.controls[self.keysdict[tkey]]=0

    def update(self):
        self.spawning()
        self.player.update()
        self.playerbullets.update()
        self.obstacles.update()
        self.enemies.update()
        self.bossparts.update()
        self.bossbody.update()
        self.particles.update()
        self.powerups.update()
        self.explosions.update()
        
        self.scrollind+=self.scrollspeed
        if self.scrollind%32==0 and self.scrollspeed!=0:
            self.hofflist[0]+=self.hscrollspeed
            if self.hofflist[0]>=len(self.tilelist)*32:
                self.hofflist[0]-=len(self.tilelist)*32
            if self.hofflist[0]<0:
                self.hofflist[0]+=len(self.tilelist)*32
            i=len(self.hofflist)-1
            while i>0:
                self.hofflist[i]=self.hofflist[i-1]
                i-=1
    def difficulty(self,level):
        self.diff=level
    def stopScrolling(self): #- for use with miniboss/main boss
        self.scrollspeed=0
    def resumeScrolling(self): #- for use with miniboss
        self.scrollspeed=2
    def draw(self):
        self.screen.fill((0,0,0))
        self.drawtiles()
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        self.bar.draw(self.screen,self.player)
        for bossbody in self.bossbody:
            bossbody.draw(self.screen)
        for bullet in self.playerbullets:
            bullet.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bosspart in self.bossparts:
            bosspart.draw(self.screen)
        if self.player.jumping==False:
            self.player.draw(self.screen)
        if self.player.jumping==True:
            self.player.draw(self.screen)
        for part in self.particles:
            part.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        for explosion in self.explosions:
            explosion.draw(self.screen)
    def drawtiles(self):
        i=-1
        while(i<17):
            self.drawtilerow(-64+32*i+(self.scrollind%32),self.hofflist[i])
            i+=1
    def drawtilerow(self,y,hoff):
        trect=pygame.Rect(32+hoff%(len(self.tilelist)*32),0,12*32,32)
        tsurf=self.tilesurf.subsurface(trect)        
        self.screen.blit(tsurf,(32+32,y))
        
        trect=pygame.Rect(hoff%(len(self.tilelist)*32),0,32,32)
        tsurf=self.tilesurf.subsurface(trect)
        ttsurf=pygame.transform.scale(tsurf,(16,32))
        self.screen.blit(ttsurf,(48,y))
        
        trect=pygame.Rect(hoff%(len(self.tilelist)*32)+(14*32)-32,0,32,32)
        tsurf=self.tilesurf.subsurface(trect)
        ttsurf=pygame.transform.scale(tsurf,(16,32))
        self.screen.blit(ttsurf,(14*32,y))
        
    def addPlayerBullet(self,x,y,hspeed,vspeed):
        self.playerbullets.add(PlayerBullet(x,y,hspeed,vspeed,self))
    def addPlayerSword(self,xoffs,yoffs,time,follow):
        self.playerbullets.add(PlayerSword(xoffs,yoffs,time,follow,self))
    def addPlayerBomb(self,xoffs,yoffs,time,follow):
        self.playerbullets.add(PlayerBomb(xoffs,yoffs,time,follow,self))
    def removePlayerBullet(self,bullet):
        self.playerbullets.remove(bullet)
    def addEnemy(self,x,y,type):
        if type==self.lastspawned:
            type+=1
        if type==0:
            grouptype=random.randint(0,1)
            if grouptype==0:
                self.enemies.add(Enemy(x,y,4,2,self))
                self.enemies.add(Enemy(480-x,y,4,2,self))
            if grouptype==1:
                self.enemies.add(Enemy(40,y,4,1,self))
                self.enemies.add(Enemy(440,y,-4,1,self))
        elif type==1:
            self.enemies.add(MissileTurret(x-40,y,self))
            self.enemies.add(MissileTurret(480-x,y,self))
        elif type==2:
            grouptype=random.randint(0,1)
            if grouptype==0:
                self.enemies.add(MeleeEnemy(240,y,0,20,self))
                self.enemies.add(MeleeEnemy(40,y,5,10,self))
                self.enemies.add(MeleeEnemy(440,y,-5,10,self))
            if grouptype==1:
                self.enemies.add(MeleeEnemy(440,y,-10,10,self))
                self.enemies.add(MeleeEnemy(320,y,-10,7,self))
                self.enemies.add(MeleeEnemy(40,y,10,7,self))
                self.enemies.add(MeleeEnemy(160,y,10,7,self))
        elif type==3:
            self.enemies.add(EnemyTurret(x,y,self))
        self.lastspawned=type
			
    def addObstacle(self,x,y,type):
        if type==0:
            self.obstacles.add(Spikes(x,y,self))
        if type==1:
            self.obstacles.add(FireWave(x,y,self))
        if type==2:
            self.obstacles.add(FirePillar(x,y,self))
    def removeObstacle(self,obstacle):
        self.obstacles.remove(obstacle)
    def addPowerup(self,x,y):
        self.powerups.add(Powerup(x,y,self))
    def addMiniboss(self,x,y,creator):
        self.bossparts.add(Miniboss(x,y,creator))
    def addMinibossBody(self,creator,game):
        self.bossbody.add(MinibossBody(creator,self))
    def addExplosion(self,x,y):
        self.explosions.add(Explosion(x,y,self))
    def removeExplosion(self,other):
        self.explosions.remove(other)
    def addBoss(self,creator):
        self.bossbody.add(Boss(creator))
    def addEye(self,x,y,boss,creator):
        self.bossparts.add(Eye(x,y,boss,creator))
    def addMouth(self,x,y,boss,creator):
        self.bossparts.add(Mouth(x,y,boss,creator))
    def addEnemyBullet(self,x,y,hspeed,vspeed):
        self.enemies.add(EnemyBullet(x,y,hspeed,vspeed,self))
    def addHomingMissile(self,x,y,hspeed,vspeed):
        self.enemies.add(HomingMissile(x,y,hspeed,vspeed,self))
    def addEnemySword(self,xoff,yoff,follow):
        self.enemies.add(EnemySword(xoff,yoff,follow,self))
    def addFirePart(self,x,y,hspeed,vspeed,life):
        self.particles.add(FirePart(x,y,hspeed,vspeed,life,self))
    def removeparticle(self,part):
        self.particles.remove(part)
    def addFireball(self,x,y,hspeed,vspeed):
        self.enemies.add(Fireball(x,y,hspeed,vspeed,self))
    def addLaser(self,x,y):
        self.enemies.add(Laser(x,y,self))
    def addLaserLead(self,x,y):
        self.enemies.add(LaserLead(x,y,self))
    def removeEnemy(self,enemy):
        self.enemies.remove(enemy)
    def removePowerup(self,powerup):
        self.powerups.remove(powerup)
    def removeBoss(self,boss):
        self.bossparts.remove(boss)
    def removeBossBase(self,boss):
        self.bossbody.remove(boss)
    def eyeDeath(self):
        for parts in self.bossparts:
            if isinstance(parts,Mouth):
                parts.eyeDeath()
    def changeVuln(self):
        for bosspart in self.bossparts:
            if isinstance(bosspart,Mouth) or isinstance(bosspart,Eye):
                bosspart.changeVuln()
    def collisions(self):
        #Collisions with enemies and player bullets
        colls=pygame.sprite.groupcollide(self.enemies,self.playerbullets,False,False)
        for enemy in colls.keys():
            for other in colls[enemy]:
                enemy.collision(other)
        #Collisions with enemies and the player
        playergroup=pygame.sprite.Group(self.player)
        colls=pygame.sprite.groupcollide(playergroup,self.enemies,False,False)
        for player in colls.keys():
            for other in colls[player]:
                player.collision(other,0)
        colls=pygame.sprite.groupcollide(playergroup,self.powerups,False,False)
        for player in colls.keys():
            for other in colls[player]:
                player.collision(other,0)
        #Collisions with obstacles and player
        playergroup=pygame.sprite.Group(self.player)
        colls=pygame.sprite.groupcollide(playergroup,self.obstacles,False,False)
        for player in colls.keys():
            for other in colls[player]:
                player.collision(other,1)
        #Collisions with boss parts and player
        playergroup=pygame.sprite.Group(self.player)
        colls=pygame.sprite.groupcollide(playergroup,self.bossparts,False,False)
        for player in colls.keys():
            for other in colls[player]:
                player.collision(other,2)
        #Collisions with boss parts and player bullets
        colls=pygame.sprite.groupcollide(self.bossparts,self.playerbullets,False,False)
        for bosspart in colls.keys():
            for other in colls[bosspart]:
                bosspart.collision(other)
    def spawning(self):
        self.enemyalarm-=1
        self.minitimer-=1
        self.obstaclealarm-=1
        if self.minispawned==False or self.minidefeated==True:
            self.finaltimer-=1
        if self.minitimer<=0 and self.minispawned==False and self.minidefeated==False:
            self.addMiniboss(320,16,self)
            self.minispawned=True
        if self.finaltimer<=0 and self.finalspawned==False and self.minidefeated==True:
            self.addBoss(self)
            self.finalspawned=True
        elif self.minitimer>0 or self.minidefeated==True and self.finalspawned==False:   
            if self.enemyalarm<=0:
                enemytype=random.randint(0,3)
                self.addEnemy(random.randint(80,440),-16,enemytype)
                self.enemyalarm=60
            if self.obstaclealarm<=0:
                self.addObstacle(random.randint(40,400),-16,0)
                self.obstaclealarm=180
                
    def konamicode(self):
        self.player.lives += 30