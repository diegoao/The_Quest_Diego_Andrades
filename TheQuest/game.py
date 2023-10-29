import pygame as pg
from . import ALTO, ANCHO, NUMERONIVELES, NUMERORECORS, RUTABASEDEDATOS, TIEMPO1ERNIVEL, TIEMPOSIGUIENTENIVEL, VELOCIDADINICIALOBJETOS, VIDASINICIALES
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
        self.pantallainicial = True
        self.nivel = 1
        self.contadorvidas = ContadorVidas(VIDASINICIALES)
        self.marcador = Marcador()
        self.gameover = False
        self.datosrecords = []
        self.basedatos = DBManager(RUTABASEDEDATOS)
        self.tiemponivel = TIEMPO1ERNIVEL
        self.dificultadobjetos = VELOCIDADINICIALOBJETOS

    def jugar(self):
        terminarJuego = False
        self.connectandcreatetable()

        while not terminarJuego:

            if self.pantallainicial:
                terminarJuego, empezarnivel = PantallaInicio(
                    self.pantalla).ejecutar_bucle()
                self.pantallainicial = False

            if empezarnivel:
                print(f'estas en nivel:{self.nivel}')
                terminarJuego = PantallaPartida(
                    self.pantalla, self.nivel, self.contadorvidas,
                    self.marcador, self.tiemponivel, self.dificultadobjetos).ejecutar_bucle()

            if self.nivel <= NUMERONIVELES:
                self.tiemponivel = self.tiemponivel * TIEMPOSIGUIENTENIVEL
                self.tiemponivel = round(self.tiemponivel)
                self.dificultadobjetos = [
                    self.dificultadobjetos[0]+2, self.dificultadobjetos[1]+2]

            if self.contadorvidas.vidas <= 0 or self.nivel == NUMERONIVELES:
                empezarnivel = False
                self.gameover = True
            else:
                self.nivel += 1
                empezarnivel = True
                # self.gameover = True

            if self.gameover:
                terminarJuego = PantallaRecords(
                    self.pantalla, self.basedatos).ejecutar_bucle()

        # Cerramos pygame
        pg.quit()

    def connectandcreatetable(self):
        self.basedatos.conectar()
        puntosinciales = 0
        sql = 'SELECT Fecha, Nombre, Puntuación, id FROM records'
        try:
            # Leo datos al inciar el juego para mostrar records
            print(self.basedatos.consultaSQL(sql))
        except:
            # Si hay error es porque no existe la tabla y la creo con el numero de records en blanco
            self.basedatos.creartabla()
            sql = 'INSERT INTO records (Fecha,Nombre,Puntuación) VALUES (?, ?, ?)'
            parametros = ('xx-xx-xxxx', 'Jugador', puntosinciales)
            for i in range(NUMERORECORS):
                self.basedatos.nuevo(sql, parametros)


if __name__ == '__main__':
    juego = TheQuest()
    juego.jugar()
