# estándar
import os
from random import randint

# librerías de terceros
import pygame as pg

# mis importaciones
from . import ALTO,  ANCHO, GROSORMARGENES, RUTAFUENTESENCABEZADOS, TAMAÑOMARGENESPARTIDA


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
            if self.rect.bottom < alturaNave + TAMAÑOMARGENESPARTIDA:
                self.rect.bottom = alturaNave + TAMAÑOMARGENESPARTIDA
        if pulsadas[pg.K_DOWN]:
            self.rect.y += self.velomovimiento
            if self.rect.top > ALTO-alturaNave-TAMAÑOMARGENESPARTIDA:
                self.rect.top = ALTO-alturaNave-TAMAÑOMARGENESPARTIDA


class Marcador:
    def __init__(self):
        self.valor = 0
        self.tipo_letra = pg.font.Font(RUTAFUENTESENCABEZADOS, 25)

    def aumentar(self, incremento):
        self.valor += incremento

    def pintar(self, pantalla):

        puntos = str(self.valor)
        cadena = f'Puntos del jugador: {puntos}'
        texto = self.tipo_letra.render(cadena, True, (255, 215, 0))
        altotexto = texto.get_height()
        pos_x = 20
        pos_y = (TAMAÑOMARGENESPARTIDA-altotexto)/2
        pantalla.blit(texto, (pos_x, pos_y))


class ContadorVidas:

    def __init__(self, vidas_iniciales):
        self.vidas = vidas_iniciales
        self.tipo_letra = pg.font.Font(RUTAFUENTESENCABEZADOS, 25)

    def perder_vida(self):
        self.vidas -= 1
        return self.vidas < 0

    def pintar(self, pantalla, vidas):
        margen = 0
        # Configuro texto vidas:
        cadena = 'VIDAS: '
        texto = self.tipo_letra.render(cadena, True, (255, 215, 0))
        anchotext, altotext = texto.get_size()
        pos_x = 20
        pos_y = ALTO - (TAMAÑOMARGENESPARTIDA-GROSORMARGENES+altotext)/2
        pantalla.blit(texto, (pos_x, pos_y))
        # Configuro imagenes visualizadoras de vida
        ruta = os.path.join('Recursos', 'imágenes', 'Componentes', 'vidas.png')
        self.logo = pg.image.load(ruta)
        anchoimagen, altoimagen = self.logo.get_size()
        pos_y = ALTO - (TAMAÑOMARGENESPARTIDA-GROSORMARGENES+altoimagen)/2

        for i in range(vidas):
            pantalla.blit(self.logo, (pos_x + anchotext+margen, pos_y))
            margen = margen + anchoimagen
