# The_Quest_Diego_Andrades
Desarrollo proyecto final.

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

