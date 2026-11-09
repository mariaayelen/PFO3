"""Cliente de consola para consultar animales de Misiones."""
import json
import socket

HOST = "127.0.0.1"
PUERTO = 6000


def consultar(accion, animal=""):
    pedido = {"accion": accion, "animal": animal}
    try:
        with socket.create_connection((HOST, PUERTO), timeout=5) as conexion:
            conexion.settimeout(12)
            conexion.sendall((json.dumps(pedido, ensure_ascii=False) + "\n").encode("utf-8"))
            with conexion.makefile("r", encoding="utf-8") as entrada:
                linea = entrada.readline(4096)
                if not linea:
                    print("No llegó ninguna respuesta.")
                    return None
                return json.loads(linea)
    except (OSError, ValueError) as error:
        print("No se pudo conectar. Revisá que estén abiertos el servidor y los workers.")
        return None


def mostrar_respuesta(respuesta, accion):
    if not respuesta:
        return
    if not respuesta.get("ok"):
        print(respuesta.get("mensaje", "Ocurrió un problema."))
        return
    datos = respuesta["resultado"]
    print("\n--- RESULTADO ---")
    if accion == "listar":
        for nombre in datos:
            print("-", nombre)
    elif accion == "ficha":
        print("Animal:", datos["nombre"])
        print("Grupo:", datos["grupo"])
        print("Ambiente:", datos["ambiente"])
        print("Alimentación:", datos["alimentacion"])
        print("Dato para aprender:", datos["dato"])
    elif accion == "pregunta":
        print("Animal:", datos["animal"])
        print("Pregunta para conversar en clase:", datos["pregunta"])
    print("Respondió el worker", respuesta["worker"])


def iniciar_cliente():
    while True:
        print("\n=== EXPLORADORES DE LA FAUNA DE MISIONES ===")
        print("1. Ver los animales del diccionario")
        print("2. Buscar la ficha de un animal")
        print("3. Obtener una pregunta de repaso")
        print("0. Salir")
        opcion = input("Elegí una opción: ").strip()
        if opcion == "0":
            print("¡Hasta la próxima!")
            break
        if opcion == "1":
            mostrar_respuesta(consultar("listar"), "listar")
        elif opcion in ("2", "3"):
            nombre = input("Escribí el nombre del animal: ").strip()
            if not nombre:
                print("Primero escribí un nombre.")
                continue
            accion = "ficha" if opcion == "2" else "pregunta"
            mostrar_respuesta(consultar(accion, nombre), accion)
        else:
            print("Esa opción no existe.")


if __name__ == "__main__":
    iniciar_cliente()
