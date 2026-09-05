
def repetir(notas, veces):
    """Repite una lista de (nota, duracion) 'veces' veces seguidas."""
    return notas * veces


# ------------------------------------------------------------------
# Para Elisa (Beethoven) - tema principal
# CORREGIDO: melodía completa subida 1 octava (ver nota arriba).
# ------------------------------------------------------------------
MELODIA_PARA_ELISA = [
    ("E5", 0.5), ("Ds5", 0.5), ("E5", 0.5), ("Ds5", 0.5), ("E5", 0.5),
    ("B4", 0.5), ("D5", 0.5), ("C5", 0.5), ("A4", 1),
    ("C4", 0.5), ("E4", 0.5), ("A4", 0.5), ("B4", 1),
    ("E4", 0.5), ("Gs4", 0.5), ("B4", 0.5), ("C5", 1),
    ("E5", 0.5), ("Ds5", 0.5), ("E5", 0.5), ("Ds5", 0.5), ("E5", 0.5),
    ("B4", 0.5), ("D5", 0.5), ("C5", 0.5), ("A4", 1),
    ("C4", 0.5), ("E4", 0.5), ("A4", 0.5), ("B4", 1),
    ("D5", 0.5), ("C5", 0.5), ("B4", 0.5), ("A4", 2),
]

# ------------------------------------------------------------------
# Himno a la Alegría (Beethoven, 9na Sinfonía)
# Capítulo 1: tema | Capítulo 2: repetición | Capítulo 3: puente
# Capítulo 4: regreso al tema | Capítulo 5: coda con arpegio
# ------------------------------------------------------------------
HIMNO_TEMA = [
    ("E4", 1), ("E4", 1), ("F4", 1), ("G4", 1),
    ("G4", 1), ("F4", 1), ("E4", 1), ("D4", 1),
    ("C4", 1), ("C4", 1), ("D4", 1), ("E4", 1),
    ("E4", 1.5), ("D4", 0.5), ("D4", 2),
]

HIMNO_PUENTE = [
    ("D4", 1), ("D4", 1), ("E4", 1), ("C4", 1),
    ("D4", 1), ("E4", 0.5), ("F4", 0.5), ("E4", 1), ("C4", 1),
    ("D4", 1), ("E4", 0.5), ("F4", 0.5), ("E4", 1), ("D4", 1),
    ("C4", 1), ("D4", 1), ("G3", 2),
]

HIMNO_REGRESO = [
    ("E4", 1), ("E4", 1), ("F4", 1), ("G4", 1),
    ("G4", 1), ("F4", 1), ("E4", 1), ("D4", 1),
    ("C4", 1), ("C4", 1), ("D4", 1), ("E4", 1),
    ("D4", 1), ("C4", 1), ("C4", 2),
]

HIMNO_CODA = [
    ("C4", 0.5), ("E4", 0.5), ("G4", 0.5), ("C5", 0.5),
    ("G4", 0.5), ("E4", 0.5), ("C4", 1),
    ("G3", 1), ("C4", 2),
]

MELODIA_HIMNO_ALEGRIA = (
    HIMNO_TEMA          # Capítulo 1
    + HIMNO_TEMA        # Capítulo 2 (repetición)
    + HIMNO_PUENTE      # Capítulo 3 (puente)
    + HIMNO_REGRESO     # Capítulo 4 (regreso)
    + HIMNO_CODA        # Capítulo 5 (coda con arpegio)
)

# ------------------------------------------------------------------
# Minueto en Sol (Bach/Petzold)
# CORREGIDO: melodía completa subida 1 octava para reflejar el
# original (ver nota arriba). A - repetición de A - B - repetición
# de B - coda.
# ------------------------------------------------------------------
MINUETO_A = [
    ("D5", 1), ("G4", 1), ("A4", 1), ("B4", 1),
    ("C5", 1), ("D5", 2), ("G4", 1),
    ("G4", 1), ("Fs4", 1), ("G4", 1), ("A4", 1),
    ("B4", 2), ("B4", 1),
    ("C5", 1), ("B4", 1), ("A4", 1), ("G4", 1),
    ("Fs4", 1), ("G4", 2), ("D4", 1),
    ("G4", 1), ("A4", 1), ("B4", 1), ("C5", 1),
    ("D5", 2), ("D5", 1),
]

MINUETO_B = [
    ("G5", 1), ("Fs5", 1), ("G5", 1), ("D5", 1),
    ("G5", 1), ("Fs5", 1), ("G5", 1), ("B4", 1),
    ("C5", 1), ("B4", 1), ("A4", 1), ("G4", 1),
    ("Fs4", 1), ("G4", 2), ("G4", 1),
]

MINUETO_CODA = [
    ("A4", 1), ("B4", 1), ("C5", 1),
    ("D5", 2), ("G4", 1),
    ("Fs4", 1), ("G4", 2),
]

MELODIA_MINUETO_SOL = (
    MINUETO_A
    + MINUETO_A     # repetición de A
    + MINUETO_B
    + MINUETO_B     # repetición de B
    + MINUETO_CODA
)

# ------------------------------------------------------------------
# Canon en Re (Pachelbel)
# Bajo solo -> primera variación (escala descendente, la más famosa
# del Canon) -> variación más movida (corcheas) -> regreso al bajo
# -> coda.
# ------------------------------------------------------------------
OSTINATO_CANON_RE = [
    ("D4", 1), ("A3", 1), ("B3", 1), ("Fs3", 1),
    ("G3", 1), ("D3", 1), ("G3", 1), ("A3", 1),
]

CANON_VARIACION_1 = [
    ("Fs4", 1), ("E4", 1), ("D4", 1), ("Cs4", 1),
    ("B3", 1), ("A3", 1), ("B3", 1), ("Cs4", 1),
]

CANON_VARIACION_2 = [
    ("Fs4", 0.5), ("E4", 0.5), ("E4", 0.5), ("D4", 0.5),
    ("D4", 0.5), ("Cs4", 0.5), ("Cs4", 0.5), ("B3", 0.5),
    ("B3", 0.5), ("A3", 0.5), ("A3", 0.5), ("B3", 0.5),
    ("B3", 0.5), ("Cs4", 0.5), ("Cs4", 0.5), ("D4", 0.5),
]

CANON_CODA = [
    ("D4", 1), ("Cs4", 1), ("B3", 1), ("A3", 1),
    ("G3", 1), ("Fs3", 1), ("G3", 2),
    ("A3", 1), ("D4", 2),
]

MELODIA_CANON_RE = (
    repetir(OSTINATO_CANON_RE, 3)      # bajo solo
    + CANON_VARIACION_1 * 2            # primera variación
    + CANON_VARIACION_2 * 2            # variación más movida
    + repetir(OSTINATO_CANON_RE, 2)    # regreso al bajo
    + CANON_CODA                       # coda
)

# ------------------------------------------------------------------
# Amazing Grace (himno tradicional)
# Estrofa -> estrofa una octava arriba (más intensidad) -> estrofa
# de regreso -> coda. Notas de la estrofa alta escritas literalmente.
# ------------------------------------------------------------------
AMAZING_GRACE_ESTROFA = [
    ("G3", 1), ("C4", 1), ("C4", 0.5), ("E4", 0.5), ("D4", 1), ("C4", 1),
    ("A3", 1), ("G3", 2),
    ("G3", 1), ("C4", 1), ("C4", 0.5), ("E4", 0.5), ("D4", 1), ("C4", 1),
    ("A3", 1), ("G3", 2),
    ("G3", 1), ("C4", 1), ("E4", 1), ("G4", 1), ("Fs4", 1),
    ("E4", 1), ("D4", 2),
    ("C4", 1), ("E4", 1), ("D4", 1), ("C4", 1),
    ("A3", 1), ("G3", 2),
]

AMAZING_GRACE_ESTROFA_OCTAVA_ARRIBA = [
    ("G4", 1), ("C5", 1), ("C5", 0.5), ("E5", 0.5), ("D5", 1), ("C5", 1),
    ("A4", 1), ("G4", 2),
    ("G4", 1), ("C5", 1), ("C5", 0.5), ("E5", 0.5), ("D5", 1), ("C5", 1),
    ("A4", 1), ("G4", 2),
    ("G4", 1), ("C5", 1), ("E5", 1), ("G5", 1), ("Fs5", 1),
    ("E5", 1), ("D5", 2),
    ("C5", 1), ("E5", 1), ("D5", 1), ("C5", 1),
    ("A4", 1), ("G4", 2),
]

AMAZING_GRACE_CODA = [
    ("D4", 1), ("C4", 1), ("A3", 1), ("G3", 2),
]

MELODIA_AMAZING_GRACE = (
    AMAZING_GRACE_ESTROFA
    + AMAZING_GRACE_ESTROFA_OCTAVA_ARRIBA
    + AMAZING_GRACE_ESTROFA                    # regreso
    + AMAZING_GRACE_CODA
)

# ------------------------------------------------------------------
# Greensleeves (tradicional inglesa)
# Verso -> repetición -> variación aguda tipo estribillo (octava
# arriba) -> regreso -> cierre. Notas escritas literalmente.
# ------------------------------------------------------------------
GREENSLEEVES_VERSO = [
    ("A3", 1), ("C4", 1), ("D4", 1), ("E4", 1),
    ("F4", 1), ("E4", 1), ("D4", 1), ("B3", 1),
    ("C4", 1), ("B3", 1), ("A3", 1), ("A3", 1),
    ("E3", 1), ("Gs3", 0.5), ("A3", 0.5), ("A3", 1),
    ("A3", 1), ("C4", 1), ("D4", 1), ("E4", 1),
    ("F4", 1), ("E4", 1), ("D4", 1), ("B3", 1),
    ("C4", 1), ("A3", 1), ("Gs3", 1), ("A3", 2),
]

GREENSLEEVES_VERSO_OCTAVA_ARRIBA = [
    ("A4", 1), ("C5", 1), ("D5", 1), ("E5", 1),
    ("F5", 1), ("E5", 1), ("D5", 1), ("B4", 1),
    ("C5", 1), ("B4", 1), ("A4", 1), ("A4", 1),
    ("E4", 1), ("Gs4", 0.5), ("A4", 0.5), ("A4", 1),
    ("A4", 1), ("C5", 1), ("D5", 1), ("E5", 1),
    ("F5", 1), ("E5", 1), ("D5", 1), ("B4", 1),
    ("C5", 1), ("A4", 1), ("Gs4", 1), ("A4", 2),
]

GREENSLEEVES_CIERRE = [
    ("D4", 1), ("C4", 1), ("B3", 1), ("A3", 1),
    ("Gs3", 1), ("A3", 2),
]

MELODIA_GREENSLEEVES = (
    GREENSLEEVES_VERSO
    + GREENSLEEVES_VERSO                       # repetición
    + GREENSLEEVES_VERSO_OCTAVA_ARRIBA         # variación aguda (estribillo)
    + GREENSLEEVES_VERSO                       # regreso
    + GREENSLEEVES_CIERRE                      # cierre
)

# ------------------------------------------------------------------
# Twinkle Twinkle Little Star (tradicional) - para practicar corto
# y fácil, en la región de Do central.
# ------------------------------------------------------------------
MELODIA_TWINKLE = [
    ("C4", 1), ("C4", 1), ("G4", 1), ("G4", 1), ("A4", 1), ("A4", 1), ("G4", 2),
    ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 1), ("D4", 1), ("C4", 2),
    ("G4", 1), ("G4", 1), ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 2),
    ("G4", 1), ("G4", 1), ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 2),
    ("C4", 1), ("C4", 1), ("G4", 1), ("G4", 1), ("A4", 1), ("A4", 1), ("G4", 2),
    ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 1), ("D4", 1), ("C4", 2),
]

# ------------------------------------------------------------------
# Mary Had a Little Lamb (tradicional) - todavía más fácil, buena
# para empezar.
# ------------------------------------------------------------------
MELODIA_MARY = [
    ("E4", 1), ("D4", 1), ("C4", 1), ("D4", 1), ("E4", 1), ("E4", 1), ("E4", 2),
    ("D4", 1), ("D4", 1), ("D4", 2),
    ("E4", 1), ("G4", 1), ("G4", 2),
    ("E4", 1), ("D4", 1), ("C4", 1), ("D4", 1), ("E4", 1), ("E4", 1), ("E4", 1), ("E4", 1),
    ("D4", 1), ("D4", 1), ("E4", 1), ("D4", 1), ("C4", 2),
]

# ------------------------------------------------------------------
# Happy Birthday (melodía tradicional, de "Good Morning to All",
# 1893 - de dominio público) - con anacrusa (pickup) al inicio de
# cada frase, como se toca de verdad.
# ------------------------------------------------------------------
MELODIA_CUMPLEANOS = [
    ("G3", 0.5), ("G3", 0.5), ("A3", 1), ("G3", 1), ("C4", 1), ("B3", 2),
    ("G3", 0.5), ("G3", 0.5), ("A3", 1), ("G3", 1), ("D4", 1), ("C4", 2),
    ("G3", 0.5), ("G3", 0.5), ("G4", 1), ("E4", 1), ("C4", 1), ("B3", 1), ("A3", 2),
    ("F4", 0.5), ("F4", 0.5), ("E4", 1), ("C4", 1), ("D4", 1), ("C4", 2),
]

# ------------------------------------------------------------------
# Jingle Bells (tradicional, solo el estribillo, que es la parte que
# todo el mundo reconoce) - se repite con repetir().
# ------------------------------------------------------------------
MELODIA_JINGLE_BELLS = [
    ("E4", 1), ("E4", 1), ("E4", 2),
    ("E4", 1), ("E4", 1), ("E4", 2),
    ("E4", 1), ("G4", 1), ("C4", 1), ("D4", 1), ("E4", 4),
    ("F4", 1), ("F4", 1), ("F4", 1), ("F4", 1),
    ("F4", 1), ("E4", 1), ("E4", 1), ("E4", 0.5), ("E4", 0.5),
    ("D4", 1), ("D4", 1), ("E4", 1), ("D4", 2), ("G4", 2),
]

# ------------------------------------------------------------------
# Lista final de canciones
# ------------------------------------------------------------------
SONGS = [
    ("Para Elisa (Beethoven)", repetir(MELODIA_PARA_ELISA, 5)),  # ~63s a 100 BPM
    ("Himno a la Alegría (Beethoven)", MELODIA_HIMNO_ALEGRIA),
    ("Minueto en Sol (Bach/Petzold)", MELODIA_MINUETO_SOL),
    ("Canon en Re (Pachelbel)", MELODIA_CANON_RE),
    ("Amazing Grace (himno tradicional)", MELODIA_AMAZING_GRACE),
    ("Greensleeves (tradicional inglesa)", MELODIA_GREENSLEEVES),
    ("Twinkle Twinkle Little Star (tradicional)", repetir(MELODIA_TWINKLE, 2)),
    ("Mary Had a Little Lamb (tradicional)", repetir(MELODIA_MARY, 3)),
    ("Happy Birthday (tradicional, dominio público)", repetir(MELODIA_CUMPLEANOS, 3)),
    ("Jingle Bells (estribillo, tradicional)", repetir(MELODIA_JINGLE_BELLS, 2)),
]