"""Página web del diccionario. Consulta al servidor principal usando sockets."""
import json
import socket
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
HOST = "127.0.0.1"
PUERTO = 6000


def pedir_al_servidor(accion, animal=""):
    pedido = {"accion": accion, "animal": animal}
    try:
        with socket.create_connection((HOST, PUERTO), timeout=4) as conexion:
            conexion.settimeout(10)
            conexion.sendall((json.dumps(pedido, ensure_ascii=False) + "\n").encode("utf-8"))
            with conexion.makefile("r", encoding="utf-8") as entrada:
                linea = entrada.readline(4096)
                if not linea:
                    return {"ok": False, "mensaje": "El servidor no devolvió una respuesta."}
                return json.loads(linea)
    except (OSError, ValueError):
        return {"ok": False, "mensaje": "No pude comunicarme con el servidor. Revisá que estén abiertos el servidor principal y los workers."}


@app.get("/")
def inicio():
    return render_template("inicio.html")


@app.get("/consulta")
def consulta():
    accion = request.args.get("accion", "")
    animal = request.args.get("animal", "")
    if accion not in ("listar", "ficha", "pregunta") or len(animal) > 80:
        return jsonify({"ok": False, "mensaje": "Esa consulta no es válida."}), 400
    respuesta = pedir_al_servidor(accion, animal)
    return jsonify(respuesta), (200 if respuesta.get("ok") else 503 if "comunicarme" in respuesta.get("mensaje", "") else 400)


if __name__ == "__main__":
    print("Página web: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
