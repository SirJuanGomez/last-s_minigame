from config_naves.config import *

# Definiciones de constantes
ORIG_SIZE = (50, 50)
ANCHO = 50
ALTO = (ANCHO / ORIG_SIZE[0]) * ORIG_SIZE[1]
SPEED = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        # Cargar la imagen de la nave
        self.surf = pygame.image.load("code/naves/images/test.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (ANCHO, ALTO))
        self.update_mask()

        # Guardar la imagen original para las rotaciones
        self.orig_surf = self.surf
        self.lastRotation = 0

        # Definir el rectángulo de la nave
        self.rect = self.surf.get_rect(
            center=(
                (ANCHO_VENTANA / 2) - (ANCHO / 2),
                (ALTO_VENTANA - ALTO)
            )
        )

    def update(self, movimiento, deltatime):
        # Actualizar la posición de la nave
        self.rect.move_ip(SPEED * movimiento * deltatime, 0)

        # Calcular la rotación de la nave basada en el movimiento
        rotacion = 45 * movimiento - 1
        self.surf = pygame.transform.rotate(self.orig_surf, self.lerp(self.lastRotation, rotacion, 0.5))
        self.lastRotation = rotacion
        self.update_mask()

        # Limitar la nave dentro de los límites de la ventana
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > ANCHO_VENTANA: self.rect.right = ANCHO_VENTANA
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom > ALTO_VENTANA: self.rect.bottom = ALTO_VENTANA

    def lerp(self, a: float, b: float, t: float) -> float:
        """Interpolate linealmente entre a y b con t"""
        return (1 - t) * a + t * b

    def update_mask(self):
        """Actualizar la máscara para la detección de colisiones"""
        maskSurface = self.surf
        maskSurface = pygame.transform.scale(maskSurface, (ANCHO * 0.9, ALTO * 0.9))
        self.mask = pygame.mask.from_surface(maskSurface)
