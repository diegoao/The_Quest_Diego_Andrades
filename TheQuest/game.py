import pygame as pg
from . import ALTO, ANCHO, VIDASINICIALES
from TheQuest.escenas import PantallaInicio, PantallaPartida, PantallaRecords


class TheQuest:
    def __init__(self):
        pg.init()
        # Defino las dimensiones de la pantalla.
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.pantallainicial = True
        self.nivel = 0
        self.vidas = VIDASINICIALES
        self.marcador = 0

    def jugar(self):
        terminarJuego = False
        while not terminarJuego:

            if self.pantallainicial:
                terminarJuego, empezarnivel = PantallaInicio(
                    self.pantalla).ejecutar_bucle()
                self.pantallainicial = False

            if empezarnivel:
                print(f'estas en nivel:{self.nivel}')
                terminarJuego, empezarnivel, vidas, marcador = PantallaPartida(
                    self.pantalla, self.nivel, self.vidas, self.marcador).ejecutar_bucle()
                self.nivel += 1
                self.vidas = vidas
                self.marcador = marcador

        # if self.record:
           # terminarJuego = PantallaRecords(self.pantalla).ejecutar_bucle()

        pg.quit()  # Cerramos pygame


if __name__ == '__main__':
    juego = TheQuest()
    juego.jugar()
