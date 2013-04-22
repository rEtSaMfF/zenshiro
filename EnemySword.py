import pygame
from Player import *
from PlayerBomb import *
from PlayerSword import *

class EnemySword(pygame.sprite.Sprite):
    def __init__(self,xoffs,yoffs,follow,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.MeleeEnemy=follow
        self.rect=pygame.Rect(follow.rect.centerx,follow.rect.bottom,4,16)
        #self.rect=pygame.Rect(x-4,y-4,32,16,)
        self.xoff=xoffs
        self.yoff=yoffs
        self.damage=2
    def update(self):
        #moving
        self.rect=pygame.Rect(self.MeleeEnemy.rect.centerx,self.MeleeEnemy.rect.bottom,self.xoff,self.yoff)
        if self.rect.top>448:
            self.game.removeEnemy(self)
        if self.MeleeEnemy.alive!=True:
            self.game.removeEnemy(self)
    def draw(self,screen):
        screen.blit(self.game.spr_EnemySword,self.rect)
    def collision(self,other):
        if isinstance(other,PlayerBomb):
            self.game.removeEnemy(self)
        if isinstance(other,PlayerSword):
            self.game.removeEnemy(self)