import pygame

class FirePart(pygame.sprite.Sprite):
    def __init__(self,x,y,hspeed,vspeed,life,creator):
        pygame.sprite.Sprite.__init__(self)
        self.game=creator
        self.rect=pygame.Rect(x-16,y-16,32,1)
        self.hspd=hspeed
        self.vspd=vspeed
        self.hp=life
    def update(self):
        self.hp-=1
        if self.hp<=0:
            self.game.removeparticle(self)
        #moving
        self.rect.move_ip(self.hspd,self.vspd)
        if self.rect.top>480:
            self.game.removeparticle(self)
    def draw(self,screen):
        #trect=pygame.Rect(0,0,12,12)
        #tsurf=self.game.spr_Fireball.subsurface(trect)
        #ttsurf=pygame.Surface([10,10],0,32)
        #ttsurf=ttsurf.convert_alpha()
        #pygame.transform.scale(tsurf,(10,10),ttsurf)
        #ttsurf=ttsurf.convert_alpha()
        ttsurf=pygame.Surface([32,32],0,32)
        pygame.draw.circle(ttsurf,(255,20,20),(16,16),16,0)
        pygame.draw.circle(ttsurf,(255,255,255),(16,16),8,0)
        
        screen.blit(ttsurf,self.rect,None,pygame.constants.BLEND_ADD)
    def collision(self,other):
        pass
        