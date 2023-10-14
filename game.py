import pygame


class TheQuest:
    def __init__(self):
        pygame.init()
        # Defino las dimensiones de la pantalla.
        pygame.display.set_mode((900, 700))

    def jugar(self):
        # Creamos el bucle principal del juego
        salir = False
        while not salir:
            for evento in pygame.event.get():  # Capturo el evento cerrar para cerrar el juego
                if pygame.QUIT == evento.type:
                    salir = True

        pygame.quit()  # Cerramos pygame


if __name__ == '__main__':
    juego = TheQuest()
    juego.jugar()
