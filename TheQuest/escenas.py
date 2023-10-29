import math
import os
import random
import pygame as pg
from . import ALTO, ANCHO, COLORFUENTE, FPS, GROSORMARGENES, NUMERONIVELES, RUTAFUENTESENCABEZADOS, PUNTOSATERRIZAJE, PUNTOSNAVE, TAMAÑOMARGENESPARTIDA
from .entidades import (
    Asteroide,
    Mensajes,
    NaveEspacial,
    Planeta,
    TemporizadorNivel
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
        self.inciarpartida = False

    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True, False
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    salir = True
            self.pantalla.blit(self.fondo, (0, 0))
            self.pintar_mensaje()
            pg.display.flip()  # Mostramos los cambios
        return False, True

    def pintar_mensaje(self):
        mensaje = "Pulsa <ESPACIO> para empezar la partida"
        texto = self.tipo.render(mensaje, True, (255, 215, 0))
        pos_x = (ANCHO-texto.get_width())/2
        pos_y = ALTO * 3/4
        self.pantalla.blit(texto, (pos_x, pos_y))

#####################################


class PantallaPartida(Escena):
    def __init__(self, pantalla, nivel, contadorvidas, marcador, tiemponivel, dificultad):
        super().__init__(pantalla)
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
        print('Has entrado en pantalla Partida del juego')
        super().ejecutar_bucle()
        salir = False
        self.crear_asteroide()
        self.tiempodesdeinciojuego = round(pg.time.get_ticks() / 1000, 0)
        creacion = self.tiemponivel
        self.colision = False
        self.planeta.crearplaneta()
        self.partida = True
        self.aterrizar = False
        print(f'has comenzado en el nivel: {self.nivel}')
        pg.mixer.music.load('Recursos/Sonidos/Niveles/nivel1.wav')
        pg.mixer.music.play()
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
            self.marcador.pintar(self.pantalla)
            self.pantalla.blit(self.jugador.image, self.jugador.rect)
            self.margenes()
            vidas = self.contador_vidas.vidas
            self.asteroides.draw(self.pantalla)
            self.contador_vidas.pintar(self.pantalla, vidas)
            self.Temporizador()
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

            self.textfinalnivel.pintar(self.pantalla, mensaje)
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
        velocidadobjetos = self.dificultad

        tipoAsteroides = [Asteroide.CAZA,
                          Asteroide.ASTEROIDE1, Asteroide.ASTEROIDE2]
        tipo = random.randint(0, 2)
        velocidad = random.randint(velocidadobjetos[0], velocidadobjetos[1])
        asteroide = Asteroide(
            PUNTOSNAVE[tipo], tipoAsteroides[tipo], velocidad)
        asteroide.rect.x = ANCHO + asteroide.rect.height
        asteroide.rect.y = random.randint(
            TAMAÑOMARGENESPARTIDA, ALTO-TAMAÑOMARGENESPARTIDA-asteroide.rect.width)
        self.asteroides.add(asteroide)


#####################################


class PantallaRecords(Escena):
    def __init__(self, pantalla, datos):
        super().__init__(pantalla)

    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        salir = False
        pg.mixer.music.load('Recursos/Sonidos/Niveles/records.wav')
        pg.mixer.music.play()
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
            self.pantalla.fill((0, 0, 255))
            pg.display.flip()  # Mostramos los cambios
        return True
