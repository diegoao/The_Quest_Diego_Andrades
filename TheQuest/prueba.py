import pygame as pg
from pygame.locals import *
import sys


# estándar
import os
from random import randint


# mis importaciones
ANCHO, ALTO = 900, 700


class Coche(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.imagenes = []
        for i in range(5):
            ruta_img = os.path.join(
                'Recursos', 'imágenes', 'Componentes', f'halcon{i}.png')
            self.imagenes.append(pg.image.load(ruta_img))
        self.contador = 0
        self.image = self.imagenes[1]
        self.original = self.image
        self.anchuraNave = self.image.get_width()
        self.rect = self.image.get_rect(midbottom=(self.anchuraNave/2, ALTO/2))
        self.rectoriginal = self.rect
        self.angulogiro = 0

    def update(self, colision, partida, aterrizar=None):
        self.partidainiciada = partida
        self.choque = colision
        self.contador += 1
        self.image = self.imagenes[1]
        self.aterrizar(aterrizar)

    def aterrizar(self, aterrizar):
        if aterrizar:
            velocidad = 1
            if True:  # self.angulogiro != 180:

                self.image = pg.transform.rotate(
                    self.original, self.angulogiro)
                self.rect = self.image.get_rect(
                    center=self.rectoriginal.center)
                self.angulogiro += 1


# Pantalla
PANTALLA = pg.display.set_mode((ANCHO, ALTO))
FPS = 25
RELOJ = pg.time.Clock()

# Fondo del juego
fondo = pg.image.load(
    "Recursos/imágenes/Fondos/FondoPartida.png").convert()
x = 0
y = 0
PANTALLA.blit(fondo, (x, y))
jugador = Coche()

# Bucle de juego.
while True:
    # Cerrar Juego
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    PANTALLA.blit(fondo, (0, 0))
    jugador.update(False, True, True)
    PANTALLA.blit(jugador.image, jugador.rect)
    pg.display.flip()  # Mostramos los cambios

    x += 1
    # Control de FPS
    RELOJ.tick(FPS)
    # Actualización de la ventana
    pg.display.update()
