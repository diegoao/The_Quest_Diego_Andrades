import os
import pygame as pg
from . import ALTO, ANCHO


class Escena:
    def __init__(self, pantalla):
        # Pasamos como atributo pantalla para mantener las caracteristicas en todas.
        self.pantalla = pantalla

    def ejecutar_bucle(self):
        pass


class PantallaPrincipal(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        # Cargo la imagen de la pantalla principal
        ruta = os.path.join('imágenes', 'Fondos', 'ImagenPortada.png')
        self.fondo = pg.image.load(ruta)

    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
            self.pantalla.blit(self.fondo, (0, 0))
            pg.display.flip()  # Mostramos los cambios


class PantallaPartida(Escena):
    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True

            pg.display.flip()  # Mostramos los cambios


class PantallaRecords(Escena):
    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True

            pg.display.flip()  # Mostramos los cambios
