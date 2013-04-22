import pygame
import math

class PlayerBomb(pygame.sprite.Sprite):
    def __init__(self,xoffs,yoffs,time,follow,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.player=follow
        self.rect=pygame.Rect(200,240,xoffs,yoffs)
        self.alarm=time
        self.xoff=xoffs
        self.yoff=yoffs
        self.damage=0
        self.imageind=0.0
    def update(self):
        #moving
        if self.alarm<=10:
            self.damage=3
        self.rect.centerx=280
        self.rect.centery=240
        if self.alarm<=0:
            self.game.removePlayerBullet(self)
            self.player.spritetype=0
        self.alarm-=1
        addind=0.0
        addind+=self.game.scrollspeed
        addind+=2
        addind+=1
        self.imageind+=(addind/10)
    def draw(self,screen):
        if self.alarm>10:
            drect=pygame.Rect((math.floor(self.imageind)%2)*1280,0,1280,960)
        if self.alarm<=10:
            drect=pygame.Rect((2560,0,1280,1280))
        screen.blit(self.game.spr_PlayerBomb,self.rect,drect)