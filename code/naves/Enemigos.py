from naves.config import *
ORIGIN_SIZE =(50,50)
MIN_WIDTH = 10
MAX_WIDTH = 60

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()

        self.width =random.randint(MIN_WIDTH,MAX_WIDTH)
        self.height =random.randint(self.width/ORIGIN_SIZE[0])*ORIGIN_SIZE[1]

        self.surf = pygame.image.load().convert_alpha()
        self.surf = pygame.transform.scale(self.surf,(self.width,self.height))
        self.mask = pygame.mask.from_surface(self.surf)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(0,ALTO_VENTANA),
                random.randint(-100,-20)
            )
        )

        self.speed = (random.randint(1,2)/10)*(1+(game_speed/2))
    
    def update(self,delta_time):
        self.rect.move_ip(0,self.speed*delta_time)
        self.mask= pygame.mask.from_surface(self.surf)
        if self.rect.top > ALTO_VENTANA:
            self.kill()