import pygame as pg
import random
from . import ALTO, ANCHO, INCREMENTODIFICULTAD, NUMERONIVELES, RUTABASEDEDATOS, TIEMPO1ERNIVEL, TIEMPOSIGUIENTENIVEL, VELOCIDADINICIALOBJETOS, VIDASINICIALES
from TheQuest.Escenas.PantallaInicial import PantallaInicio
from TheQuest.Escenas.PantallaJuego import PantallaPartida
from TheQuest.Escenas.PantallaRecods import Records
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
        self.nivelinicial = 1
        self.nivel = self.nivelinicial
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
        self.ofdeparture = False
        self.repetirbucle = -1

    def jugar(self):
        terminarJuego = False
        pg.mixer.music.load('Recursos/Sonidos/Niveles/Portada.wav')
        pg.mixer.music.play(self.repetirbucle)
        while not terminarJuego:
            self.gestion_pantallas()
            if self.pantallainicial:
                terminarJuego, self.gotowindows = PantallaInicio(
                    self.pantalla).ejecutar_bucle()

            if self.empezarpartida:
                terminarJuego = PantallaPartida(
                    self.pantalla, self.nivel, self.contadorvidas,
                    self.marcador, self.tiemponivel, self.dificultadobjetos, self.basedatos).ejecutar_bucle()
                pg.mixer.music.stop()
                self.gestion_niveles()

            if self.records and not terminarJuego:
                terminarJuego, self.gotowindows = Records(
                    self.pantalla, self.marcador, self.nivel, self.basedatos).ejecutar_bucle()
                self.resetpartida()
                if self.ofdeparture:
                    pg.mixer.music.stop()
                    pg.mixer.music.load('Recursos/Sonidos/Niveles/Portada.wav')
                    pg.mixer.music.play(self.repetirbucle)

        # Cerramos pygame
        pg.quit()

    def gestion_niveles(self):
        if self.nivel <= NUMERONIVELES:
            self.tiemponivel = self.tiemponivel * TIEMPOSIGUIENTENIVEL
            self.tiemponivel = round(self.tiemponivel)
            self.dificultadobjetos = [
                self.dificultadobjetos[0]+INCREMENTODIFICULTAD, self.dificultadobjetos[1]+INCREMENTODIFICULTAD]

        if self.contadorvidas.vidas <= 0 or self.nivel == NUMERONIVELES:
            self.ofdeparture = True
            self.gotowindows = 'Records'
        else:
            self.nivel += 1

    def gestion_pantallas(self):
        tiempomin = 1
        tiempomax = 60
        if self.gotowindows == 'PantallaInicio':
            self.pantallainicial = True
            self.records = False
            self.empezarpartida = False
            self.ofdeparture = False
        elif self.gotowindows == 'EmpezarPartida':
            pg.mixer.music.stop()
            self.pantallainicial = False
            self.records = False
            self.empezarpartida = True
            pg.mixer.music.load('Recursos/Sonidos/Niveles/nivel.wav')
            pg.mixer.music.play(self.repetirbucle,
                                random.randint(tiempomin, tiempomax))
        elif self.gotowindows == 'Records':
            self.pantallainicial = False
            self.records = True
            self.empezarpartida = False
            if self.ofdeparture:
                pg.mixer.music.load('Recursos/Sonidos/Niveles/records.wav')
                pg.mixer.music.play(self.repetirbucle)

    def resetpartida(self):
        self.marcador.reset()
        self.contadorvidas.reset(VIDASINICIALES)
        self.nivel = self.nivelinicial
        self.tiemponivel = TIEMPO1ERNIVEL
        self.dificultadobjetos = VELOCIDADINICIALOBJETOS


if __name__ == '__main__':
    juego = TheQuest()
    juego.jugar()
