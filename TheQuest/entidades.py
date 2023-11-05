# Estándar
import os
import math


# Librerías de terceros
import pygame as pg

# Mis importaciones
from . import ALTO,  ANCHO, COLORFUENTE, COLORWARNING, DOS, GROSORMARGENES, NUMERONIVELES, RUTAFUENTESENCABEZADOS, TAMAÑOFUENTEMARCADORES, TAMAÑOMARGENESPARTIDA


class NaveEspacial(pg.sprite.Sprite):

    margen = 100
    velocidadMin = 20
    velocidadMax = 60
    aumentoVelo = 2
    angulogiro = 0

    def __init__(self):
        super().__init__()
        self.imagenes = []
        for i in range(5):
            ruta_img = os.path.join(
                'Recursos', 'imágenes', 'Componentes', f'halcon{i}.png')
            self.imagenes.append(pg.image.load(ruta_img))
        self.contador = 0
        self.image = self.imagenes[self.contador]
        self.anchuraNave = self.image.get_width()
        self.rect = self.image.get_rect(
            midbottom=(self.anchuraNave/DOS, ALTO/DOS))
        self.velomovimiento = self.velocidadMin
        self.angulogiro = 0
        self.sonidoexplosion = pg.mixer.Sound(
            'Recursos/Sonidos/Niveles/Explosion.wav')
        self.subir = True
        self.bajar = False

    def update(self, colision=False, partida=False, aterrizar=None, mododemo=False):
        self.partidainiciada = partida
        self.choque = colision
        alturaNave = self.image.get_height()
        self.contador += 1
        self.cambiarImagenesNave()
        self.image = self.imagenes[self.contador]
        self.originimage = self.imagenes[self.contador]
        pulsadas = pg.key.get_pressed()
        if mododemo:
            self.mododemo()
        else:
            self.gestionTeclas(alturaNave, pulsadas)
        self.aterrizar(aterrizar)
        if self.angulogiro == 180:
            self.image = pg.transform.rotate(
                self.originimage, self.angulogiro)

    def aterrizar(self, aterrizar):
        if aterrizar:
            velocidad = 3
            angulogiro = 2
            if self.angulogiro != 180:
                self.angulogiro += angulogiro
                self.image = pg.transform.rotate(
                    self.originimage, self.angulogiro)
                self.rect = self.image.get_rect(
                    center=self.rect.center)
            else:
                if self.rect.y > (ALTO-self.anchuraNave)/DOS:
                    self.rect.y -= velocidad
                if self.rect.y < (ALTO-self.anchuraNave)/DOS:
                    self.rect.y += velocidad
                self.rect.x += velocidad

    def cambiarImagenesNave(self):
        if not self.choque:
            if self.contador > 1:
                self.contador = 0
        else:
            self.sonidoexplosion.play()
            if self.contador > 4:
                self.contador = 2

    def gestionTeclas(self, alturaNave, pulsadas):
        if ((pulsadas[pg.K_UP] and not pulsadas[pg.K_DOWN]) or (pulsadas[pg.K_DOWN] and not pulsadas[pg.K_UP])) and self.velomovimiento < self.velocidadMax:
            self.velomovimiento += self.aumentoVelo
        elif (not pulsadas[pg.K_UP] and not pulsadas[pg.K_DOWN]) or (pulsadas[pg.K_UP] and pulsadas[pg.K_DOWN]):
            self.velomovimiento = self.velocidadMin
        if self.partidainiciada:
            if pulsadas[pg.K_UP]:
                self.rect.y -= self.velomovimiento
                if self.rect.bottom < alturaNave + TAMAÑOMARGENESPARTIDA:
                    self.rect.bottom = alturaNave + TAMAÑOMARGENESPARTIDA
            if pulsadas[pg.K_DOWN]:
                self.rect.y += self.velomovimiento
                if self.rect.top > ALTO-alturaNave-TAMAÑOMARGENESPARTIDA:
                    self.rect.top = ALTO-alturaNave-TAMAÑOMARGENESPARTIDA

    def reset(self):
        self.rect = self.image.get_rect(
            midbottom=(self.anchuraNave/DOS, ALTO/DOS))

    def mododemo(self):
        velocidaddemo = 7
        if self.rect.y > ALTO-(ALTO/2.5) or self.bajar:
            self.subir = False
            self.bajar = True
            self.rect.y -= velocidaddemo
        if self.rect.y < ALTO/4 or self.subir:
            self.bajar = False
            self.subir = True
            self.rect.y += velocidaddemo


class Marcador:
    def __init__(self, puntos=0):
        self.valor = puntos
        self.tipo_letra = pg.font.Font(
            RUTAFUENTESENCABEZADOS, TAMAÑOFUENTEMARCADORES)

    def aumentar(self, incremento):

        self.valor += incremento

    def pintar(self, pantalla):

        puntos = str(self.valor)
        cadena = f'Puntos del jugador: {puntos}'
        texto = self.tipo_letra.render(cadena, True, COLORFUENTE)
        altotexto = texto.get_height()
        pos_x = 20
        pos_y = (TAMAÑOMARGENESPARTIDA-altotexto)/DOS
        pantalla.blit(texto, (pos_x, pos_y))

    def reset(self):
        self.valor = 0


class ContadorVidas:

    def __init__(self, vidas_iniciales):
        self.vidas = vidas_iniciales
        self.tipo_letra = pg.font.Font(
            RUTAFUENTESENCABEZADOS, TAMAÑOFUENTEMARCADORES)

    def perder_vida(self):
        self.vidas -= 1
        return self.vidas < 0

    def pintar(self, pantalla, vidas):
        margen = 0
        # Configuro texto vidas:
        cadena = 'VIDAS: '
        texto = self.tipo_letra.render(cadena, True, COLORFUENTE)
        anchotext, altotext = texto.get_size()
        pos_x = 20
        pos_y = ALTO - (TAMAÑOMARGENESPARTIDA-GROSORMARGENES+altotext)/DOS
        pantalla.blit(texto, (pos_x, pos_y))
        # Configuro imagenes visualizadoras de vida
        ruta = os.path.join('Recursos', 'imágenes', 'Componentes', 'vidas.png')
        self.logo = pg.image.load(ruta)
        anchoimagen, altoimagen = self.logo.get_size()
        pos_y = ALTO - (TAMAÑOMARGENESPARTIDA-GROSORMARGENES+altoimagen)/DOS
        for i in range(vidas):
            pantalla.blit(self.logo, (pos_x + anchotext+margen, pos_y))
            margen = margen + anchoimagen

    def reset(self, vidas_inciales):
        self.vidas = vidas_inciales


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
            self.kill()
            return True
        return False


class TemporizadorNivel:
    def __init__(self, tiempo):
        self.valor = 1
        self.tipo_letra = pg.font.Font(
            RUTAFUENTESENCABEZADOS, TAMAÑOFUENTEMARCADORES)
        self.inicialNivel = tiempo

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
        pos_y = (TAMAÑOMARGENESPARTIDA-altotexto)/DOS
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
        self.rect.x = ANCHO
        self.rect.y = (ALTO-self.rect.width)/DOS
        self.velocidad = self.movimiento

    def update(self):
        if self.rect.x >= ANCHO * 0.65:
            self.rect.x -= self.velocidad
            return True
        return False

    def reset(self):
        self.rect.x = ANCHO


class Mensajes:
    def __init__(self):
        self.alto = 0
        self.ancho = 0

    def pintar(self, pantalla, mensaje, tamaño=45, nivel=0):
        if nivel == NUMERONIVELES:
            color = (127, 255, 212)
        else:
            color = COLORFUENTE
        self.tipo_letra = pg.font.Font(RUTAFUENTESENCABEZADOS, tamaño)
        cadena = mensaje
        offset = 0
        for i in cadena:
            texto = self.tipo_letra.render(i, True, color)
            self.alto = texto.get_height()
            self.ancho = texto.get_width()
            pos_x = (ANCHO-self.ancho)/DOS
            pos_y = (ALTO-self.alto)/DOS
            pantalla.blit(texto, (pos_x, pos_y + offset))
            offset = self.alto


class Timerchangewindows:
    def __init__(self, timer):
        self.timerinic = timer
        self.timeiniciowindows = round(pg.time.get_ticks() / 1000, 0)
        self.timer = self.timerinic
        self.temporizador = 0

    def counter(self):
        self.timersecond = round(pg.time.get_ticks() / 1000, 0)
        self.temporizador = (math.trunc(
            self.timersecond-self.timeiniciowindows))
        if self.timer > 0:
            self.timer = self.timerinic
            self.timer -= self.temporizador
        else:
            return True

    def reset(self):
        self.timer = self.timerinic
        self.timeiniciowindows = round(pg.time.get_ticks() / 1000, 0)
