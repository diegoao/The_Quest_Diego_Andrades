import math
import os
import random
import pygame as pg
from TheQuest import ALTO, ANCHO, COLORFUENTE, DOS, FPS, GAMEHISTORY, INSTRUCCIONES, POSICION0, RUTAFUENTESENCABEZADOS, PUNTOSNAVE, WINDOWSTIME
from TheQuest.entidades import (
    Asteroide,
    NaveEspacial,
    Timerchangewindows
)
from TheQuest.Escenas.Escena import Escena


class PantallaInicio(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.nextwindows = ''
        self.timernextwindows = Timerchangewindows(WINDOWSTIME)
        # Cargo la imagen de la pantalla principal
        ruta = os.path.join('Recursos', 'imágenes',
                            'Fondos', 'ImagenPortada.png')
        self.fondo = pg.transform.scale(pg.image.load(ruta), (ANCHO, ALTO))
        self.inciarpartida = False
        self.jugador = NaveEspacial()
        self.asteroides = pg.sprite.Group()
        self.colision = False
        self.mododemo = True
        self.partida = False
        self.aterrizar = False
        self.timerinicio = math.trunc(
            round(pg.time.get_ticks() / 1000, 0))
        self.timerpantalla = 0
        self.transparencia = 0

    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        salir = False
        self.mododemo = True
        instrucciones = False
        self.aumentartransparencia = False
        self.disminuirtransparencia = False
        porcentajepantallaprincipal = 0.75
        width_rect_botoninstrucciones = 450
        height_rect_botoninstrucciones = 50
        self.rect_botoninstrucciones = pg.Rect(((ANCHO-width_rect_botoninstrucciones)/DOS),
                                               ((ALTO-(height_rect_botoninstrucciones*1.5))), width_rect_botoninstrucciones, height_rect_botoninstrucciones)
        width_rect_instrucciones = ANCHO * porcentajepantallaprincipal
        height_rect_instrucciones = ALTO * porcentajepantallaprincipal
        self.rect_instrucciones = pg.Rect(((ANCHO-width_rect_instrucciones)/DOS),
                                          ((ALTO-height_rect_instrucciones)/DOS), width_rect_instrucciones, height_rect_instrucciones)
        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    self.nextwindows = ''
                    return True, self.nextwindows
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE and not instrucciones:
                    self.nextwindows = 'EmpezarPartida'
                    salir = True
            self.pantalla.blit(self.fondo, POSICION0)
            self.jugador.update(self.colision, self.partida,
                                self.aterrizar, self.mododemo)
            self.pantalla.blit(self.jugador.image, self.jugador.rect)
            self.asteroidesdemo()
            self.botonintrucciones()

            x_raton, y_raton = pg.mouse.get_pos()
            if self.rect_botoninstrucciones.collidepoint((x_raton, y_raton)):
                self.timernextwindows.reset()
                self.instrucciones()
                instrucciones = True

            else:
                instrucciones = False
                # Cambio a pantalla records en x segundos
                if self.timernextwindows.counter():
                    self.nextwindows = 'Records'
                    salir = True
                self.pintar_mensaje(
                    "Pulsa <ESPACIO> para empezar la partida")
                self.titulo()
                self.mostrarhistoria()
            pg.display.flip()  # Mostramos los cambios
        return False, self.nextwindows

    def titulo(self):
        tamañofuente = 120
        self.tipo = pg.font.Font(RUTAFUENTESENCABEZADOS, tamañofuente)
        mensaje = "THE QUEST"
        texto = self.tipo.render(mensaje, True, COLORFUENTE)
        pos_x = (ANCHO-texto.get_width())/DOS
        pos_y = texto.get_height()/DOS
        self.pantalla.blit(texto, (pos_x, pos_y))

    def botonintrucciones(self):
        grosorborde = 2
        tamañofuente = 45
        fuente = pg.font.Font(RUTAFUENTESENCABEZADOS, tamañofuente)
        mensaje = 'INSTRUCCIONES'
        color = pg.Color('white')
        pg.draw.rect(self.pantalla, pg.Color(
            'red'), self.rect_botoninstrucciones, grosorborde)
        text_surface = fuente.render(
            mensaje, True, color)
        self.pantalla.blit(
            text_surface, (self.rect_botoninstrucciones.centerx-(text_surface.get_width()/DOS), self.rect_botoninstrucciones.centery-(text_surface.get_height()/DOS)))

    def asteroidesdemo(self):
        self.timerpantalla = math.trunc(
            round(pg.time.get_ticks() / 1000, 0))
        crearasteroride = False
        self.asteroides.draw(self.pantalla)
        if (self.timerinicio+1) == self.timerpantalla:
            self.timerinicio = self.timerpantalla
            self.textoprogresivo = True
            crearasteroride = True
        grupoAsteroides = pg.sprite.Group.sprites(self.asteroides)
        for asteroide in grupoAsteroides:
            asteroide.update()
        if crearasteroride:
            velocidadobjetos = [10, 20]
            tipoAsteroides = [Asteroide.CAZA,
                              Asteroide.ASTEROIDE1, Asteroide.ASTEROIDE2]
            tipo = random.randint(0, 2)
            velocidad = random.randint(
                velocidadobjetos[0], velocidadobjetos[1])
            asteroide = Asteroide(
                PUNTOSNAVE[tipo], tipoAsteroides[tipo], velocidad)
            asteroide.rect.x = ANCHO + asteroide.rect.height
            asteroide.rect.y = random.randint(ALTO/4, ALTO-(ALTO/2.5))
            self.asteroides.add(asteroide)

    def mostrarhistoria(self):
        tamañofuente = 30
        self.tipo = pg.font.Font(RUTAFUENTESENCABEZADOS, tamañofuente)
        altotexto = self.tipo.get_height()
        mensaje = GAMEHISTORY
        pos_y = (ALTO - (len(mensaje)*altotexto)*DOS)/DOS
        for cadena in mensaje:
            texto = self.tipo.render(cadena, True, color=('white'))
            texto.set_alpha(self.transparencia)
            pos_x = (ANCHO-texto.get_width())/DOS
            self.pantalla.blit(texto, (pos_x, pos_y))
            pos_y += texto.get_height()*DOS

        if self.transparencia <= 0:
            self.disminuirtransparencia = False
            self.aumentartransparencia = True

        if self.transparencia >= 200:
            self.aumentartransparencia = False
            self.disminuirtransparencia = True

        if self.disminuirtransparencia:
            self.transparencia -= 1
        if self.aumentartransparencia:
            self.transparencia += 1

    def instrucciones(self):
        grosorborde = 3
        tamañoencabezado = 45
        fuente = pg.font.Font(RUTAFUENTESENCABEZADOS, tamañoencabezado)
        mensaje = '¿CÒMO JUGAR?'
        pg.draw.rect(self.pantalla, pg.Color(
            'red'), self.rect_instrucciones, grosorborde)
        text_surface = fuente.render(
            mensaje, True, color=pg.Color('white'))
        self.pantalla.blit(
            text_surface, (self.rect_instrucciones.centerx-(text_surface.get_width()/DOS),
                           self.rect_instrucciones.top))
        #########
        tamañoencabezado = 24
        fuente = pg.font.Font(RUTAFUENTESENCABEZADOS, tamañoencabezado)
        pg.draw.rect(self.pantalla, pg.Color(
            'red'), self.rect_instrucciones, grosorborde)
        pos_y = self.rect_instrucciones.top + text_surface.get_height()
        for mensaje in INSTRUCCIONES:
            text_surface = fuente.render(
                mensaje, True, COLORFUENTE)
            self.pantalla.blit(
                text_surface, (self.rect_instrucciones.left + grosorborde,
                               pos_y))
            pos_y += text_surface.get_height()*2
