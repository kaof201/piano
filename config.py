"""
config.py - Configuracion estatica del piano de escritorio
=============================================================
Aqui viven los numeros y mapas que casi nunca cambian: distribucion
de teclas del teclado fisico, rangos de octavas, tamanos en pantalla
y parametros del modo practica. Si algun dia quieres remapear teclas,
cambiar el tamano de la ventana o ajustar el rango de BPM, este es el
archivo indicado.

No hay logica de dibujo ni de audio aqui, solo datos - asi el resto
del programa se lee sin ruido.
"""

import pygame

# ------------------------------------------------------------------
# Audio / teoria musical
# ------------------------------------------------------------------
SAMPLE_RATE = 44100
BASE_MIDI_DEFAULT = 48  # C3 = MIDI 48
OCTAVE_SHIFT_RANGE = (-24, 24)  # permite llegar de C1 a C5

VALID_BASES = [
    BASE_MIDI_DEFAULT + 12 * k
    for k in range(OCTAVE_SHIFT_RANGE[0] // 12, OCTAVE_SHIFT_RANGE[1] // 12 + 1)
]

NOTE_NAMES = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]

# ------------------------------------------------------------------
# Modo practica
# ------------------------------------------------------------------
DEFAULT_BPM = 100
BPM_MIN, BPM_MAX, BPM_STEP = 40, 240, 5

# Tolerancia: si sueltas la tecla habiendo sostenido al menos este
# porcentaje del tiempo requerido, igual se cuenta como valida.
HOLD_TOLERANCE = 1.0  # 1.0 = debe cumplirse el 100% del tiempo

# ------------------------------------------------------------------
# Distribucion de teclas del teclado fisico -> teclas del piano
# ------------------------------------------------------------------
OFFSET_TO_KEY = {
    0: pygame.K_z,  1: pygame.K_s,  2: pygame.K_x,  3: pygame.K_d,
    4: pygame.K_c,  5: pygame.K_v,  6: pygame.K_g,  7: pygame.K_b,
    8: pygame.K_h,  9: pygame.K_n,  10: pygame.K_j, 11: pygame.K_m,
    12: pygame.K_q, 13: pygame.K_2, 14: pygame.K_w, 15: pygame.K_3,
    16: pygame.K_e, 17: pygame.K_r, 18: pygame.K_5, 19: pygame.K_t,
    20: pygame.K_6, 21: pygame.K_y, 22: pygame.K_7, 23: pygame.K_u,
    24: pygame.K_i,
}
KEY_OFFSETS = {v: k for k, v in OFFSET_TO_KEY.items()}

OFFSET_TO_LABEL = {
    0: "Z", 1: "S", 2: "X", 3: "D", 4: "C", 5: "V", 6: "G", 7: "B",
    8: "H", 9: "N", 10: "J", 11: "M", 12: "Q", 13: "2", 14: "W",
    15: "3", 16: "E", 17: "R", 18: "5", 19: "T", 20: "6", 21: "Y",
    22: "7", 23: "U", 24: "I",
}

ROW_LOW = [(0, False), (1, True), (2, False), (3, True), (4, False),
           (5, False), (6, True), (7, False), (8, True), (9, False),
           (10, True), (11, False)]                       # octava baja
ROW_HIGH = [(12, False), (13, True), (14, False), (15, True), (16, False),
            (17, False), (18, True), (19, False), (20, True), (21, False),
            (22, True), (23, False), (24, False)]          # octava alta

NUM_KEYS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
PLUS_KEYS = [pygame.K_EQUALS, pygame.K_KP_PLUS]
MINUS_KEYS = [pygame.K_MINUS, pygame.K_KP_MINUS]
FULLSCREEN_KEYS = [pygame.K_F11]
MENU_UP_KEYS = [pygame.K_UP]
MENU_DOWN_KEYS = [pygame.K_DOWN]
MENU_CONFIRM_KEYS = [pygame.K_RETURN, pygame.K_KP_ENTER]

# ------------------------------------------------------------------
# Tamanos de la ventana y las teclas
# ------------------------------------------------------------------
WHITE_KEY_W = 92
WHITE_KEY_H = 280
BLACK_KEY_W = 58
BLACK_KEY_H = 175
ROW_GAP = 30
TOP_MARGIN = 230   # espacio para titulo, progreso y proximas notas
BOTTOM_MARGIN = 50
SIDE_MARGIN = 24
PRESS_DIP = 8  # cuantos px "se hunde" una tecla activa al presionarla

MAX_WHITES = max(
    sum(1 for _, black in ROW_LOW if not black),
    sum(1 for _, black in ROW_HIGH if not black),
)
WIDTH = SIDE_MARGIN * 2 + MAX_WHITES * WHITE_KEY_W
HEIGHT = TOP_MARGIN + WHITE_KEY_H + ROW_GAP + WHITE_KEY_H + BOTTOM_MARGIN

MODE_FREE = "free"
MODE_MENU = "menu"
MODE_SONG = "song"
