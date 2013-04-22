import pygame
from Player import *

class Powerup(pygame.sprite.Sprite):
    def __init__(self,x,y,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-4,y-4,5,48)
        self.hspd=0
        self.vspd=self.game.scrollspeed
    def update(self):
        #moving
        self.rect.move_ip(self.hspd,self.vspd)
        if self.rect.top>480:
            self.game.removeEnemy(self)
    def draw(self,screen):
        screen.blit(self.game.spr_PlayerSwordIdle,self.rect)
    def collision(self,other):
        if isinstance(other,Player):
            self.game.removePowerup(self)