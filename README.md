# The_Quest_Diego_Andrades
Desarrollo proyecto final.

## Funciones del juego

Gestión de pantallas
```
1.- Cuando empieza el juego aparece en la pantalla principal ejecutando el juego en modo demo. Si no hacemos clic en instrucciones o en la tecla espacio para comenzar la partida irá cambiando entre la pantalla principal y la pantalla de récords cada 8 segundos(configurados con una variable desde .init)
2.-La ventana instrucciones aparece cuando marcamos con el ratón sobre el botón. Hasta que no desmarquemos el botón instrucciones no podremos iniciar la partida.
3.-La base de datos se creará con valores predeterminados la primera vez que accedamos la pantalla Récords.
4.-Si acabamos el juego y hemos conseguido un récord o nos quedamos sin vidas, pero aun así lo hemos conseguido nos mostrará una ventana para introducir nuestras iniciales y memorizar el récord. No dejará seguir si no se meten 3 caracteres.
5.-Si se accede a la pantalla récords viniendo de la pantalla de partida ya sea porque nos hemos quedado sin vidas o se ha conseguido pasar el juego, se nos habilitará un mensaje para reiniciar el juego desde dicha pantalla pulsando la tecla <<INTRO>>. Si
en 8 segundos no se inicia volveremos a la pantallaprincipal y deshabilito el acceso a partida desde récords.

```

¿Cómo funciona el juego?

```
1.-Si dejamos pulsada la flecha arriba o abajo la velocidad de movimiento incrementa
2.-Hay 3 niveles(Se pueden configurar más desde el init). En cada nivel se aumenta la velocidad del objeto y el nº de objetos que se crean por segundo.
3.-El tiempo del nivel siguiente se incrementa  con respecto al anterior con un multiplicador configurado en el .init.
4.-El tiempo se muestra en la pantalla de la partida en forma de cuenta atrás. Si queda
10 segundos el color cambia a ROJO para que el jugador sepa que el nivel está acabando.
5.-Si un objeto colisiona con la nave no suma puntos y esta explosionará. Cuando la nave aterriza en un planeta suma puntos extras de forma aleatoria.

```

## Cómo crear un entorno virtual

Supongamos que queremos crear un entorno virtual con el
nombre _env_.

```
python -m venv env

# En mac/linux si usáis python 3
python3 -m venv env
```

## Cómo activar el entorno virtual

```
# en Windows
.\env\Scripts\activate

# en Mac/Linux
source env/bin/activate
```

## Gestor de paquetes: pip

- Instalar un paquete nuevo: `pip install <nombre-del-paquete>`
- Ver los paquetes instalados (en el entorno): `pip freeze`
- Las dependencias necesarias para usar el juego están en el archivo `requirements.txt`
  que se pueden instalar con el comando `pip install -r requirements.txt` desde
  el directorio raíz del proyecto.

## Desactivar el entorno virtual

```
# Con el entorno virtual activo

deactivate
```

