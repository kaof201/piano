"""
menu_view.py - Menu de seleccion de canciones (modo practica)
==================================================================
Dibuja la lista de canciones de songs.py como tarjetas: cada una con
un acento de color, el numero/tecla rapida para elegirla, el nombre,
y una duracion aproximada calculada a partir de sus notas. Tambien
soporta un "cursor" que se mueve con las flechas arriba/abajo y se
confirma con Enter, ademas del atajo directo de pulsar el numero.

Se dibuja a pantalla completa (no solo en la cabecera) porque un
menu de canciones es, en esencia, otra pantalla distinta a la del
piano en si.
"""

import pygame

import theme
from config import SIDE_MARGIN, WIDTH, HEIGHT, DEFAULT_BPM
from music_theory import song_duration_seconds
from visuals import rounded_rect_vertical_gradient, drop_shadow_rect, soft_glow, render_text_with_shadow

CARD_TOP = 96
CARD_GAP = 14
CARD_BOTTOM_MARGIN = 60


def _card_rects(song_count):
    available = HEIGHT - CARD_TOP - CARD_BOTTOM_MARGIN
    raw_height = (available - CARD_GAP * (song_count - 1)) / song_count if song_count else 0
    card_height = max(56, min(96, int(raw_height)))
    width = WIDTH - SIDE_MARGIN * 2

    rects = []
    y = CARD_TOP
    for _ in range(song_count):
        rects.append(pygame.Rect(SIDE_MARGIN, y, width, card_height))
        y += card_height + CARD_GAP
    return rects


def _draw_card(screen, fonts, index, name, notes, rect, is_selected):
    accent = theme.accent_for_index(index)

    drop_shadow_rect(screen, rect, radius=14, offset=(0, 5), alpha=130 if is_selected else 80)

    top_c = tuple(min(255, c + 16) for c in theme.PANEL_BG) if is_selected else theme.PANEL_BG
    rounded_rect_vertical_gradient(screen, rect, top_c, theme.PANEL_BG, radius=14)

    border_color = accent if is_selected else theme.PANEL_BORDER
    pygame.draw.rect(screen, border_color, rect, width=3 if is_selected else 2, border_radius=14)

    accent_bar = pygame.Rect(rect.x, rect.y, 8, rect.height)
    pygame.draw.rect(screen, accent, accent_bar, border_top_left_radius=14, border_bottom_left_radius=14)

    badge_center = (rect.x + 44, rect.centery)
    if is_selected:
        soft_glow(screen, badge_center, radius=32, color=accent, max_alpha=90)
    pygame.draw.circle(screen, accent, badge_center, 20)
    num_text = fonts["badge"].render(str(index + 1), True, (22, 20, 28))
    ntw, nth = num_text.get_size()
    screen.blit(num_text, (badge_center[0] - ntw // 2, badge_center[1] - nth // 2))

    title = fonts["menu_title"].render(name, True, theme.TEXT_PRIMARY)
    screen.blit(title, (rect.x + 78, rect.y + rect.height // 2 - title.get_height() - 2))

    seconds = song_duration_seconds(notes, DEFAULT_BPM)
    meta = f"{len(notes)} notas   -   ~{seconds / 60:.1f} min a {DEFAULT_BPM} BPM"
    meta_text = fonts["menu_meta"].render(meta, True, theme.TEXT_DIM)
    screen.blit(meta_text, (rect.x + 78, rect.y + rect.height // 2 + 4))


def draw_song_menu(screen, fonts, songs, selected_index):
    render_text_with_shadow(
        screen, fonts["title"], "Elige una cancion para practicar",
        theme.TEXT_PRIMARY, (SIDE_MARGIN, 24),
    )
    subtitle = "Cada tarjeta muestra cuantas notas tiene y cuanto dura aprox. al tempo por defecto."
    screen.blit(fonts["subtitle"].render(subtitle, True, theme.TEXT_DIM), (SIDE_MARGIN, 62))

    rects = _card_rects(len(songs))
    for i, ((name, notes), rect) in enumerate(zip(songs, rects)):
        _draw_card(screen, fonts, i, name, notes, rect, i == selected_index)

    hint = "Flechas arriba/abajo: moverte   |   Enter o el numero: elegir   |   P: cancelar"
    screen.blit(fonts["subtitle"].render(hint, True, theme.TEXT_DIM), (SIDE_MARGIN, HEIGHT - 40))
