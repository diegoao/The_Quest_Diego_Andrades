import sqlite3
from datetime import date


class DBManager:

    def __init__(self, ruta):
        self.ruta = ruta

    def conectar(self):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        return conexion, cursor

    def desconectar(self, conexion):
        conexion.close()

    def consultaSQL(self, consulta):

        # 1. Conectar a la base de datos
        conexion = sqlite3.connect(self.ruta)

        # 2. Abrir cursor
        cursor = conexion.cursor()

        # 3. Ejecutar la consulta
        cursor.execute(consulta)

        # 4. Tratar los datos
        # 4.1 Obtener los datos
        datos = cursor.fetchall()

        # 4.2 Los guardo localmente
        self.registros = []
        nombres_columna = []
        for columna in cursor.description:
            nombres_columna.append(columna[0])

        for dato in datos:
            movimiento = {}
            indice = 0
            for nombre in nombres_columna:
                movimiento[nombre] = dato[indice]
                indice += 1
            self.registros.append(movimiento)

        # 5. Cerrar la conexión
        conexion.close()

        # 6. Devolver los resultados
        return self.registros

    def borrar(self, puntos):

        sql = 'delete from records where Puntos<?'
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        resultado = False
        try:
            cursor.execute(sql, (puntos,))
            conexion.commit()
            resultado = True
        except:
            conexion.rollback()

        conexion.close()
        return resultado

        conexion, cursor = self.conectar()

        resultado = False
        try:
            cursor.execute(consulta, params)
            conexion.commit()
            resultado = True
        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)
        return resultado

    def nuevo(self, consulta, parametros):
        conexion, cursor = self.conectar()
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        resultado = False
        try:
            cursor.execute(consulta, parametros)
            conexion.commit()
            resultado = True
        except:
            conexion.rollback()
            conexion.close()
        return resultado

    def creartabla(self):
        consulta = """CREATE TABLE "records" (
                "Nombre"	TEXT NOT NULL,
                "Puntos"	NUMERIC NOT NULL,
                "Nivel"	TEXT NOT NULL,
                "Fecha"	TEXT NOT NULL,
                "id"	INTEGER NOT NULL,
	            PRIMARY KEY("id" AUTOINCREMENT)
                );"""
        conexion, cursor = self.conectar()
        cursor.execute(consulta)
        conexion.commit()
        resultado = False
        try:
            cursor.execute(consulta)
            conexion.commit()
            resultado = True
        except:
            conexion.rollback()
            conexion.close()
        return resultado
