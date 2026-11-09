
const animales = document.getElementById('animales');
const resultado = document.getElementById('resultado');

// Fotos guardadas en la carpeta static/imagenes
const fotos = {
  'corzuela': 'corzuela.jfif',
  'yarara': 'yarara.jpg',
  'oso-hormiguero': 'oso-hormiguero.jpg',
  'carpincho': 'carpincho.jpg',
  'mono': 'mono.png',
  'tucan': 'tucan.jpeg',
  'coati': 'coati.jpg',
  'tapir': 'tapir.jpg',
  'yaguarete': 'yaguarete.jpg',
  'lobito': 'lobito.jfif'
};


function nombreArchivo(nombre) {
  let animal = nombre.toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim();

  if (animal.includes('tapir')) return 'tapir';
  if (animal.includes('mono')) return 'mono';
  if (animal.includes('yaguarete')) return 'yaguarete';
  if (animal.includes('coati')) return 'coati';
  if (animal.includes('tucan')) return 'tucan';
  if (animal.includes('lobito')) return 'lobito';

  return animal.replace(/\s+/g, '-');
}


function obtenerFoto(nombre) {
  const archivo = fotos[nombreArchivo(nombre)];
  return archivo ? `/static/imagenes/${archivo}` : '';
}

async function consultar(accion, animal = '') {
  try {
    const ruta = `/consulta?accion=${encodeURIComponent(accion)}&animal=${encodeURIComponent(animal)}`;
    const respuesta = await fetch(ruta);
    return await respuesta.json();
  } catch (error) {
    return {ok: false, mensaje: 'No se pudo realizar la consulta.'};
  }
}

function mostrarError(mensaje) {
  resultado.hidden = false;
  resultado.replaceChildren();

  const texto = document.createElement('p');
  texto.className = 'error';
  texto.textContent = mensaje;
  resultado.append(texto);
}

function linea(etiqueta, valor) {
  const p = document.createElement('p');
  const b = document.createElement('strong');
  b.textContent = etiqueta + ': ';
  p.append(b, document.createTextNode(valor));
  return p;
}

async function verFicha(nombre) {
  resultado.hidden = false;
  resultado.replaceChildren();
  resultado.textContent = 'Buscando la ficha...';

  const respuesta = await consultar('ficha', nombre);

  if (!respuesta.ok) {
    mostrarError(respuesta.mensaje);
    return;
  }

  const ficha = respuesta.resultado;
  resultado.replaceChildren();

  const titulo = document.createElement('h2');
  titulo.textContent = ficha.nombre;

  const foto = document.createElement('img');
  foto.src = obtenerFoto(nombre);
  foto.alt = ficha.nombre;
  foto.className = 'foto-ficha';
  foto.hidden = !foto.src;

  const dato = document.createElement('p');
  dato.className = 'dato';
  dato.textContent = ficha.dato;

  const boton = document.createElement('button');
  boton.className = 'boton';
  boton.textContent = 'Ver pregunta para repasar';

  const pregunta = document.createElement('div');

  boton.addEventListener('click', async () => {
    pregunta.className = 'pregunta';
    pregunta.textContent = 'Buscando una pregunta...';

    const r = await consultar('pregunta', nombre);
    pregunta.textContent = r.ok ? r.resultado.pregunta : r.mensaje;
  });

  const trabajador = document.createElement('p');
  trabajador.className = 'worker';
  trabajador.textContent = `Respondió el worker ${respuesta.worker}`;

  resultado.append(
    titulo,
    foto,
    linea('Grupo', ficha.grupo),
    linea('Ambiente', ficha.ambiente),
    linea('Alimentación', ficha.alimentacion),
    dato,
    boton,
    pregunta,
    trabajador
  );

  resultado.scrollIntoView({behavior: 'smooth', block: 'start'});
}

async function iniciar() {
  const respuesta = await consultar('listar');
  animales.replaceChildren();

  if (!respuesta.ok) {
    const p = document.createElement('p');
    p.className = 'error';
    p.textContent = respuesta.mensaje;
    animales.append(p);
    return;
  }

  respuesta.resultado.forEach((nombre) => {
    const boton = document.createElement('button');
    boton.className = 'tarjeta';

    const foto = document.createElement('img');
    foto.src = obtenerFoto(nombre);
    foto.alt = nombre;
    foto.className = 'foto-animal';
    foto.hidden = !obtenerFoto(nombre);

    const texto = document.createElement('span');
    texto.className = 'nombre';
    texto.textContent = nombre;

    const subtitulo = document.createElement('span');
    subtitulo.className = 'subtitulo';
    subtitulo.textContent = 'Ver ficha del animal';

    boton.append(foto, texto, subtitulo);
    boton.addEventListener('click', () => verFicha(nombre));

    animales.append(boton);
  });
}

iniciar();
