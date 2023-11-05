# Estándar
import math
import os
import random
# Librerias de terceros
import pygame as pg
# Mis importaciones
from TheQuest import ALTO, ANCHO, COLORFUENTE, DOS, FPS, GROSORMARGENES, NUMERONIVELES, PUNTOSATERRIZAJE, PUNTOSNAVE, RUTAFUENTESENCABEZADOS, TAMAÑOFUENTEMARCADORES, TAMAÑOMARGENESPARTIDA
from TheQuest.entidades import (
    Asteroide,
    Mensajes,
    NaveEspacial,
    Planeta,
    TemporizadorNivel
)
from TheQuest.Escenas.Escena import Escena


class PantallaPartida(Escena):
    def __init__(self, pantalla, nivel, contadorvidas, marcador, tiemponivel, dificultad, db):
        super().__init__(pantalla)
        self.basededatos = db
        self.nivel = nivel
        self.tiemponivel = tiemponivel
        self.dificultad = dificultad
        self.jugador = NaveEspacial()
        ruta = os.path.join('Recursos', 'imágenes',
                            'Fondos', 'FondoPartida.png')
        self.fondo = pg.image.load(ruta).convert()
        self.contador_vidas = contadorvidas
        self.marcador = marcador
        self.asteroides = pg.sprite.Group()
        self.temporizador = TemporizadorNivel(self.tiemponivel)
        self.planeta = Planeta()
        self.colision = False
        self.textfinalnivel = Mensajes()
        self.esperacambionivel = False

    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        salir = False
        self.tiempodesdeinciojuego = round(pg.time.get_ticks() / 1000, 0)
        creacion = self.tiemponivel
        self.colision = False
        self.planeta.crearplaneta(self.nivel)
        self.partida = True
        self.aterrizar = False
        self.xfondo = 0
        self.yfondo = 0

        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE and self.esperacambionivel:
                    salir = True

            # Movimiento del fondo
            self.moverfondo()
            # self.pantalla.blit(self.fondo, (0, 0))
            self.jugador.update(self.colision, self.partida, self.aterrizar)
            self.pantalla.blit(self.jugador.image, self.jugador.rect)
            self.marcador.pintar(self.pantalla)
            self.margenes()
            vidas = self.contador_vidas.vidas
            self.asteroides.draw(self.pantalla)
            self.contador_vidas.pintar(self.pantalla, vidas)
            self.Temporizador()
            self.mostrarnivel()
            self.pantalla.blit(self.planeta.image, self.planeta.rect)
            # Creo,  actualizo la posición del Asteroide y cuento puntos
            if (creacion-1) == self.temporizador.valor:
                creacion = self.temporizador.valor
                self.crear_asteroide()
            grupoAsteroides = pg.sprite.Group.sprites(self.asteroides)
            for asteroide in grupoAsteroides:
                if asteroide.update():
                    self.marcador.aumentar(asteroide.puntos)

            # Detecto las colisiones y si surgen resto vidas hasta que me quedo sin ninguna y cierro el juego
            self.colisiones()

            # Pongo temporizador de 1 segundos para cuando me colisiona asteroide parar colision
            if self.colision:
                if self.tiempo_colision == self.temporizador.valor:
                    self.colision = False
            if self.contador_vidas.vidas <= 0:
                salir = True
            self.finalizarNivel()
            pg.display.flip()  # Mostramos los cambios
        return False

    def moverfondo(self):
        x_calculada = self.xfondo % self.fondo.get_rect().width
        self.pantalla.blit(
            self.fondo, (x_calculada - self.fondo.get_rect().width, self.yfondo))
        if x_calculada < ANCHO:
            self.pantalla.blit(self.fondo, (x_calculada, 0))
        self.xfondo -= 1

    def colisiones(self):
        memoriacolisiones = []
        if not self.colision and self.temporizador.valor > 0:
            memoriacolisiones = pg.sprite.spritecollide(
                self.jugador, self.asteroides, False)
        if len(memoriacolisiones) > 0:
            for i in memoriacolisiones:
                i.kill()
            if self.contador_vidas.vidas > 0 and not self.colision:
                self.contador_vidas.perder_vida()
            self.tiempo_colision = (self.temporizador.valor-1)
            self.colision = True

    def finalizarNivel(self):
        if self.temporizador.valor <= 0 and not self.esperacambionivel:
            self.partida = False
            self.planeta.update()
            self.aterrizar = True
        if self.jugador.rect.colliderect(self.planeta.rect):
            if self.aterrizar:
                self.marcador.aumentar(random.randint(
                    PUNTOSATERRIZAJE[0], PUNTOSATERRIZAJE[1]))
            self.aterrizar = False
            if self.nivel < NUMERONIVELES:
                mensaje = [f'Has terminado el nivel {self.nivel}',
                           'Pulsa <<ESPACIO>> para continuar']
            else:
                mensaje = [f'Felicitaciones has completado el juego',
                           'Pulsa <<ESPACIO>> para continuar']
            tamañofuente = 45
            self.textfinalnivel.pintar(
                self.pantalla, mensaje, tamañofuente, self.nivel)
            self.esperacambionivel = True

    def Temporizador(self):
        self.timerSeg = round(pg.time.get_ticks() / 1000, 0)
        self.temporizador.decrementar(math.trunc(
            self.timerSeg-self.tiempodesdeinciojuego))
        self.temporizador.pintar(self.pantalla)

    def margenes(self):
        pg.draw.line(self.pantalla, COLORFUENTE, (0,
                                                  TAMAÑOMARGENESPARTIDA), (ANCHO, TAMAÑOMARGENESPARTIDA), GROSORMARGENES)
        pg.draw.line(self.pantalla, COLORFUENTE,
                     (0, ALTO-TAMAÑOMARGENESPARTIDA), (ANCHO, ALTO-TAMAÑOMARGENESPARTIDA), GROSORMARGENES)

    def crear_asteroide(self):
        for nobjetos in range(self.nivel):
            velocidadobjetos = self.dificultad

            tipoAsteroides = [Asteroide.CAZA,
                              Asteroide.ASTEROIDE1, Asteroide.ASTEROIDE2]
            tipo = random.randint(0, DOS)
            velocidad = random.randint(
                velocidadobjetos[0], velocidadobjetos[1])
            asteroide = Asteroide(
                PUNTOSNAVE[tipo], tipoAsteroides[tipo], velocidad)
            asteroide.rect.x = ANCHO + asteroide.rect.height
            asteroide.rect.y = random.randint(
                TAMAÑOMARGENESPARTIDA, ALTO-TAMAÑOMARGENESPARTIDA-asteroide.rect.width)
            self.asteroides.add(asteroide)

    def mostrarnivel(self):
        self.tipo_letra = pg.font.Font(
            RUTAFUENTESENCABEZADOS, TAMAÑOFUENTEMARCADORES)
        nivel = str(self.nivel)
        cadena = f'Jugando el nivel: {nivel}'
        texto = self.tipo_letra.render(cadena, True, COLORFUENTE)
        altotexto = texto.get_height()
        anchotexto = texto.get_width()
        pos_x = (ANCHO-anchotexto)/DOS
        pos_y = ALTO - (TAMAÑOMARGENESPARTIDA-GROSORMARGENES+altotexto)/DOS
        self.pantalla.blit(texto, (pos_x, pos_y))
