# mis importaciones

import pygame
import sys
import os
ruta = os.path.join(
    'Recursos', 'Tipografía', 'SF Distant Galaxy.ttf')
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([800, 800])
base_font = pygame.font.Font(ruta, 32)
user_text = ''
input_rect = pygame.Rect(200, 200, 140, 32)
color = pygame.Color('red')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not event.key == pygame.K_SPACE:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
        print(user_text)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, color, input_rect, 2)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect))
    pygame.display.flip()
    clock.tick(25)


# mostrar records
    #  pos_y = ALTO/4

    # for num in range(len(records)):
    #   Nombre = records[num]["Nombre"]
    #  Puntuacion = records[num]["Puntuación"]
    #  Nivel = records[num]["Nivel"]
    # Fecha = records[num]["Fecha"]

    # cadena = "{:<5} {:>12} {:>12} {:>12}".format(
    #   Nombre, Puntuacion, Nivel, Fecha)

    # texto = self.tipo_letra.render(cadena, True, COLORFUENTE)
    # self.alto = texto.get_height()
    # self.ancho = texto.get_width()
    # pos_x = (ANCHO-self.ancho)/2
    # self.pantalla.blit(texto, (pos_x, pos_y))
    # pos_y += self.alto * 3
