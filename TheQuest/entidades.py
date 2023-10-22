# estándar
import os
from random import randint

# librerías de terceros
import pygame as pg

# mis importaciones
from . import ALTO,  ANCHO, COLORFUENTE, COLORWARNING, GROSORMARGENES, RUTAFUENTESENCABEZADOS, TAMAÑOMARGENESPARTIDA, TIEMPONIVEL


class NaveEspacial(pg.sprite.Sprite):

    margen = 100
    velocidadMin = 20
    velocidadMax = 60
    aumentoVelo = 2

    def __init__(self):
        super().__init__()
        self.imagenes = []
        for i in range(5):
            ruta_img = os.path.join(
                'Recursos', 'imágenes', 'Componentes', f'halcon{i}.png')
            self.imagenes.append(pg.image.load(ruta_img))
        self.contador = 0
        self.image = self.imagenes[self.contador]
        anchuraNave = self.image.get_width()
        self.rect = self.image.get_rect(midbottom=(anchuraNave/2, ALTO/2))
        self.velomovimiento = self.velocidadMin
        self.sonidoexplosion = pg.mixer.Sound(
            'Recursos/Sonidos/Niveles/Explosion.wav')

    def update(self, colision=None):
        self.choque = colision
        alturaNave = self.image.get_height()
        self.contador += 1
        if not self.choque:
            if self.contador > 1:
                self.contador = 0
        else:
            self.sonidoexplosion.play()
            if self.contador > 4:
                self.contador = 2

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


class Asteroide(pg.sprite.Sprite):
    CAZA = 0
    ASTEROIDE1 = 1
    ASTEROIDE2 = 2
    IMG_ASTEROIDES = ['caza.png', 'asteroide.png', 'asteroide1.png']

    def __init__(self, puntos, modalidad=CAZA, velocidad=20):
        super().__init__()
        self.tipo = modalidad
        self.imagenes = []
        self.contador = 0
        for img in self.IMG_ASTEROIDES:
            ruta = os.path.join(
                'Recursos', 'imágenes', 'Componentes', img)
            self.imagenes.append(pg.image.load(ruta))
        self.image = self.imagenes[modalidad]
        self.rect = self.image.get_rect()
        self.puntos = puntos
        self.velocidad = velocidad

    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.x < 0:
            print('eliminado por update')
            self.kill()
            return True
        return False


class TemporizadorNivel:
    def __init__(self, nivel):
        self.valor = 1
        self.tipo_letra = pg.font.Font(RUTAFUENTESENCABEZADOS, 25)
        self.inicialNivel = TIEMPONIVEL[nivel]

    def decrementar(self, temporizador):
        if self.valor > 0:
            self.valor = self.inicialNivel
            self.valor -= temporizador

    def pintar(self, pantalla):

        segundos = str(self.valor)
        cadena = f'Tiempo del nivel: {segundos}'
        if self.valor > 10:
            texto = self.tipo_letra.render(cadena, True, COLORFUENTE)
        else:
            texto = self.tipo_letra.render(cadena, True, COLORWARNING)
        altotexto = texto.get_height()
        pos_x = 500
        pos_y = (TAMAÑOMARGENESPARTIDA-altotexto)/2
        pantalla.blit(texto, (pos_x, pos_y))


class Planeta:

    IMG_PLANETAS = ['Planeta0.png', 'Planeta1.png', 'Planeta2.png']
    movimiento = 2

    def crearplaneta(self, modalidad=0):
        self.tipo = modalidad
        self.imagenes = []
        ruta = os.path.join(
            'Recursos', 'imágenes', 'Planetas', self.IMG_PLANETAS[self.tipo])
        self.imagenes.append(pg.image.load(ruta))
        self.image = self.imagenes[self.tipo]
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO + (self.rect.height/2)
        self.rect.y = (ALTO-self.rect.width)/2
        self.velocidad = self.movimiento

    def update(self):
        print('actualizando posicion planeta')
        print(f'posicionx planeta {self.rect.x}')
        if self.rect.x >= ANCHO * 0.65:
            self.rect.x -= self.velocidad
            return True
        return False
