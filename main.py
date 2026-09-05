"""
Piano de escritorio - controlado con el teclado del computador
================================================================
Cubre 2 octavas completas (25 notas) visibles a la vez, dibujadas como
DOS teclados apilados: el de arriba es la octava alta, el de abajo es
la octava baja (igual que en el teclado fisico, donde la fila QWERTY
esta arriba de la fila ZXCV). Puedes desplazarte con las flechas
arriba/abajo por todo el rango de C1 a C5.

La app esta organizada en modulos, cada uno con una sola
responsabilidad (ver el encabezado de cada archivo para el detalle):

  config.py        tamanos, mapas de teclas, constantes
  theme.py         colores y fuentes
  music_theory.py  conversion nota <-> MIDI <-> frecuencia
  audio.py         sintesis y carga de sonidos
  visuals.py       degradados, sombras y brillos genericos
  background.py    fondo animado (degradado + particulas)
  piano_view.py    dibujo de las teclas
  menu_view.py     menu de seleccion de canciones (tarjetas)
  hud_view.py      cabecera, progreso e instrucciones
  game.py          estado + bucle principal
  songs.py         canciones integradas para practicar

Distribucion de teclas:

  Teclado de ARRIBA (octava alta):
    Blancas: Q W E R T Y U I
    Negras:      2 3   5 6 7

  Teclado de ABAJO (octava baja):
    Blancas: Z X C V B N M
    Negras:      S D   G H J

  Flecha ARRIBA / ABAJO: desplaza las 2 octavas hacia arriba/abajo (C1 a C5).
  F11: alternar pantalla completa.
  P: abrir/cerrar el menu de canciones (ver songs.py).
  + / - : subir o bajar el tempo (BPM) del modo practica.
  ESC: salir

Modo practica (tecla P):
  Se abre un menu con las canciones de songs.py, mostradas como
  tarjetas con su numero, cuantas notas tienen y cuanto duran aprox.
  Muevete con las flechas arriba/abajo y confirma con Enter, o pulsa
  directamente el numero de la cancion. Una vez elegida, el teclado te
  guia nota por nota:

  - La tecla que debes tocar AHORA se marca en VERDE.
  - La tecla que vas a tocar DESPUES (la siguiente) se marca en AZUL,
    para que puedas ir ubicandola mientras sostienes la actual.
  - Debes MANTENER presionada la tecla verde durante todo el tiempo
    indicado (segun la duracion de la nota y el tempo/BPM actual).
    El avance a la siguiente nota no ocurre hasta que se cumpla ese
    tiempo sosteniendo la tecla correcta; si la sueltas antes, tendras
    que volver a presionarla.
  - Si la siguiente nota de la cancion esta en otra octava, el
    programa CAMBIA LA OCTAVA AUTOMATICAMENTE por ti (de C1 a C5) al
    empezar la cancion y cada vez que avanzas de nota: no hace falta
    usar las flechas mientras practicas.

Sonido:
  - Si existe una carpeta "samples/" junto a este archivo con archivos
    .wav nombrados como la nota (ej: C3.wav, Cs3.wav, D3.wav... la 's'
    es sostenido/sharp), se usan esos samples reales.
  - Si falta el archivo de una nota, se genera un tono sintetizado
    con timbre de piano (armonicos + caida exponencial) automaticamente.
"""

from game import PianoApp


def main():
    PianoApp().run()


if __name__ == "__main__":
    main()
