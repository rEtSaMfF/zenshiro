import pygame
import math

class Spikes(pygame.sprite.Sprite):
    def __init__(self,x,y,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-16,y-16,32,32)
        self.hspd=0
        self.vspd=0
        self.hpmax=26
        self.hp=self.hpmax
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
        
    def draw(self,screen):
        screen.blit(self.game.spr_spikes,self.rect)
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
    