import os
import random
import pygame as pg
from . import ALTO, ANCHO, COLORFUENTE, FPS, GROSORMARGENES, RUTAFUENTESENCABEZADOS, TAMAÑOMARGENESPARTIDA, VIDASINICIALES
from .entidades import (
    Asteroide,
    ContadorVidas,
    Marcador,
    NaveEspacial
)


class Escena:
    def __init__(self, pantalla):
        # Pasamos como atributo pantalla para mantener las caracteristicas en todas.
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def ejecutar_bucle(self):
        pass


class PantallaInicio(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        # Cargo la imagen de la pantalla principal
        ruta = os.path.join('Recursos', 'imágenes',
                            'Fondos', 'ImagenPortada.png')
        self.fondo = pg.image.load(ruta)
        self.tipo = pg.font.Font(RUTAFUENTESENCABEZADOS, 30)
        print("Has entrado en pantalla de incio del juego")

    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    salir = True
            self.pantalla.blit(self.fondo, (0, 0))
            self.pintar_mensaje()
            pg.display.flip()  # Mostramos los cambios
        return False

    def pintar_mensaje(self):
        mensaje = "Pulsa <ESPACIO> para empezar la partida"
        texto = self.tipo.render(mensaje, True, (255, 215, 0))
        pos_x = (ANCHO-texto.get_width())/2
        pos_y = ALTO * 3/4
        self.pantalla.blit(texto, (pos_x, pos_y))

#####################################


class PantallaPartida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.jugador = NaveEspacial()
        ruta = os.path.join('Recursos', 'imágenes',
                            'Fondos', 'FondoPartida.png')
        self.fondo = pg.image.load(ruta)
        self.contador_vidas = ContadorVidas(VIDASINICIALES)
        self.marcador = Marcador()
        self.asteroides = pg.sprite.Group()

    def ejecutar_bucle(self):
        print('Has entrado en pantalla Partida del juego')
        super().ejecutar_bucle()
        creacion = 0
        salir = False
        self.crear_asteroide()

        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
            self.pantalla.blit(self.fondo, (0, 0))
            self.jugador.update()
            self.marcador.pintar(self.pantalla)
            self.pantalla.blit(self.jugador.image, self.jugador.rect)
            self.margenes()
            vidas = self.contador_vidas.vidas
            self.asteroides.draw(self.pantalla)
            self.contador_vidas.pintar(self.pantalla, vidas)
            self.timerSeg = round(pg.time.get_ticks() / 1000, 0)

            # Creo y actualizo la posición del Asteroide
            if (creacion+1) == self.timerSeg:
                creacion = self.timerSeg
                self.crear_asteroide()
            grupoAsteroides = pg.sprite.Group.sprites(self.asteroides)
            for asteroide in grupoAsteroides:
                if asteroide.update():
                    self.marcador.aumentar(asteroide.puntos)

            # Detecto las colisiones y si surgen resto vidas hasta que me quedo sin ninguna y cierro el juego
            colisiones = pg.sprite.spritecollide(
                self.jugador, self.asteroides, False)
            if len(colisiones) > 0:
                for i in colisiones:
                    i.kill()
                if self.contador_vidas.vidas > 0:
                    self.contador_vidas.perder_vida()
            if self.contador_vidas.vidas <= 0:
                salir = True

            pg.display.flip()  # Mostramos los cambios

        return False

    def margenes(self):
        pg.draw.line(self.pantalla, COLORFUENTE, (0,
                                                  TAMAÑOMARGENESPARTIDA), (ANCHO, TAMAÑOMARGENESPARTIDA), GROSORMARGENES)
        pg.draw.line(self.pantalla, COLORFUENTE,
                     (0, ALTO-TAMAÑOMARGENESPARTIDA), (ANCHO, ALTO-TAMAÑOMARGENESPARTIDA), GROSORMARGENES)

    def crear_asteroide(self):
        tipo = None
        velocidadmin = 12
        velocidadmax = 20
        tipoAsteroides = [Asteroide.CAZA,
                          Asteroide.ASTEROIDE1, Asteroide.ASTEROIDE2]
        puntos = [30, 22, 12]
        tipo = random.randint(0, 2)
        velocidad = random.randint(velocidadmin, velocidadmax)
        asteroide = Asteroide(
            puntos[tipo], tipoAsteroides[tipo], velocidad)
        asteroide.rect.x = ANCHO + asteroide.rect.height
        asteroide.rect.y = random.randint(
            TAMAÑOMARGENESPARTIDA, ALTO-TAMAÑOMARGENESPARTIDA-asteroide.rect.width)
        self.asteroides.add(asteroide)


#####################################


class PantallaRecords(Escena):
    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
            self.pantalla.fill((0, 0, 255))
            pg.display.flip()  # Mostramos los cambios
