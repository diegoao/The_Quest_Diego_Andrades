import pygame
temporizador = 60
visualizar = 0 + 3

while True:
    segundos = round(pygame.time.get_ticks() / 1000, 0)
    temporizador = 60
    temporizador -= segundos
    reloj = pygame.time.Clock()

    if (visualizar+3) == segundos:
        # print(f'tiempo{segundos}')
        visualizar = segundos

    reloj.tick(2)
   # print(temporizador)
    lista = [4]
    print(lista[-1])
