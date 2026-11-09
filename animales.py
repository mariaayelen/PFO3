"""Pequeño diccionario escolar sobre animales de Misiones."""

ANIMALES = {
    "yaguarete": {
        "nombre": "Yaguareté", "grupo": "Mamífero", "ambiente": "Selva",
        "alimentacion": "Carnívoro",
        "dato": "Es el felino más grande de América y necesita grandes áreas de monte para vivir.",
        "pregunta": "¿Qué come el yaguareté?", "respuesta": "carnivoro"
    },
    "tapir": {
        "nombre": "Tapir (anta)", "grupo": "Mamífero", "ambiente": "Selva",
        "alimentacion": "Herbívoro",
        "dato": "Es un mamífero grande que ayuda a dispersar semillas en el monte.",
        "pregunta": "¿Qué ayuda a dispersar el tapir?", "respuesta": "semillas"
    },
    "coati": {
        "nombre": "Coatí", "grupo": "Mamífero", "ambiente": "Selva",
        "alimentacion": "Omnívoro",
        "dato": "Tiene una cola larga y suele buscar alimento con su hocico alargado.",
        "pregunta": "¿El coatí es mamífero o ave?", "respuesta": "mamifero"
    },
    "tucan": {
        "nombre": "Tucán", "grupo": "Ave", "ambiente": "Selva",
        "alimentacion": "Principalmente frutos",
        "dato": "Su pico grande y colorido es una de sus características más conocidas.",
        "pregunta": "¿Qué parte del cuerpo del tucán es muy llamativa?", "respuesta": "pico"
    },
    "mono cai": {
        "nombre": "Mono caí", "grupo": "Mamífero", "ambiente": "Selva",
        "alimentacion": "Omnívoro",
        "dato": "Vive entre los árboles y utiliza sus manos para manipular alimentos.",
        "pregunta": "¿Dónde pasa mucho tiempo el mono caí?", "respuesta": "arboles"
    },
    "carpincho": {
        "nombre": "Carpincho", "grupo": "Mamífero", "ambiente": "Humedales",
        "alimentacion": "Herbívoro",
        "dato": "Es el roedor más grande del mundo y suele vivir cerca del agua.",
        "pregunta": "¿Cerca de qué suele vivir el carpincho?", "respuesta": "agua"
    },
    "oso hormiguero": {
        "nombre": "Oso hormiguero", "grupo": "Mamífero", "ambiente": "Pastizales y monte",
        "alimentacion": "Hormigas y termitas",
        "dato": "Su lengua larga le permite alimentarse de hormigas y termitas.",
        "pregunta": "¿Qué animales pequeños come el oso hormiguero?", "respuesta": "hormigas"
    },
    "yarara": {
        "nombre": "Yarará", "grupo": "Reptil", "ambiente": "Monte",
        "alimentacion": "Carnívoro",
        "dato": "Es una serpiente venenosa: si se la encuentra, hay que mantener distancia.",
        "pregunta": "¿A qué grupo pertenece la yarará?", "respuesta": "reptil"
    },
    "corzuela": {
        "nombre": "Corzuela", "grupo": "Mamífero", "ambiente": "Monte",
        "alimentacion": "Herbívoro",
        "dato": "Es un pequeño ciervo que puede moverse con agilidad entre la vegetación.",
        "pregunta": "¿Qué tipo de alimentación tiene la corzuela?", "respuesta": "herbivoro"
    },
    "lobito de rio": {
        "nombre": "Lobito de río", "grupo": "Mamífero", "ambiente": "Ríos y arroyos",
        "alimentacion": "Carnívoro",
        "dato": "Es un mamífero semiacuático que se desplaza bien en el agua.",
        "pregunta": "¿El lobito de río es un mamífero o un pez?", "respuesta": "mamifero"
    },
}


def normalizar(texto):
    import unicodedata
    texto = unicodedata.normalize("NFD", texto.lower().strip())
    return "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")


# Para buscar con y sin tildes (ejemplo: yaguareté, tucán).
ANIMALES = {normalizar(clave): valor for clave, valor in ANIMALES.items()}


def resolver(accion, animal=""):
    clave = normalizar(animal)
    if accion == "listar":
        return {"ok": True, "resultado": [dato["nombre"] for dato in ANIMALES.values()]}
    if clave not in ANIMALES:
        return {"ok": False, "mensaje": "No encontré ese animal. Probá con la opción de listar."}
    datos = ANIMALES[clave]
    if accion == "ficha":
        return {"ok": True, "resultado": {
            "nombre": datos["nombre"], "grupo": datos["grupo"],
            "ambiente": datos["ambiente"], "alimentacion": datos["alimentacion"],
            "dato": datos["dato"]}}
    if accion == "pregunta":
        return {"ok": True, "resultado": {"animal": datos["nombre"], "pregunta": datos["pregunta"]}}
    return {"ok": False, "mensaje": "Esa opción no existe."}
