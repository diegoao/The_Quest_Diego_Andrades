import pygame as pg
from . import ALTO, ANCHO, NUMERONIVELES, RUTABASEDEDATOS, TIEMPO1ERNIVEL, TIEMPOSIGUIENTENIVEL, VELOCIDADINICIALOBJETOS, VIDASINICIALES
from TheQuest.escenas import PantallaInicio, PantallaPartida, PantallaRecords
from .entidades import (
    ContadorVidas,
    Marcador,
)
from .dbmanager import DBManager


class TheQuest:
    def __init__(self):
        pg.init()
        # Defino las dimensiones de la pantalla.
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.nivel = 1
        self.contadorvidas = ContadorVidas(VIDASINICIALES)
        self.marcador = Marcador()
        self.pantallainicial = False
        self.records = False
        self.empezarpartida = False
        self.datosrecords = []
        self.basedatos = DBManager(RUTABASEDEDATOS)
        self.tiemponivel = TIEMPO1ERNIVEL
        self.dificultadobjetos = VELOCIDADINICIALOBJETOS
        self.gotowindows = 'PantallaInicio'
        pg.display.set_caption('The Quest-Diego Andrades Oñate')

    def jugar(self):
        terminarJuego = False

        while not terminarJuego:

            self.gestion_niveles()

            if self.pantallainicial:
                terminarJuego, self.gotowindows = PantallaInicio(
                    self.pantalla).ejecutar_bucle()

            if self.empezarpartida:
                terminarJuego = PantallaPartida(
                    self.pantalla, self.nivel, self.contadorvidas,
                    self.marcador, self.tiemponivel, self.dificultadobjetos, self.basedatos).ejecutar_bucle()

                if self.nivel <= NUMERONIVELES:
                    self.tiemponivel = self.tiemponivel * TIEMPOSIGUIENTENIVEL
                    self.tiemponivel = round(self.tiemponivel)
                    self.dificultadobjetos = [
                        self.dificultadobjetos[0]+2, self.dificultadobjetos[1]+2]

                if self.contadorvidas.vidas <= 0 or self.nivel == NUMERONIVELES:
                    self.gotowindows = 'Records'
                else:
                    self.nivel += 1

            if self.records and not terminarJuego:
                terminarJuego, self.gotowindows = PantallaRecords(
                    self.pantalla, self.marcador, self.nivel, self.basedatos).ejecutar_bucle()
                self.resetpartida()

        # Cerramos pygame
        pg.quit()

    def gestion_niveles(self):
        if self.gotowindows == 'PantallaInicio':
            self.pantallainicial = True
            self.records = False
            self.empezarpartida = False
        elif self.gotowindows == 'EmpezarPartida':
            self.pantallainicial = False
            self.records = False
            self.empezarpartida = True
        elif self.gotowindows == 'Records':
            self.pantallainicial = False
            self.records = True
            self.empezarpartida = False

    def resetpartida(self):
        self.marcador.reset()
        self.contadorvidas.reset(VIDASINICIALES)
        self.nivel = 1
        self.tiemponivel = TIEMPO1ERNIVEL
        self.dificultadobjetos = VELOCIDADINICIALOBJETOS


if __name__ == '__main__':
    juego = TheQuest()
    juego.jugar()
