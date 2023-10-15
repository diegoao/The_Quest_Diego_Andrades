import pygame as pg
from . import ALTO, ANCHO
from TheQuest.escenas import PantallaInicio, PantallaPartida, PantallaRecords


class TheQuest:
    def __init__(self):
        pg.init()
        # Defino las dimensiones de la pantalla.
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))

        self.escenas = [
            PantallaInicio(self.pantalla),
            PantallaPartida(self.pantalla),
            PantallaRecords(self.pantalla)
        ]

    def jugar(self):
        for escena in self.escenas:
            escena.ejecutar_bucle()

        pg.quit()  # Cerramos pygame


if __name__ == '__main__':
    juego = TheQuest()
    juego.jugar()
