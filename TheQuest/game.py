import pygame as pg
from . import ALTO, ANCHO
from TheQuest.escenas import PantallaInicio, PantallaPartida, PantallaRecords


class TheQuest:
    def __init__(self):
        pg.init()
        # Defino las dimensiones de la pantalla.
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.pantallainicial = True
        self.nivel = 0

    def jugar(self):
        terminarJuego = False
        while not terminarJuego:
            if self.pantallainicial:
                terminarJuego, empezarNivel0 = PantallaInicio(
                    self.pantalla).ejecutar_bucle()
                self.pantallainicial = False

            if empezarNivel0:
                print(f'estas en nivel:{self.nivel}')
                terminarJuego, empezarNivel1 = PantallaPartida(
                    self.pantalla, self.nivel).ejecutar_bucle()

            if empezarNivel1:
                self.nivel += 1
                print(f'estas en nivel:{self.nivel}')
                terminarJuego, empezarNivel2 = PantallaPartida(
                    self.pantalla, self.nivel).ejecutar_bucle()
            if empezarNivel2:
                self.nivel += 1
                print(f'estas en nivel:{self.nivel}')
                terminarJuego, self.pantallainicial = PantallaPartida(
                    self.pantalla, self.nivel).ejecutar_bucle()
                print(f'valor pantalla inicial:{self.pantallainicial}')
                print(f'valor pantalla terminarjuego:{terminarJuego}')

        # if self.record:
           # terminarJuego = PantallaRecords(self.pantalla).ejecutar_bucle()

        pg.quit()  # Cerramos pygame


if __name__ == '__main__':
    juego = TheQuest()
    juego.jugar()
