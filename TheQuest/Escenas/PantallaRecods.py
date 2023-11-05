import os
import datetime
import pygame as pg
from TheQuest import ALTO, ANCHO, COLORFUENTE, DOS, NUMERORECORS, POSICION0, RUTAFUENTESENCABEZADOS, WINDOWSTIME
from TheQuest.entidades import (
    Mensajes,
    Timerchangewindows
)
from TheQuest.Escenas.Escena import Escena


class Records(Escena):
    def __init__(self, pantalla, marcador, nivel, datos):
        super().__init__(pantalla)
        self.nivel = nivel
        self.basedatos = datos
        self.marcador = marcador
        self.nextwindows = ''
        self.numniniciales = 3

    def ejecutar_bucle(self):
        super().ejecutar_bucle()
        salir = False
        self.mensajes = Mensajes()
        pedirinciales = False
        tamañofuente = 35
        self.tipo_letra = pg.font.Font(RUTAFUENTESENCABEZADOS, tamañofuente)
        ruta = os.path.join('Recursos', 'imágenes',
                            'Fondos', 'FondoPartida.png')
        self.fondo = pg.transform.scale(pg.image.load(ruta), (ANCHO, ALTO))
        ####################################
        self.fondos = []
        for i in range(3):
            ruta_img = os.path.join(
                'Recursos', 'imágenes', 'Fondos', f'hiperespacio{i}.png')
            self.fondos.append(pg.transform.scale(
                pg.image.load(ruta_img), (ANCHO, ALTO)))
        self.cambioimagenes = 0
        self.cambio1seg = 0
        self.cambiosentidoimg = 0
        ########################
        self.encabezado = []
        self.records = []
        self.connectandcreatetable()
        fechaActual = str(datetime.datetime.now().date())
        partes = fechaActual.split("-")
        fechaActual = "-".join(reversed(partes))
        self.iniciales = ''
        mensaje = [f'Has conseguido un record, introducir 3 inciales',
                   'Pulsa <<ESPACIO>> para continuar']
        tamañofuente = 30
        # Consulto a la base de datos para ver si los puntos del jugador están entre los 5 primeros
        sql = f'SELECT Puntos from records where Puntos > {self.marcador.valor}'
        records = self.basedatos.consultaSQL(sql)
        # Si el número de records mayores que el marcador es menor que numero máximo de records lo guardamos
        if len(records) < NUMERORECORS and self.marcador.valor != 0:
            pedirinciales = True
        else:
            self.records, self.encabezado = self.pedirrecords()
            self.timernextwindows = Timerchangewindows(WINDOWSTIME)
        # bucle principal
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    self.nextwindows = ''
                    return True, self.nextwindows
                if evento.type == pg.KEYDOWN and not evento.key == pg.K_SPACE and pedirinciales:
                    if evento.key == pg.K_BACKSPACE:
                        self.iniciales = self.iniciales[:-1]
                    else:
                        self.iniciales += evento.unicode
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE and pedirinciales and len(self.iniciales) == self.numniniciales:
                    sql = 'INSERT INTO records (Nombre,Puntos, Nivel, Fecha) VALUES (?, ?, ?, ?)'
                    parametros = (self.iniciales, self.marcador.valor,
                                  self.nivel, fechaActual)
                    self.basedatos.nuevo(sql, parametros)
                    self.records, self.encabezado = self.pedirrecords()
                    self.eliminarrecords()
                    self.timernextwindows = Timerchangewindows(WINDOWSTIME)
                    pedirinciales = False
                if evento.type == pg.KEYDOWN and evento.key == pg.K_RETURN and not pedirinciales:
                    self.nextwindows = 'EmpezarPartida'
                    salir = True

            if pedirinciales:
                self.pantalla.blit(self.fondo, POSICION0)
                self.mensajes.pintar(self.pantalla, mensaje, tamañofuente)
                self.pediriniciales()
            else:
                self.hiperespacio()
                self.pantalla.blit(self.image, POSICION0)
                self.mostrarrecords()
                # Cambio a pantalla Inicial en 5 segundos
                if self.timernextwindows.counter():
                    self.nextwindows = 'PantallaInicio'
                    salir = True
                mensaje = 'PULSA <<INTRO>> PARA COMENZAR LA PARTIDA'
                self.pintar_mensaje(mensaje)
            pg.display.flip()  # Mostramos los cambios
        return False, self.nextwindows

    def hiperespacio(self):
        if self.cambioimagenes == 2:
            self.cambiosentidoimg = True
        if self.cambioimagenes == 0:
            self.cambiosentidoimg = False
        if self.timernextwindows.timer != self.cambio1seg:
            self.cambio1seg = self.timernextwindows.timer
            if self.cambiosentidoimg:
                self.cambioimagenes -= 1
            else:
                self.cambioimagenes += 1
        self.image = self.fondos[self.cambioimagenes]

    def pediriniciales(self):
        tamañofuente = 45
        if len(self.iniciales) > self.numniniciales:
            self.iniciales = self.iniciales[:self.numniniciales]
        fuente = pg.font.Font(RUTAFUENTESENCABEZADOS, tamañofuente)
        ancho_rectangulo = 120
        alto_rectangulo = 50
        input_rect = pg.Rect(((ANCHO-ancho_rectangulo)/DOS),
                             ((ALTO-alto_rectangulo)/1.5), ancho_rectangulo, alto_rectangulo)
        color = pg.Color('white')
        pg.draw.rect(self.pantalla, COLORFUENTE, input_rect, DOS)
        text_surface = fuente.render(
            self.iniciales, True, color)
        self.pantalla.blit(
            text_surface, (input_rect.centerx-(text_surface.get_width()/DOS), input_rect.centery-(text_surface.get_height()/DOS)))

    def pedirrecords(self):
        # Pido los enunciado de las columnas y omito el id
        sql = 'SELECT name FROM PRAGMA_TABLE_INFO("records") WHERE NOT name = "id" '
        columnas = self.basedatos.consultaSQL(sql)
        # Pido los records ordenados en orden descendente
        sql = f'select Nombre,Puntos, Nivel, Fecha from records order by Puntos DESC LIMIT {NUMERORECORS}'
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
