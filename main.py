import pygame
import random
import os

# Inicializamos Pygame
pygame.init()

# Definimos constantes de la pantalla
ANCHO_PANTALLA = 1000
ALTO_PANTALLA = 600
GRAVEDAD = 0.3
FUERZA_SALTO = -6
VELOCIDAD_MAX = 12
ESPACIO_OBSTACULOS_FACIL = 250
ESPACIO_OBSTACULOS_DIFICIL = 200

# Inicializamos la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('OVNI Adventures')

# Cargamos sonidos
sonido_salto = pygame.mixer.Sound('jump.mp3')
sonido_choque = pygame.mixer.Sound('hit.mp3')

# Cargamos imágenes (debes proporcionar estas imágenes)
imagen_ovni1 = pygame.image.load('ovni.png').convert_alpha()  # OVNI con luces
imagen_ovni2 = pygame.image.load('ovni2.png').convert_alpha()  # OVNI sin luces
# Redimensionamos las imágenes de los aviones a un tamaño más pequeño
imagen_avion = pygame.transform.scale(pygame.image.load('airplane3.png').convert_alpha(), (50, 30))  # Imagen del avión pequeño

# Redimensionamos y cargamos tres tamaños diferentes de edificios
imagen_edificio_pequeño = pygame.transform.scale(pygame.image.load('building_small.png').convert_alpha(), (70, 200))
imagen_edificio_mediano = pygame.transform.scale(pygame.image.load('building_medium.png').convert_alpha(), (70, 300))
imagen_edificio_grande = pygame.transform.scale(pygame.image.load('building_large.png').convert_alpha(), (70, 400))

# Redimensionamos las estrellas al tamaño del OVNI
imagen_estrella = pygame.transform.scale(pygame.image.load('star.png').convert_alpha(), (50, 35))  # Tamaño del OVNI

# Cargamos las imágenes de los fondos
imagen_fondo_dia = pygame.image.load('background_city_day.png').convert()
imagen_fondo_noche = pygame.image.load('background_city_night.jpg').convert()

# Definimos la clase del OVNI (en lugar del pájaro)
class OVNI:
    def __init__(self, x, y):
        self.imagenes = [pygame.transform.scale(imagen_ovni1, (50, 35)), pygame.transform.scale(imagen_ovni2, (50, 35))]
        self.index_imagen = 0
        self.imagen = self.imagenes[self.index_imagen]
        self.rect = self.imagen.get_rect(center=(x, y))
        self.velocidad = 0
        self.contador_animacion = 0

    def saltar(self):
        self.velocidad = FUERZA_SALTO
        sonido_salto.play()

    def actualizar(self):
        self.velocidad = min(self.velocidad + GRAVEDAD, VELOCIDAD_MAX)
        self.rect.y += self.velocidad

        # Animación del OVNI
        self.contador_animacion += 1
        if self.contador_animacion % 5 == 0:
            self.index_imagen = (self.index_imagen + 1) % 2
            self.imagen = self.imagenes[self.index_imagen]

    def mostrar(self):
        pantalla.blit(self.imagen, self.rect)

# Definimos la clase de los obstáculos (edificios y aviones/naves)
class Obstaculo:
    def __init__(self, x, espacio_entre_obstaculos):
        self.x = x
        self.altura = random.randint(150, 400)
        # Seleccionamos aleatoriamente entre tres tamaños de edificios
        self.edificio_tipo = random.choice([imagen_edificio_pequeño, imagen_edificio_mediano, imagen_edificio_grande])

        # Edificio (parte inferior)
        self.rect_edificio = self.edificio_tipo.get_rect(midbottom=(self.x, ALTO_PANTALLA))

        # Avión/nave (parte superior)
        self.rect_avion = imagen_avion.get_rect(midbottom=(self.x, self.altura - espacio_entre_obstaculos))

    def mover(self, velocidad):
        self.rect_edificio.x -= velocidad
        self.rect_avion.x -= velocidad

    def mostrar(self):
        pantalla.blit(self.edificio_tipo, self.rect_edificio)  # Mostramos el edificio aleatorio
        pantalla.blit(imagen_avion, self.rect_avion)  # Mostramos el avión

    def fuera_pantalla(self):
        return self.rect_edificio.right < 0

# Definimos la clase de las estrellas (poder especial)
class Estrella:
    def __init__(self, x, y):
        self.rect = imagen_estrella.get_rect(center=(x, y))

    def mover(self, velocidad):
        self.rect.x -= velocidad

    def mostrar(self):
        pantalla.blit(imagen_estrella, self.rect)

# Función para detectar colisiones
def detectar_colision(ovni, obstaculos):
    for obstaculo in obstaculos:
        if ovni.rect.colliderect(obstaculo.rect_edificio) or ovni.rect.colliderect(obstaculo.rect_avion):
            sonido_choque.play()
            return True
    if ovni.rect.top <= 0 or ovni.rect.bottom >= ALTO_PANTALLA:
        sonido_choque.play()
        return True
    return False

# Función para cargar puntuaciones
def cargar_puntuaciones():
    try:
        with open("highscores.txt", "r") as archivo:
            return [int(linea.strip()) for linea in archivo.readlines()]
    except:
        return [0] * 5

# Función para guardar puntuaciones
def guardar_puntuacion(puntaje):
    puntuaciones = cargar_puntuaciones()
    puntuaciones.append(puntaje)
    puntuaciones = sorted(puntuaciones, reverse=True)[:5]
    with open("highscores.txt", "w") as archivo:
        for punt in puntuaciones:
            archivo.write(f"{punt}\n")

# Función para manejar el parallax scrolling del fondo
def mostrar_fondo(fondo_x, fondo):
    pantalla.blit(fondo, (fondo_x, 0))
    pantalla.blit(fondo, (fondo_x + ANCHO_PANTALLA, 0))

# Función para reiniciar el juego
def reiniciar_juego(dificultad='facil', num_jugadores=1):
    ovni1 = OVNI(100, ALTO_PANTALLA // 2)
    ovni2 = OVNI(100, ALTO_PANTALLA // 2 + 100) if num_jugadores == 2 else None
    obstaculos = []
    estrellas = []
    marcador = 0
    velocidad_juego = 3 if dificultad == 'facil' else 6
    espacio_entre_obstaculos = ESPACIO_OBSTACULOS_FACIL if dificultad == 'facil' else ESPACIO_OBSTACULOS_DIFICIL
    fondo = imagen_fondo_dia
    modo_zen = False
    return ovni1, ovni2, obstaculos, estrellas, marcador, velocidad_juego, espacio_entre_obstaculos, fondo, modo_zen

def mostrar_menu():
    fuente = pygame.font.SysFont('Arial', 40)
    opciones = ["1 Jugador", "2 Jugadores", "Salir"]
    seleccion = 0

    ejecutando = True
    while ejecutando:
        pantalla.fill((0, 0, 0))

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (100, 100, 100)
            texto_opcion = fuente.render(opcion, True, color)
            pantalla.blit(texto_opcion, (ANCHO_PANTALLA // 2 - 100, 200 + i * 60))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:  # Enter para seleccionar opción
                    if seleccion == 0:
                        return 1  # Opción de 1 jugador
                    elif seleccion == 1:
                        return 2  # Opción de 2 jugadores
                    elif seleccion == 2:
                        pygame.quit()
                        quit()  # Salir del juego

# Función principal del juego
def jugar(num_jugadores=1):
    reloj = pygame.time.Clock()
    ovni1, ovni2, obstaculos, estrellas, marcador, velocidad_juego, espacio_entre_obstaculos, fondo, modo_zen = reiniciar_juego(num_jugadores=num_jugadores)
    fuente = pygame.font.SysFont('Arial', 30)
    fondo_x = 0

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    ovni1.saltar()
                if num_jugadores == 2 and evento.key == pygame.K_UP:  # Multijugador
                    ovni2.saltar()
                if evento.key == pygame.K_z:  # Modo Zen toggle
                    modo_zen = not modo_zen

        # Mover el fondo
        fondo_x -= 1
        if fondo_x <= -ANCHO_PANTALLA:
            fondo_x = 0
        mostrar_fondo(fondo_x, fondo)

        # Actualizar y mostrar OVNI
        ovni1.actualizar()
        ovni1.mostrar()

        # Multijugador
        if num_jugadores == 2:
            ovni2.actualizar()
            ovni2.mostrar()

        # Generamos nuevos edificios y naves/aviones
        if len(obstaculos) == 0 or obstaculos[-1].rect_edificio.right < ANCHO_PANTALLA - 200:
            obstaculos.append(Obstaculo(ANCHO_PANTALLA, espacio_entre_obstaculos))
        if len(estrellas) == 0 or estrellas[-1].rect.right < ANCHO_PANTALLA - 300:
            estrellas.append(Estrella(random.randint(ANCHO_PANTALLA, ANCHO_PANTALLA + 100), random.randint(50, ALTO_PANTALLA - 50)))

        # Mover y mostrar obstáculos
        for obstaculo in obstaculos:
            obstaculo.mover(velocidad_juego)
            obstaculo.mostrar()

        # Mover y mostrar estrellas
        for estrella in estrellas:
            estrella.mover(velocidad_juego)
            estrella.mostrar()

        # Eliminar obstáculos y estrellas fuera de pantalla
        obstaculos = [obstaculo for obstaculo in obstaculos if not obstaculo.fuera_pantalla()]
        estrellas = [estrella for estrella in estrellas if estrella.rect.right > 0]

        # Detección de colisiones
        if not modo_zen and detectar_colision(ovni1, obstaculos):
            ejecutando = False

        # Detectar colisión con estrellas
        for estrella in estrellas:
            if ovni1.rect.colliderect(estrella.rect):
                marcador += 10
                estrellas.remove(estrella)

        # Actualizar el marcador
        marcador += 0.01
        texto_marcador = fuente.render(f'Marcador: {int(marcador)}', True, (255, 255, 255))
        pantalla.blit(texto_marcador, (10, 10))

        # Aumentar dificultad
        velocidad_juego = 3 + int(marcador // 10)

        # Cambio de día a noche
        if int(marcador) % 50 == 0:
            fondo = imagen_fondo_dia if (int(marcador) // 50) % 2 == 0 else imagen_fondo_noche

        # Actualizar la pantalla
        pygame.display.update()
        reloj.tick(60)

    # Fin del juego, guardar puntuación y mostrar Game Over
    guardar_puntuacion(int(marcador))
    pantalla.fill((0, 0, 0))
    texto_game_over = fuente.render('Game Over', True, (255, 0, 0))
    pantalla.blit(texto_game_over, (ANCHO_PANTALLA // 2 - 70, ALTO_PANTALLA // 2 - 30))
    texto_reiniciar = fuente.render('Presiona R para reiniciar o M para volver al menú', True, (255, 255, 255))
    pantalla.blit(texto_reiniciar, (ANCHO_PANTALLA // 2 - 150, ALTO_PANTALLA // 2 + 10))
    pygame.display.update()

    # Espera hasta que el jugador presione R para reiniciar o M para ir al menú
    esperando_reinicio = True
    while esperando_reinicio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando_reinicio = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                ovni1, ovni2, obstaculos, estrellas, marcador, velocidad_juego, espacio_entre_obstaculos, fondo, modo_zen = reiniciar_juego(num_jugadores=num_jugadores)
                esperando_reinicio = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
                num_jugadores = mostrar_menu()
                jugar(num_jugadores=num_jugadores)

    jugar(num_jugadores=num_jugadores)

# Ejecutamos el juego
if __name__ == "__main__":
    num_jugadores = mostrar_menu()
    jugar(num_jugadores=num_jugadores)
