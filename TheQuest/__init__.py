import os
# Variables
ANCHO = 1200
ALTO = 700
FPS = 25
VIDASINICIALES = 3

RUTAFUENTESENCABEZADOS = os.path.join(
    'Recursos', 'Tipografía', 'SF Distant Galaxy.ttf')
COLORFUENTE = (255, 215, 0)
COLORWARNING = (220, 30, 0)
COLORRECORDS = (255, 99, 0)
TAMAÑOMARGENESPARTIDA = 40
GROSORMARGENES = 5

# configuración niveles

NUMERONIVELES = 2
TIEMPO1ERNIVEL = 10
TIEMPOSIGUIENTENIVEL = 1.5
# Velocidad incial objetos
VELOCIDADINICIALOBJETOS = [10, 15]
# Puntos que te da la nave  en el marcador entre estos dos valores al aterrizar
PUNTOSATERRIZAJE = [20, 100]

# Puntos Naves
PUNTOSNAVE = [9, 22, 16]

# Ruta base de datos
RUTABASEDEDATOS = os.path.join('TheQuest', 'Data', 'Records.db')
NUMERORECORS = 5


GAMEHISTORY = ['La búsqueda comienza en un planeta tierra',
               'moribundo por el cambio climático.',
               'Partiremos a la búsqueda de un planeta',
               'compatible con la vida humana para colonizarlo.']
