import pygame
import sys
import os
import random
import math
import cv2
import mediapipe as mp

# Asegúrate de que el script esté ejecutándose desde el directorio raíz del proyecto
project_root = os.path.dirname(os.path.abspath(__file__))  # Obtiene la ruta absoluta del script
project_root = os.path.join(project_root, 'code')  # Asegúrate de que apunta al directorio 'code'

# Añadimos 'code' al PYTHONPATH para que Python pueda encontrar la carpeta 'juego_naves/config_naves'
sys.path.append(project_root)

# Verificamos si 'code' está en el PYTHONPATH
print("PYTHONPATH:", sys.path)

# Intentamos importar el módulo
try:
    from juego_naves.config_naves.cofig import *  # O usa 'config' si el archivo se llama 'config.py'
    print("Módulo importado correctamente")
except ModuleNotFoundError as e:
    print("Error al importar el módulo:", e)

# Aquí empieza el resto del código para el juego

class Nave_Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])
        self.clock = pygame.time.Clock()
        self.corrinedo = False
        self.iniciado = False

        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        pygame.init()
        pygame.display.set_caption("MISILES")

        self.font = pygame.font.Font('IntensaFuente', 32)
        self.smaller_font = pygame.font.Font('IntensaFuente', 22)
        self.fondo = Fondo()

        self.inicializado()

    def inicializado(self):
        self.start_time = pygame.time.get_ticks()
        self.last_frame_time = self.start_time
        self.jugador = Player()
        self.movement = 0
        self.enemy_timer = 1000
        pygame.time.set_timer(ADD_ENEMY, self.enemy_timer)

        self.enemies = pygame.sprite.Group()
        self.lost = False
        self.score = 0
        self.webcam = webcam().inicio()

        self.max_face_surf_height = 0
        self.face_left_x = 0
        self.face_right_x = 0
        self.face_top_y = 0
        self.face_bottom_y = 0

    def update(self, delta_time):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.corrinedo = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.corrinedo = False

        if self.lost or not self.iniciado:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.inicializado()
                    self.iniciado = True
        else:
            game_speed = 1 + ((pygame.time.get_ticks() - self.start_time) / 1000) * 0.1
            self.score = self.score + (delta_time * game_speed)

            for event in events:
                if event.type == ADD_ENEMY:
                    num = random.randint(1, 5)
                    for e in range(num):
                        enemy = Enemy()
                        self.enemies.add(enemy)

                    self.enemy_timer = 1000 - ((game_speed - 1) * 100)
                    if self.enemy_timer < 50:
                        self.enemy_timer = 50
                    pygame.time.set_timer(ADD_ENEMY, self.enemy_timer)

            self.jugador.update(self.movement, delta_time)
            self.enemies.update(delta_time)
            self.process_collision()
            self.fondo.update(delta_time)

    def process_collision(self):
        collide = pygame.sprite.spritecollide(self.jugador, self.enemies, False, pygame.sprite.collide_mask)
        if collide:
            self.lost = True

    def render(self):
        self.screen.fill((0, 0, 0))
        self.fondo.render(self.screen)

        if self.webcam.lastFrame is not None:
            self.render_camera()

        self.screen.blit(self.jugador.surf, self.jugador.rect)

        for e in self.enemies:
            self.screen.blit(e.surf, e.rect)

        display_score = round(self.score / 1000)
        text_score = self.font.render('PUNTUACION: ' + str(display_score), True, (255, 255, 255))
        scoreTextRect = text_score.get_rect()
        scoreTextRect.bottom = ANCHO_VENTANA - 5
        scoreTextRect.left = 5
        self.screen.blit(text_score, scoreTextRect)

        if self.lost:
            mensaje_perdida = self.font.render('PERDISTE', True, (255, 255, 255), (0, 0, 0))
            mensaje_perdida_rect = mensaje_perdida.get_rect()
            mensaje_perdida_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2)
            self.screen.blit(mensaje_perdida, mensaje_perdida_rect)

            texto_reinicio = self.smaller_font.render('Presiona Enter para reintentar', True, (200, 200, 200), (0, 0, 0))
            texto_reinicio_rect = texto_reinicio.get_rect()
            texto_reinicio_rect.center = (ANCHO_VENTANA // 2, (ALTO_VENTANA // 2) + 40)
            self.screen.blit(texto_reinicio, texto_reinicio_rect)

        if not self.iniciado:
            mensaje_perdida = self.font.render('Presiona Enter para comenzar', True, (255, 255, 255), (0, 0, 0))
            mensaje_perdida_rect = mensaje_perdida.get_rect()
            mensaje_perdida_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2)
            self.screen.blit(mensaje_perdida, mensaje_perdida_rect)

        pygame.display.flip()

    def loop(self):
        with self.mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                min_detection_confidence=0.5,
                refine_landmarks=True
        ) as self.face_mesh:
            while self.corrinedo:
                if not self.lost:
                    if not self.webcam.ready():
                        continue
                    self.process_camera()

                time = pygame.time.get_ticks()
                delta_time = time - self.last_frame_time
                self.last_frame_time = time
                self.update(delta_time)
                self.render()
                self.clock.tick(60)
            pygame.quit()

    def process_camera(self):
        image = self.webcam.read()
        if image is not None:
            image.flags.writeable = False
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = self.face_mesh.process(image)
            self.webcam_image = image

            if results.multi_face_landmarks is not None:
                for face_landmarks in results.multi_face_landmarks:
                    top = (face_landmarks.landmark[10].x, face_landmarks.landmark[10].y)
                    bottom = (face_landmarks.landmark[152].x, face_landmarks.landmark[152].y)

                    self.face_left_x = face_landmarks.landmark[234].x
                    self.face_right_x = face_landmarks.landmark[454].x
                    self.face_top_y = face_landmarks.landmark[10].y
                    self.face_bottom_y = face_landmarks.landmark[152].y

                    self.face_left_x -= 0.1
                    self.face_right_x += 0.1
                    self.face_top_y -= 0.1
                    self.face_bottom_y += 0.1

                    cv2.line(
                        self.webcam_image,
                        (int(top[0] * self.webcam.width()), int(top[1] * self.webcam.height())),
                        (int(bottom[0] * self.webcam.width()), int(bottom[1] * self.webcam.height())),
                        (0, 255, 0), 3
                    )

                    cv2.circle(self.webcam_image, (int(top[0] * self.webcam.width()), int(top[1] * self.webcam.height())), 8, (0, 0, 255), -1)
                    cv2.circle(self.webcam_image, (int(bottom[0] * self.webcam.width()), int(bottom[1] * self.webcam.height())), 8, (0, 0, 255), -1)

                    self.detect_head_movement(top, bottom)

            k = cv2.waitKey(1) & 0xFF

    def detect_head_movement(self, top, bottom):
        radians = math.atan2(bottom[1] - top[1], bottom[0] - top[0])
        degrees = math.degrees(radians)

        min_degrees = 70
        max_degrees = 110
        degree_range = max_degrees - min_degrees

        if degrees < min_degrees: degrees = min_degrees
        if degrees > max_degrees: degrees = max_degrees

        self.movement = ((degrees - min_degrees) / degree_range) * 2 - 1

    def render_camera(self):
        if self.face_left_x < 0: self.face_left_x = 0
        if self.face_right_x > 1: self.face_right_x = 1
        if self.face_top_y < 0: self.face_top_y = 0
        if self.face_bottom_y > 1: self.face_bottom_y = 1

        face_surf = pygame.image.frombuffer(self.webcam_image, (int(self.webcam.width()), int(self.webcam.height())), "BGR")

        face_rect = pygame.Rect(
            int(self.face_left_x * self.webcam.width()),
            int(self.face_top_y * self.webcam.height()),
            int(self.face_right_x * self.webcam.width()) - int(self.face_left_x * self.webcam.width()),
            int(self.face_bottom_y * self.webcam.height()) - int(self.face_top_y * self.webcam.height())
        )

        only_face_surf = pygame.Surface((int(self.face_right_x * self.webcam.width()) - int(self.face_left_x * self.webcam.width()),
                                         int(self.face_bottom_y * self.webcam.height()) - int(self.face_top_y * self.webcam.height())))
        only_face_surf.blit(face_surf, (0, 0), face_rect)

        height = only_face_surf.get_rect().height
        width = only_face_surf.get_rect().width
        if width == 0:
            width = 1

        face_ratio = height / width
        face_area_width = 130
        face_area_height = face_area_width * face_ratio
        if face_area_height > self.max_face_surf_height:
            self.max_face_surf_height = face_area_height

        only_face_surf = pygame.transform.scale(only_face_surf, (int(face_area_width), int(self.max_face_surf_height)))
        self.screen.blit(only_face_surf, only_face_surf.get_rect())
