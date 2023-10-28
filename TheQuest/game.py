import pygame as pg
from . import ALTO, ANCHO, NUMERORECORS, RUTABASEDEDATOS, VIDASINICIALES
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
        self.nivel = 0
        self.contadorvidas = ContadorVidas(VIDASINICIALES)
        self.marcador = Marcador()
        self.gameover = False
        self.datosrecords = []
        self.basedatos = DBManager(RUTABASEDEDATOS)

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
                    self.pantalla, self.nivel, self.contadorvidas, self.marcador).ejecutar_bucle()
            self.nivel += 1

            if self.contadorvidas.vidas <= 0:
                empezarnivel = False
                self.gameover = True
            else:
                empezarnivel = True

            if self.gameover:
                terminarJuego = PantallaRecords(self.pantalla).ejecutar_bucle()

        self.basedatos.desconectar()
        pg.quit()

    def connectandcreatetable(self):
        self.basedatos.conectar()
        sql = 'SELECT Fecha, Nombre, Puntuación, id FROM records'
        try:
            # Leo datos al inciar el juego para mostrar records
            self.datosrecords = self.basedatos.consultaSQL(sql)
        except:
            # Si hay error es porque no existe la tabla y la creo con el numero de records en blanco
            self.basedatos.creartabla()
            sql = 'INSERT INTO records (Fecha,Nombre,Puntuación) VALUES (?, ?, ?)'
            parametros = ('xx-xx-xxxx', 'Jugador', 0)
            for i in range(NUMERORECORS):
                self.basedatos.nuevo(sql, parametros)
            self.datosrecords = self.basedatos.consultaSQL(
                sql)  # Cerramos pygame


if __name__ == '__main__':
    juego = TheQuest()
    juego.jugar()
