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
    margen = 25
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

        self.rect = self.image.get_rect(midbottom=(ANCHO/2, ALTO-self.margen))

    def update(self):
        # 00 -> 01 -> 00 -> 01
        self.contador += 1
        if self.contador > 1:
            self.contador = 0
        self.image = self.imagenes[self.contador]
