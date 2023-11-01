import math
import os
import random
import datetime
import pygame as pg
from . import ALTO, ANCHO, COLORFUENTE, FPS, GROSORMARGENES, NUMERONIVELES, NUMERORECORS, RUTAFUENTESENCABEZADOS, PUNTOSATERRIZAJE, PUNTOSNAVE, TAMAÑOMARGENESPARTIDA
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
        self.nextwindows = ''

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
                    return True
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    self.nextwindows = 'EmpezarPartida'
                    salir = True
            self.pantalla.blit(self.fondo, (0, 0))
            self.pintar_mensaje()
            pg.display.flip()  # Mostramos los cambios
        return False, self.nextwindows

    def pintar_mensaje(self):
        mensaje = "Pulsa <ESPACIO> para empezar la partida"
        texto = self.tipo.render(mensaje, True, (255, 215, 0))
        pos_x = (ANCHO-texto.get_width())/2
        pos_y = ALTO * 3/4
        self.pantalla.blit(texto, (pos_x, pos_y))

#####################################


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
        pg.mixer.music.load('Recursos/Sonidos/Niveles/nivel.wav')
        # pg.mixer.music.play()
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

    def mostrarnivel(self):
        self.tipo_letra = pg.font.Font(RUTAFUENTESENCABEZADOS, 25)
        nivel = str(self.nivel)
        cadena = f'Jugando el nivel: {nivel}'
        texto = self.tipo_letra.render(cadena, True, COLORFUENTE)
        altotexto = texto.get_height()
        anchotexto = texto.get_width()
        pos_x = (ANCHO-anchotexto)/2
        pos_y = ALTO - (TAMAÑOMARGENESPARTIDA-GROSORMARGENES+altotexto)/2
        self.pantalla.blit(texto, (pos_x, pos_y))

#####################################


class PantallaRecords(Escena):
    def __init__(self, pantalla, marcador, nivel, datos):
        super().__init__(pantalla)
        self.nivel = nivel
        self.basedatos = datos
        self.marcador = marcador

    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        print('Has entrado en pantalla Records')
        salir = False
        self.mensajes = Mensajes()
        pedirinciales = False
        self.tipo_letra = pg.font.Font(RUTAFUENTESENCABEZADOS, 35)
        ruta = os.path.join('Recursos', 'imágenes',
                            'Fondos', 'FondoPartida.png')
        self.fondo = pg.transform.scale(pg.image.load(ruta), (ANCHO, ALTO))
        pg.mixer.music.load('Recursos/Sonidos/Niveles/records.wav')
        # pg.mixer.music.play()
        self.encabezado = []
        self.records = []
        self.connectandcreatetable()
        fechaActual = datetime.datetime.now().date()
        self.iniciales = ''
        mensaje = [f'Has conseguido un record, introducir 3 inciales',
                   'Pulsa <<ESPACIO>> para continuar']
        tamañofuente = 30
        sql = f'SELECT Puntos from records where Puntos > {self.marcador.valor}'
        records = self.basedatos.consultaSQL(sql)
        # Si el número de records mayores que el marcador es menor que numero máximo de records lo guardamos
        if len(records) < NUMERORECORS:
            pedirinciales = True
        else:
            self.records, self.encabezado = self.pedirrecords()
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
                if evento.type == pg.KEYDOWN and not evento.key == pg.K_SPACE and pedirinciales:
                    if evento.key == pg.K_BACKSPACE:
                        self.iniciales = self.iniciales[:-1]
                    else:
                        self.iniciales += evento.unicode
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE and pedirinciales and len(self.iniciales) == 3:
                    sql = 'INSERT INTO records (Nombre,Puntos, Nivel, Fecha) VALUES (?, ?, ?, ?)'
                    parametros = (self.iniciales, self.marcador.valor,
                                  self.nivel, fechaActual)
                    self.basedatos.nuevo(sql, parametros)
                    self.records, self.encabezado = self.pedirrecords()
                    self.eliminarrecords()
                    pedirinciales = False

            self.pantalla.blit(self.fondo, (0, 0))
            if pedirinciales:
                self.mensajes.pintar(self.pantalla, mensaje, tamañofuente)
                self.pediriniciales()
            else:
                self.mostrarrecords()
            pg.display.flip()  # Mostramos los cambios
        return True

    def pediriniciales(self):

        if len(self.iniciales) > 3:
            self.iniciales = self.iniciales[:3]
        fuente = pg.font.Font(RUTAFUENTESENCABEZADOS, 45)
        ancho_rectangulo = 120
        alto_rectangulo = 50
        input_rect = pg.Rect(((ANCHO-ancho_rectangulo)/2),
                             ((ALTO-alto_rectangulo)/1.5), ancho_rectangulo, alto_rectangulo)
        color = pg.Color('white')
        pg.draw.rect(self.pantalla, COLORFUENTE, input_rect, 2)
        text_surface = fuente.render(
            self.iniciales, True, color)
        self.pantalla.blit(
            text_surface, (input_rect.centerx-(text_surface.get_width()/2), input_rect.centery-(text_surface.get_height()/2)))

    def pedirrecords(self):
        # Pido los enunciado de las columnas y omito el id
        sql = 'SELECT name FROM PRAGMA_TABLE_INFO("records") WHERE NOT name = "id" '
        columnas = self.basedatos.consultaSQL(sql)
        # Pido los records ordenados en orden descendente
        sql = 'select Nombre,Puntos, Nivel, Fecha from records order by Puntos DESC LIMIT 5'
        records = self.basedatos.consultaSQL(sql)
        return records, columnas

    def eliminarrecords(self):
        puntos = self.records[-1]["Puntos"]
        self.basedatos.borrar(puntos)

    def mostrarrecords(self):
        pos_y = 100
        pos_x = ANCHO * 0.16
        for columna in self.encabezado:
            texto = self.tipo_letra.render(
                str(columna['name']), True, COLORFUENTE)
            self.pantalla.blit(texto, (pos_x, pos_y))
            pos_x += 200
        pos_y += 100
        for num in range(len(self.records)):
            pos_x = ANCHO * 0.16
            Nombre = self.records[num]["Nombre"]
            Puntuacion = self.records[num]["Puntos"]
            Nivel = self.records[num]["Nivel"]
            Fecha = self.records[num]["Fecha"]
            datos = [Nombre, Puntuacion, Nivel, Fecha]
            for data in datos:
                texto = self.tipo_letra.render(str(data), True, COLORFUENTE)
                self.pantalla.blit(texto, (pos_x, pos_y))
                pos_x += 200
            pos_y += 60

    def connectandcreatetable(self):
        self.basedatos.conectar()
        sql = 'SELECT Nombre, Puntos, Nivel, Fecha id FROM records'
        try:
            # Leo datos al inciar el juego para mostrar records
            self.basedatos.consultaSQL(sql)
        except:
            # Si hay error es porque no existe la tabla y la creo con el numero de records en blanco
            self.basedatos.creartabla()
            sql = 'INSERT INTO records (Nombre,Puntos, Nivel, Fecha) VALUES (?, ?, ?, ?)'
            parametros = ('---', '0', '0', 'xx-xx-xxxx')
            for i in range(NUMERORECORS):
                self.basedatos.nuevo(sql, parametros)
