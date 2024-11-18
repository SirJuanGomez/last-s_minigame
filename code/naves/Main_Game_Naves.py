from naves.AI import *
from naves.config import *
from naves.Enemigos import *
from naves.nave import *
from naves.Fondo import *

class Nave_Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([ANCHO_VENTANA,ALTO_VENTANA])
        self.clock = pygame.time.Clock()
        self.corrinedo = False
        self.iniciado = False

        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        pygame.init()
        pygame.display.set_caption("MISILES")

        self.font = pygame.font.Font('IntensaFuente',32)
        self.smaller_font = pygame.font.Font('IntensaFuente',22)
        self.fondo=Fondo()

        self.inicializado()

    def inicializado(self):
        self.start_time = pygame.time.get_ticks()
        self.last_frame_time= self.start_time
        self.jugador = Player()
        self.movement=0
        self.enemy_timer=1000
        pygame.time.set_timer(ADD_ENEMY,self.enemy_timer)

        self.enemies = pygame.sprite.Group()
        self.lost = False
        self.score = 0
        self.webcam = webcam().inicio()

        self.max_face_surf_height = 0
        self.face_left_x = 0
        self.face_right_x = 0
        self.face_top_y = 0
        self.face_bottom_y = 0

    def update(self,delta_time):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.corrinedo = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.corrinedo = False

        if self.lost or not self.iniciado:
            for event in events:
                if event.type== KEYDOWN and event.key == K_RETURN:
                    self.inicializado()
                    self.iniciado = True
        else :
            game_speed= 1+((pygame.time.get_ticks()-self.start_time)/1000)*.1
            self.score= self.score+(delta_time*game_speed)

            for event in events:
                if event.type == ADD_ENEMY:
                    num= random.randint(1,5)
                    for e in range(num):
                        enemy=Enemy()
                        self.enemies.add(enemy)
                    
                    self.enemy_timer=1000-((game_speed-1)*100)
                    if self.enemy_timer<50: self.enemy_timer=50
                    pygame.time.set_timer(ADD_ENEMY,self.enemy_timer)
            self.player.update(self.movement,delta_time)
            