from naves.config import *


ORIG_SIZE=(50,50)
ANCHO= 50
ALTO= (ANCHO/ORIG_SIZE[0])*ORIG_SIZE[1]
SPEED= 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()

        self.surf = pygame.image.load("code/naves/images/test.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf,(ANCHO,ALTO))
        self.update_mask()

        self.orig_surf=self.surf
        self.lastRotation=0

        self.rect= self.surf.get_rect(
            center=(
                (ANCHO_VENTANA/2)-(ANCHO/2),
                (ALTO_VENTANA-ALTO)
            )
        )
    
    def update(self,movimiento,deltatime):
        self.rect.move_ip(SPEED*movimiento*deltatime,0)
        rotacion=45*movimiento-1
        self.surf = pygame.transform.rotate(self.orig_surf,self.lerp(self.lastRotation,rotacion,.5))
        self.lastRotation= rotacion
        self.update_mask()

        if self.rect.lef < 0: self.rect.left=0
        if self.rect.right > ANCHO_VENTANA: self.rect.right= ANCHO_VENTANA
        if self.rect.top <= 0: self.rect.top =0
        if self.rect.bottom > ALTO_VENTANA: self.rect.bottom = ALTO_VENTANA
    
    def lerp(self,a:float,b:float,t:float) -> float:
        return (1-t)*a+t*b
    
    def update_mask(self):
        maskSurface=self.surf
        maskSurface= pygame.transform.scale(maskSurface,(ANCHO*.9,ALTO*.9))
        self.mask= pygame.mask.from_surface(maskSurface)