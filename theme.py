"""
theme.py - Paleta visual y tipografias
=========================================
Todo lo que tiene que ver con "como se ve" (colores, degradados,
fuentes) vive aqui, separado de config.py (que es solo tamanos y
mapas de teclas) y de los archivos que DIBUJAN usando esta paleta
(visuals.py, piano_view.py, menu_view.py, hud_view.py, background.py).

Cambiar el tema de color de toda la app deberia ser, idealmente,
cuestion de tocar solo este archivo.
"""

import pygame

# ------------------------------------------------------------------
# Fondo (degradado + particulas ambientales)
# ------------------------------------------------------------------
BG_TOP = (14, 12, 24)
BG_BOTTOM = (28, 19, 42)
PARTICLE_COLOR = (255, 214, 140)

# ------------------------------------------------------------------
# Teclas
# ------------------------------------------------------------------
WHITE_TOP = (255, 255, 255)
WHITE_BOTTOM = (221, 219, 230)
WHITE_ACTIVE_TOP = (255, 226, 140)
WHITE_ACTIVE_BOTTOM = (255, 186, 76)
WHITE_BORDER = (18, 16, 26)

BLACK_TOP = (52, 49, 62)
BLACK_BOTTOM = (14, 13, 20)
BLACK_ACTIVE_TOP = (255, 176, 84)
BLACK_ACTIVE_BOTTOM = (210, 118, 18)
BLACK_GLOSS = (94, 90, 106)

KEY_LABEL_DARK = (35, 33, 45)
KEY_LABEL_LIGHT = (250, 250, 252)

# Colores de guia del modo practica
TARGET_GLOW = (86, 232, 140)     # nota que debes tocar AHORA (verde)
NEXT_GLOW = (94, 168, 255)       # nota que sigue DESPUES (azul)
WARN_GLOW = (255, 176, 64)       # aviso de cambio de octava

# ------------------------------------------------------------------
# Texto / UI general
# ------------------------------------------------------------------
TEXT_PRIMARY = (240, 238, 248)
TEXT_DIM = (152, 148, 170)
TEXT_ACCENT = (255, 200, 90)
PANEL_BG = (32, 28, 48)
PANEL_BORDER = (62, 56, 82)
PROGRESS_BG = (48, 44, 64)

# Paleta de acentos para las tarjetas del menu de canciones (se asigna
# una por indice, ciclica si hay mas canciones que colores).
SONG_ACCENTS = [
    (255, 138, 128),   # coral
    (129, 212, 250),   # celeste
    (174, 213, 129),   # verde suave
    (255, 214, 102),   # ambar
    (206, 147, 216),   # lila
    (128, 222, 234),   # turquesa
]


def accent_for_index(index):
    return SONG_ACCENTS[index % len(SONG_ACCENTS)]


def load_fonts():
    """Crea y devuelve todas las fuentes que usa la app en un dict."""
    return {
        "title": pygame.font.SysFont("Arial", 28, bold=True),
        "subtitle": pygame.font.SysFont("Arial", 16),
        "body": pygame.font.SysFont("Arial", 18),
        "body_bold": pygame.font.SysFont("Arial", 18, bold=True),
        "key_label": pygame.font.SysFont("Arial", 22, bold=True),
        "menu_title": pygame.font.SysFont("Arial", 21, bold=True),
        "menu_meta": pygame.font.SysFont("Arial", 15),
        "badge": pygame.font.SysFont("Arial", 20, bold=True),
        "chip": pygame.font.SysFont("Arial", 17, bold=True),
    }
