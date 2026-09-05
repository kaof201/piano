"""
songs.py - Canciones integradas para practicar con el piano de escritorio
==========================================================================
Este archivo está separado de main.py a propósito: para agregar una
canción nueva en el futuro, solo hay que añadir una entrada más a la
lista SONGS de aquí abajo. main.py no necesita cambiar.

Formato de cada canción:
    ("Nombre visible", [(nota, duracion), (nota, duracion), ...])

- "nota": nombre de la nota, igual a como las nombra main.py.
- "duracion": número relativo (1 = negra, 0.5 = corchea, 2 = blanca, etc).

DURACIÓN REAL EN SEGUNDOS: el modo práctica sostiene cada nota por
duracion * (60 / BPM) segundos. Con el BPM por defecto (100), una nota de
duración 1 dura 0.6s. Puedes calcular cuánto dura una canción completa
sumando todas las duraciones y multiplicando por (60 / BPM).

Todas las piezas de abajo son de dominio público. Cada una se define UNA
vez como su tema/frase principal (MELODIA_X) y luego se repite varias
veces con repetir(...) para que la sesión de práctica dure más — igual
que en una interpretación real, donde estos temas se repiten (los
minuetos y el Canon de Pachelbel literalmente están construidos así).
Si quieres que dure más o menos, solo cambia el número de repeticiones,
o ajusta el BPM con +/- mientras tocas.
"""


def repetir(notas, veces):
    """Repite una lista de (nota, duracion) 'veces' veces seguidas."""
    return notas * veces


# ------------------------------------------------------------------
# Para Elisa (Beethoven) - tema principal, ~21 tiempos por vuelta
# ------------------------------------------------------------------
MELODIA_PARA_ELISA = [
    ("E4", 0.5), ("Ds4", 0.5), ("E4", 0.5), ("Ds4", 0.5), ("E4", 0.5),
    ("B3", 0.5), ("D4", 0.5), ("C4", 0.5), ("A3", 1),
    ("C3", 0.5), ("E3", 0.5), ("A3", 0.5), ("B3", 1),
    ("E3", 0.5), ("Gs3", 0.5), ("B3", 0.5), ("C4", 1),
    ("E4", 0.5), ("Ds4", 0.5), ("E4", 0.5), ("Ds4", 0.5), ("E4", 0.5),
    ("B3", 0.5), ("D4", 0.5), ("C4", 0.5), ("A3", 1),
    ("C3", 0.5), ("E3", 0.5), ("A3", 0.5), ("B3", 1),
    ("D4", 0.5), ("C4", 0.5), ("B3", 0.5), ("A3", 2),
]

# ------------------------------------------------------------------
# Himno a la Alegría (Beethoven, 9na Sinfonía) - tema con puente, ~64 tiempos
# ------------------------------------------------------------------
MELODIA_HIMNO_ALEGRIA = [
    ("E4", 1), ("E4", 1), ("F4", 1), ("G4", 1),
    ("G4", 1), ("F4", 1), ("E4", 1), ("D4", 1),
    ("C4", 1), ("C4", 1), ("D4", 1), ("E4", 1),
    ("E4", 1.5), ("D4", 0.5), ("D4", 2),
    ("E4", 1), ("E4", 1), ("F4", 1), ("G4", 1),
    ("G4", 1), ("F4", 1), ("E4", 1), ("D4", 1),
    ("C4", 1), ("C4", 1), ("D4", 1), ("E4", 1),
    ("D4", 1), ("C4", 1), ("C4", 2),
    ("D4", 1), ("D4", 1), ("E4", 1), ("C4", 1),
    ("D4", 1), ("E4", 0.5), ("F4", 0.5), ("E4", 1), ("C4", 1),
    ("D4", 1), ("E4", 0.5), ("F4", 0.5), ("E4", 1), ("D4", 1),
    ("C4", 1), ("D4", 1), ("G3", 2),
    ("E4", 1), ("E4", 1), ("F4", 1), ("G4", 1),
    ("G4", 1), ("F4", 1), ("E4", 1), ("D4", 1),
    ("C4", 1), ("C4", 1), ("D4", 1), ("E4", 1),
    ("D4", 1), ("C4", 1), ("C4", 2),
]

# ------------------------------------------------------------------
# Minueto en Sol (Bach/Petzold) - partes A y B, ~46 tiempos
# ------------------------------------------------------------------
MELODIA_MINUETO_SOL = [
    ("D4", 1), ("G3", 1), ("A3", 1), ("B3", 1),
    ("C4", 1), ("D4", 2), ("G3", 1),
    ("G3", 1), ("Fs3", 1), ("G3", 1), ("A3", 1),
    ("B3", 2), ("B3", 1),
    ("C4", 1), ("B3", 1), ("A3", 1), ("G3", 1),
    ("Fs3", 1), ("G3", 2), ("D3", 1),
    ("G3", 1), ("A3", 1), ("B3", 1), ("C4", 1),
    ("D4", 2), ("D4", 1),
    ("G4", 1), ("Fs4", 1), ("G4", 1), ("D4", 1),
    ("G4", 1), ("Fs4", 1), ("G4", 1), ("B3", 1),
    ("C4", 1), ("B3", 1), ("A3", 1), ("G3", 1),
    ("Fs3", 1), ("G3", 2), ("G3", 1),
]

# ------------------------------------------------------------------
# Canon en Re (Pachelbel) - el famoso bajo ostinato de 8 notas.
# En la pieza real este patrón se repite unas 28 veces a lo largo de
# ~5 minutos; aquí lo repetimos 20 veces (~1.6 min a 100 BPM).
# ------------------------------------------------------------------
OSTINATO_CANON_RE = [
    ("D4", 1), ("A3", 1), ("B3", 1), ("Fs3", 1),
    ("G3", 1), ("D3", 1), ("G3", 1), ("A3", 1),
]

# ------------------------------------------------------------------
# Amazing Grace (himno tradicional) - estrofa completa, ~31 tiempos
# ------------------------------------------------------------------
MELODIA_AMAZING_GRACE = [
    ("G3", 1), ("C4", 1), ("C4", 0.5), ("E4", 0.5), ("D4", 1), ("C4", 1),
    ("A3", 1), ("G3", 2),
    ("G3", 1), ("C4", 1), ("C4", 0.5), ("E4", 0.5), ("D4", 1), ("C4", 1),
    ("A3", 1), ("G3", 2),
    ("G3", 1), ("C4", 1), ("E4", 1), ("G4", 1), ("Fs4", 1),
    ("E4", 1), ("D4", 2),
    ("C4", 1), ("E4", 1), ("D4", 1), ("C4", 1),
    ("A3", 1), ("G3", 2),
]

# ------------------------------------------------------------------
# Greensleeves (tradicional inglesa) - sección A completa, ~28 tiempos
# ------------------------------------------------------------------
MELODIA_GREENSLEEVES = [
    ("A3", 1), ("C4", 1), ("D4", 1), ("E4", 1),
    ("F4", 1), ("E4", 1), ("D4", 1), ("B3", 1),
    ("C4", 1), ("B3", 1), ("A3", 1), ("A3", 1),
    ("E3", 1), ("Gs3", 0.5), ("A3", 0.5), ("A3", 1),
    ("A3", 1), ("C4", 1), ("D4", 1), ("E4", 1),
    ("F4", 1), ("E4", 1), ("D4", 1), ("B3", 1),
    ("C4", 1), ("A3", 1), ("Gs3", 1), ("A3", 2),
]


SONGS = [
    # nombre, notas repetidas -> duración aprox. a 100 BPM
    ("Para Elisa (Beethoven)", repetir(MELODIA_PARA_ELISA, 7)),          # ~1.5 min
    ("Himno a la Alegría (Beethoven)", repetir(MELODIA_HIMNO_ALEGRIA, 3)),  # ~1.9 min
    ("Minueto en Sol (Bach/Petzold)", repetir(MELODIA_MINUETO_SOL, 4)),  # ~1.8 min
    ("Canon en Re (Pachelbel)", repetir(OSTINATO_CANON_RE, 20)),         # ~1.6 min
    ("Amazing Grace (himno tradicional)", repetir(MELODIA_AMAZING_GRACE, 5)),  # ~1.5 min
    ("Greensleeves (tradicional inglesa)", repetir(MELODIA_GREENSLEEVES, 6)),  # ~1.7 min
]