import pygame

class PlayerSword(pygame.sprite.Sprite):
    def __init__(self,xoffs,yoffs,time,follow,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.player=follow
        self.rect=pygame.Rect(follow.rect.centerx-(xoffs/2),follow.rect.top-yoffs*1.5,64,48)
        self.alarm=time
        self.xoff=xoffs
        self.yoff=yoffs
        self.damage=3
        self.imageind=0
    def update(self):
        self.imageind+=1
        #moving
        self.rect=pygame.Rect(self.player.rect.centerx-self.xoff/2,self.player.rect.top-self.yoff*1.5,64,48)
        if self.alarm<=0:
            self.game.removePlayerBullet(self)
            self.player.spritetype=0
        self.alarm-=1
    def draw(self,screen):
        drect=pygame.Rect((self.imageind)*64,0,64,48)
        screen.blit(self.game.spr_PlayerSword,self.rect,drect)