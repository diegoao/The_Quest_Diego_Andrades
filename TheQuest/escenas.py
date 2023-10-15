import os
import pygame as pg
from . import ALTO, ANCHO, COLORFUENTE, FPS, RUTAFUENTESENCABEZADOS
from .entidades import (
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
                    salir = True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    salir = True
            self.pantalla.blit(self.fondo, (0, 0))
            self.pintar_mensaje()
            pg.display.flip()  # Mostramos los cambios

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
        self.marcador = Marcador()

    def ejecutar_bucle(self):
        print('Has entrado en pantalla Partida del juego')
        super().ejecutar_bucle()
        salir = False
        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
            self.pantalla.blit(self.fondo, (0, 0))
            self.jugador.update()
            self.marcador.pintar(self.pantalla)
            self.pantalla.blit(self.jugador.image, self.jugador.rect)
            pg.draw.line(self.pantalla, COLORFUENTE, (0, 40), (ANCHO, 40), 5)
            pg.draw.line(self.pantalla, COLORFUENTE,
                         (0, ALTO-40), (ANCHO, ALTO-40), 5)
            pg.display.flip()  # Mostramos los cambios


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
