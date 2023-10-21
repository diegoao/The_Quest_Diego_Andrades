import pygame
from pygame.locals import *
import sys

import os
# Pantalla
ANCHO, ALTO = 900, 700
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
FPS = 60
RELOJ = pygame.time.Clock()

# Fondo del juego
fondo = pygame.image.load(
    "Recursos/imágenes/Fondos/FondoPartida.png").convert()
x = 0
y = 0
PANTALLA.blit(fondo, (x, y))

# Bucle de juego.
while True:
    # Cerrar Juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Movimiento del fondo
    x_relativa = x % fondo.get_rect().width
    PANTALLA.blit(fondo, (x + fondo.get_rect().width, y))
    if x_relativa < ANCHO:
        PANTALLA.blit(fondo, (x_relativa, y))
    x += 1
    # Control de FPS
    RELOJ.tick(FPS)
    # Actualización de la ventana
    pygame.display.update()
