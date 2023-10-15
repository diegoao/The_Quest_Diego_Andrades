# estándar
import os
from random import randint

# librerías de terceros
import pygame as pg

# mis importaciones
from . import ALTO,  ANCHO


class NaveEspacial(pg.sprite.Sprite):

    margen = 100
    velocidadMin = 20
    velocidadMax = 60
    aumentoVelo = 2

    def __init__(self):
        super().__init__()

        self.imagenes = []
        for i in range(2):
            ruta_img = os.path.join(
                'Recursos', 'imágenes', 'Componentes', f'halcon{i}.png')
            self.imagenes.append(pg.image.load(ruta_img))

        self.contador = 0
        self.image = self.imagenes[self.contador]
        anchuraNave = self.image.get_width()
        self.rect = self.image.get_rect(midbottom=(anchuraNave/2, ALTO/2))
        self.velomovimiento = self.velocidadMin

    def update(self):
        # 00 -> 01 -> 00 -> 01
        alturaNave = self.image.get_height()
        self.contador += 1
        if self.contador > 1:
            self.contador = 0
        self.image = self.imagenes[self.contador]
        pulsadas = pg.key.get_pressed()

        if ((pulsadas[pg.K_UP] and not pulsadas[pg.K_DOWN]) or (pulsadas[pg.K_DOWN] and not pulsadas[pg.K_UP])) and self.velomovimiento < self.velocidadMax:
            self.velomovimiento += self.aumentoVelo
        elif (not pulsadas[pg.K_UP] and not pulsadas[pg.K_DOWN]) or (pulsadas[pg.K_UP] and pulsadas[pg.K_DOWN]):
            self.velomovimiento = self.velocidadMin

        if pulsadas[pg.K_UP]:
            self.rect.y -= self.velomovimiento
            if self.rect.bottom < alturaNave:
                self.rect.bottom = alturaNave
        if pulsadas[pg.K_DOWN]:
            self.rect.y += self.velomovimiento
            if self.rect.top > ALTO-alturaNave:
                self.rect.top = ALTO-alturaNave
