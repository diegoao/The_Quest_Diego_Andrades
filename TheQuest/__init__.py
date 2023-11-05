import os
# Variables
ANCHO = 1200
ALTO = 700
FPS = 25
# Vidas inciales
VIDASINICIALES = 3

RUTAFUENTESENCABEZADOS = os.path.join(
    'Recursos', 'Tipografía', 'SF Distant Galaxy.ttf')
COLORFUENTE = (255, 215, 0)
COLORWARNING = (220, 30, 0)
COLORRECORDS = (255, 99, 0)
TAMAÑOMARGENESPARTIDA = 40
GROSORMARGENES = 5
TAMAÑOFUENTEMARCADORES = 25

# Configuración niveles

NUMERONIVELES = 3
TIEMPO1ERNIVEL = 12
TIEMPOSIGUIENTENIVEL = 1.3
INCREMENTODIFICULTAD = 10

# Velocidad incial objetos
VELOCIDADINICIALOBJETOS = [13, 15]

# Tiempo entre cambio de pantalla inicial y records
WINDOWSTIME = 8

# Puntos que te da la nave  en el marcador entre estos dos valores al aterrizar
PUNTOSATERRIZAJE = [20, 100]

# Puntos Naves
PUNTOSNAVE = [9, 22, 16]

# Ruta base de datos
RUTABASEDEDATOS = os.path.join('TheQuest', 'Data', 'Records.db')
# Configuramos el número de records a guardar/mostrar
NUMERORECORS = 5

# Para cuando divido entre 2
DOS = 2
POSICION0 = (0, 0)

GAMEHISTORY = ['La búsqueda comienza en un planeta tierra',
               'moribundo por el cambio climático.',
               'Partiremos a la búsqueda de un planeta',
               'compatible con la vida humana para colonizarlo.']

INSTRUCCIONES = ['1-Utilice la tecla espacio para moverte/confirmar entre',
                 'menús. Hay 3 niveles',
                 '2-Usando la flecha arriba y abajo del teclado podrás',
                 'mover la nave.',
                 '3-El jugador dispone de 3 vidas para completar el juego.',
                 '4-Evita colisionar con naves y asteroides, estos sumarán',
                 'puntos.',
                 '5-Cuando finalices un nivel, la nave aterrizará y te dará',
                 'puntos extra.',
                 '6-La dificultad y el tiempo irá incrementando en cada nivel.']
