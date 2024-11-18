from naves.config import *

class Fondo(pygame.sprite.Sprite):
    def __init__(self):
        super(Fondo, self).__init__()
        self.surf=pygame.image.load("")
        ancho_fondo= ANCHO_VENTANA*2
        alto_fondo= (ancho_fondo/self.surf.get_width())*self.surf.get_height()
        self.surf= pygame.transform.scale(self.surf,(ancho_fondo,alto_fondo))
        self.rect=self.surf.get_rect(
            bottomleft=(0,ALTO_VENTANA)
        )

        self.surf2= self.surf
        self.rect2= self.surf2.get_rect(bottomleft=self.rect.topleft)
        self.ypos=0
        self.ypos2= alto_fondo-ALTO_VENTANA
    
    def update(self,delta_time):
        self.ypos += .05*delta_time
        self.ypos2 +=.05*delta_time
        self.rect.y= int(self.ypos)
        self.rect2.y= int(self.ypos2)

        if self.rect.y > ALTO_VENTANA:
            self.ypos=self.rect2.y-self.surf2.get_height()
            self.rect.y=self.ypos
        if self.rect2.y > ALTO_VENTANA:
            self.ypos2=self.rect.y-self.surf.get_height()
            self.rect2.y=self.ypos2
    
    def render(self,dest):
        dest.blit(self.surf,self.rect)
        dest.blit(self.surf2,self.rect2)