import pygame
from PlayerBullet import *
from Enemy import *
import math
import random

class SideBar():
    def __init__(self,creator,font):
        self.game=creator
        self.width=self.game.screen_rect.right
        self.height=self.game.screen_rect.bottom
        self.font=font
        self.stars=[]
        self.nextupdate=0
        self.progress=0
        self.time=self.game.finaltimer
        self.prog_surf=pygame.image.load("./images/progressbar.png").convert_alpha()
        self.prog_rect=self.prog_surf.get_rect()
        count=50
        while count>0:
            x = random.randint(0,self.width)
            if x<40 or x>self.width*.75:
                self.stars.append([pygame.image.load('images/Star.png'),x,random.randint(0,self.height)])
                count-=1

    def draw(self,screen,player):
        # divider
        pygame.draw.line(screen,(100,100,100),(self.width*.75,0),(self.width*.75,self.height),2)
        
        if self.game.scrollspeed!=0:
            self.nextupdate+=1
        if self.nextupdate%(math.floor(self.time/100))==0 and self.game.finaltimer>=0:
            self.progress+=1.25786
            
        self.newprog_surf=pygame.transform.scale(self.prog_surf,(self.prog_rect.right,int(math.floor(self.prog_rect.bottom*self.progress))))
            
        # text info
        name = self.font.render("ZENSHIRO", 1, (255,255,255))
        score = self.font.render("Score: %s" % player.score, 1, (0, 255, 0))
        lives = self.font.render("Lives: %s" % player.lives, 1, (0, 0, 255))
        kills = self.font.render("Kills: %s" % player.kills, 1, (255, 0, 0))
        bombs = self.font.render("Bomb: %s" % player.bombs, 1, (200, 200, 200))
        swords = self.font.render("Sword: %s%%" %player.swords, 1, (0,255,255))
        namepos = [self.width*.75, 0]
        scorepos = [self.width*.75, 40]
        livespos = [self.width*.75, 60]
        killspos = [self.width*.75, 80]
        bombspos = [self.width*.75, 100]
        swordspos = [self.width*.75, 120]
        screen.blit(name, namepos)
        screen.blit(score, scorepos)
        screen.blit(lives, livespos)
        screen.blit(kills, killspos)
        screen.blit(bombs, bombspos)
        screen.blit(swords, swordspos)
        
        # progress bar
        screen.blit(self.newprog_surf,(self.width*.76,(self.height*.92)-self.prog_rect.bottom*self.progress))
        progressbar = pygame.image.load('images/Progress Bar.png')
        screen.blit(progressbar,(self.width*.76,self.height*.5))
        maxkills=100
        maxprogress=progressbar.get_height()
        progress=progressbar.get_rect().bottom
        progress+=self.height*.5
        progress-=maxprogress*player.kills/maxkills
        #progressline=pygame.Rect(self.width*.75,progress,self.width*.25,1)
        #pygame.draw.rect(screen,(255,0,0),progressline,1)
        
        # progress=maxprogress*player.kills/maxkills
        # fullbar=pygame.Rect(self.width*.95,self.height*.3,20,maxprogress)
        # progressbar=pygame.Rect(self.width*.95,self.height*.3,20,progress)
        # progressbar.bottom=444
        # pygame.draw.rect(screen,(200,200,200),fullbar,1)
        # pygame.draw.rect(screen,(200,200,200),progressbar,0)
        
        # STARS!
        if random.randint(1,10)==1:
            x = random.randint(0,self.width)
            if x<40 or x>self.width*.75:
                self.stars.append([pygame.image.load('images/Star.png'),x,0])
        for star in self.stars:
            screen.blit(star[0],(star[1],star[2]))
            star[2]+=.2
            if star[2]>self.height:
                self.stars.remove(star)