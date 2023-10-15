# estándar
import os
from random import randint

# librerías de terceros
import pygame as pg

# mis importaciones
from . import ALTO,  ANCHO


class NaveEspacial(pg.sprite.Sprite):
    """
    1. Debe ser de tipo Sprite (herencia) -- DONE
    2. Se puede mover (método)
        2.1 Leer el teclado
        2.2 Límites de movimiento (no debe salir de la pantalla)
    3. Pintarse (método) -- DONE
    4. Volver a la posición inicial (método)
    5. Velocidad  --- DONE
    """
    margen = 100
    velocidad = 20

    def __init__(self):
        super().__init__()

        self.imagenes = []
        for i in range(2):
            ruta_img = os.path.join(
                'Recursos', 'imágenes', 'Componentes', f'halcon{i}.png')
            print(f'halcon{i}')
            self.imagenes.append(pg.image.load(ruta_img))

        self.contador = 0
        self.image = self.imagenes[self.contador]
        anchuraNave = self.image.get_width()
        self.rect = self.image.get_rect(midbottom=(anchuraNave/2, ALTO/2))

    def update(self):
        # 00 -> 01 -> 00 -> 01
        self.contador += 1
        alturaNave = self.image.get_height()
        if self.contador > 1:
            self.contador = 0
        self.image = self.imagenes[self.contador]

        pulsadas = pg.key.get_pressed()
        if pulsadas[pg.K_UP]:
            self.rect.y -= self.velocidad
            if self.rect.bottom < alturaNave:
                self.rect.bottom = alturaNave
        if pulsadas[pg.K_DOWN]:
            self.rect.y += self.velocidad
            if self.rect.top > ALTO-alturaNave:
                self.rect.top = ALTO-alturaNave
