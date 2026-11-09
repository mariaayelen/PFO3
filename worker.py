"""Servidor trabajador: resuelve consultas del diccionario escolar."""
import argparse
import json
import socket
from concurrent.futures import ThreadPoolExecutor
from animales import resolver

HOST = "127.0.0.1"


def atender(conexion, direccion, numero):
    try:
        conexion.settimeout(10)
        with conexion, conexion.makefile("r", encoding="utf-8") as entrada:
            linea = entrada.readline(4096)
            pedido = json.loads(linea)
            accion = pedido.get("accion", "")
            animal = pedido.get("animal", "")
            if not isinstance(accion, str) or not isinstance(animal, str):
                respuesta = {"ok": False, "mensaje": "Datos incorrectos."}
            else:
                respuesta = resolver(accion, animal)
            respuesta["worker"] = numero
            conexion.sendall((json.dumps(respuesta, ensure_ascii=False) + "\n").encode("utf-8"))
            print(f"Worker {numero}: {accion} - {animal or 'todos'}")
    except (ValueError, OSError, UnicodeError) as error:
        print(f"Worker {numero}: problema al atender un pedido: {error}")


def iniciar(numero, puerto):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, puerto))
        servidor.listen(10)
        print(f"Worker {numero} escuchando en {HOST}:{puerto}")
        with ThreadPoolExecutor(max_workers=3) as hilos:
            while True:
                conexion, direccion = servidor.accept()
                hilos.submit(atender, conexion, direccion, numero)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor trabajador")
    parser.add_argument("--numero", type=int, required=True, choices=[1, 2])
    datos = parser.parse_args()
    try:
        iniciar(datos.numero, 6100 + datos.numero)
    except KeyboardInterrupt:
        print("\nWorker detenido.")
    except OSError as error:
        print(f"No se pudo iniciar el worker: {error}")
