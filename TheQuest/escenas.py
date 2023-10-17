import os
import random
import pygame as pg
from . import ALTO, ANCHO, COLORFUENTE, FPS, GROSORMARGENES, RUTAFUENTESENCABEZADOS, TAMAÑOMARGENESPARTIDA, VIDASINICIALES
from .entidades import (
    Asteroide,
    ContadorVidas,
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
                    return True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    salir = True
            self.pantalla.blit(self.fondo, (0, 0))
            self.pintar_mensaje()
            pg.display.flip()  # Mostramos los cambios
        return False

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
        self.contador_vidas = ContadorVidas(VIDASINICIALES)
        self.asteroides = pg.sprite.Group()

    def ejecutar_bucle(self):
        print('Has entrado en pantalla Partida del juego')
        super().ejecutar_bucle()
        self.crear_asteroide()
        grupo = pg.sprite.Group.sprites(self.asteroides)
        salir = False
        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
            self.pantalla.blit(self.fondo, (0, 0))
            self.jugador.update()
            self.marcador.pintar(self.pantalla)
            self.pantalla.blit(self.jugador.image, self.jugador.rect)
            self.margenes()
            vidas = self.contador_vidas.vidas
            self.asteroides.draw(self.pantalla)
            self.contador_vidas.pintar(self.pantalla, vidas)
            self.asteroides.update(grupo[1])
            print(pg.sprite.Group.sprites(self.asteroides))
            # self.asteroides.update(self.asteroides)
            pg.display.flip()  # Mostramos los cambios
        return False

    def margenes(self):
        pg.draw.line(self.pantalla, COLORFUENTE, (0,
                                                  TAMAÑOMARGENESPARTIDA), (ANCHO, TAMAÑOMARGENESPARTIDA), GROSORMARGENES)
        pg.draw.line(self.pantalla, COLORFUENTE,
                     (0, ALTO-TAMAÑOMARGENESPARTIDA), (ANCHO, ALTO-TAMAÑOMARGENESPARTIDA), GROSORMARGENES)

    def crear_asteroide(self):
        numeroAsterorides = 2
        tipo = None
        velocidadmin = 1
        velocidadmax = 10
        tipoAsteroides = [Asteroide.CAZA,
                          Asteroide.ASTEROIDE1, Asteroide.ASTEROIDE2]
        puntos = [30, 22, 12]
        contador = 1
        while contador <= numeroAsterorides:
            tipo = random.randint(0, 2)
            velocidad = random.randint(velocidadmin, velocidadmax)
            asteroide = Asteroide(
                puntos[tipo], tipoAsteroides[tipo], velocidad)
            asteroide.rect.x = ANCHO + asteroide.rect.height
            asteroide.rect.y = random.randint(
                TAMAÑOMARGENESPARTIDA, ALTO-TAMAÑOMARGENESPARTIDA-asteroide.rect.width)
            self.asteroides.add(asteroide)
            contador += 1


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
