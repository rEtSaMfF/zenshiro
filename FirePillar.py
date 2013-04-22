import pygame
import math

class FirePillar(pygame.sprite.Sprite):
    def __init__(self,x,y,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-16,y-16,57,480)
        self.hspd=0
        self.vspd=0
        self.lifetime=90
    def update(self):
        self.lifetime-=1
        if self.lifetime<=0:
            self.game.removeObstacle(self)
        #moving
        self.vspd=self.game.scrollspeed
        self.rect.move_ip(self.hspd,self.vspd)
        if self.rect.top>480:
            self.game.removeObstacle(self)
	#needs new sprite	
    def draw(self,screen):
        screen.blit(self.game.spr_FirePillar,self.rect)
    def collision(self,other):
        if isinstance(other,PlayerBomb):
            self.game.removeObstacle(self)