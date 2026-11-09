"""Servidor principal: recibe consultas y las reparte entre dos workers por socket."""
import json
import logging
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

HOST = "127.0.0.1"
PUERTO = 6000
WORKERS = [("127.0.0.1", 6101), ("127.0.0.1", 6102)]
contador = 0
candado = threading.Lock()

logging.basicConfig(filename="actividad_servidor.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s", encoding="utf-8")


def enviar_a_worker(pedido):
    global contador
    with candado:
        elegido = contador % len(WORKERS)
        contador += 1
    # Si un worker está apagado, intentamos con el otro.
    for intento in range(len(WORKERS)):
        posicion = (elegido + intento) % len(WORKERS)
        host, puerto = WORKERS[posicion]
        try:
            with socket.create_connection((host, puerto), timeout=4) as conexion:
                conexion.settimeout(8)
                conexion.sendall((json.dumps(pedido, ensure_ascii=False) + "\n").encode("utf-8"))
                with conexion.makefile("r", encoding="utf-8") as entrada:
                    linea = entrada.readline(4096)
                    if not linea:
                        raise OSError("No llegó una respuesta")
                    respuesta = json.loads(linea)
                print(f"Consulta enviada al worker {posicion + 1}")
                logging.info("Consulta %s atendida por worker %s", pedido.get("accion"), posicion + 1)
                return respuesta
        except (OSError, ValueError) as error:
            print(f"Worker {posicion + 1} no respondió: {error}")
    logging.warning("No hay workers disponibles")
    return {"ok": False, "mensaje": "Los workers no están disponibles."}


def atender_cliente(conexion, direccion):
    print(f"Cliente conectado: {direccion[0]}")
    try:
        conexion.settimeout(15)
        with conexion, conexion.makefile("r", encoding="utf-8") as entrada:
            linea = entrada.readline(4096)
            pedido = json.loads(linea)
            if (not isinstance(pedido, dict) or
                pedido.get("accion") not in ("listar", "ficha", "pregunta") or
                not isinstance(pedido.get("animal", ""), str) or
                len(pedido.get("animal", "")) > 80):
                respuesta = {"ok": False, "mensaje": "Pedido no válido."}
            else:
                respuesta = enviar_a_worker(pedido)
            conexion.sendall((json.dumps(respuesta, ensure_ascii=False) + "\n").encode("utf-8"))
    except (OSError, ValueError, UnicodeError) as error:
        print(f"Problema con un cliente: {error}")


def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PUERTO))
        servidor.listen(10)
        print("=== SERVIDOR PRINCIPAL - FAUNA DE MISIONES ===")
        print(f"Escuchando en {HOST}:{PUERTO}")
        print("Repartiendo consultas entre workers 1 y 2")
        with ThreadPoolExecutor(max_workers=8) as hilos:
            while True:
                conexion, direccion = servidor.accept()
                hilos.submit(atender_cliente, conexion, direccion)


if __name__ == "__main__":
    try:
        iniciar_servidor()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    except OSError as error:
        print(f"No se pudo iniciar el servidor: {error}")
