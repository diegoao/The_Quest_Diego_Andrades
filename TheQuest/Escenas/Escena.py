import pygame as pg

from TheQuest import ALTO, ANCHO, COLORFUENTE, DOS, RUTAFUENTESENCABEZADOS


class Escena:
    def __init__(self, pantalla):
        # Pasamos como atributo pantalla para mantener las caracteristicas en todas.
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def ejecutar_bucle(self):
        pass

    def pintar_mensaje(self, mensaje):
        mensaje = mensaje
        tamañofuente = 30
        self.tipo = pg.font.Font(RUTAFUENTESENCABEZADOS, tamañofuente)
        texto = self.tipo.render(mensaje, True, COLORFUENTE)
        pos_x = (ANCHO-texto.get_width())/DOS
        pos_y = (ALTO * 3/4) + texto.get_height()
        self.pantalla.blit(texto, (pos_x, pos_y))
