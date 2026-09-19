"""
menu_view.py - Menu de seleccion de canciones (modo practica)
==================================================================
Dibuja la lista de canciones de songs.py como tarjetas: cada una con
un acento de color, el numero/tecla rapida para elegirla, el nombre,
y una duracion aproximada calculada a partir de sus notas.

Cada tarjeta es, en el fondo, un boton con tres estados posibles:
normal, hover (el mouse esta encima) y seleccionado (el cursor de
teclado esta ahi). Se puede elegir una cancion de tres formas
equivalentes: moviendose con las flechas y Enter, pulsando
directamente su numero, o haciendo clic con el mouse (ver
game.py: _handle_mouse_click, que usa card_rects() de aqui para
saber donde cayo el clic).

Se dibuja a pantalla completa (no solo en la cabecera) porque un
menu de canciones es, en esencia, otra pantalla distinta a la del
piano en si.
"""

import pygame

import theme
from config import STAGE_X, STAGE_WIDTH, HEIGHT, DEFAULT_BPM
from music_theory import song_duration_seconds
from visuals import rounded_rect_vertical_gradient, drop_shadow_rect, render_text_with_shadow, icon_note, cached_text

CARD_TOP = 100
CARD_GAP = 16
CARD_BOTTOM_MARGIN = 60


def card_rects(song_count):
    """Posicion/tamano de cada tarjeta. Publica porque game.py la usa
    para saber que tarjeta cayo bajo el clic del mouse."""
    available = HEIGHT - CARD_TOP - CARD_BOTTOM_MARGIN
    raw_height = (available - CARD_GAP * (song_count - 1)) / song_count if song_count else 0
    card_height = max(56, min(92, int(raw_height)))
    rects = []
    y = CARD_TOP
    for _ in range(song_count):
        rects.append(pygame.Rect(STAGE_X, y, STAGE_WIDTH, card_height))
        y += card_height + CARD_GAP
    return rects


def _draw_card(screen, fonts, index, name, notes, rect, is_selected, is_hover):
    accent = theme.accent_for_index(index)

    drop_shadow_rect(screen, rect, radius=10, offset=(0, 3), alpha=70)

    if is_selected:
        bg = theme.PANEL_SELECTED_BG
    elif is_hover:
        bg = theme.PANEL_HOVER_BG
    else:
        bg = theme.PANEL_BG
    rounded_rect_vertical_gradient(screen, rect, bg, bg, radius=10)

    border_color = accent if is_selected else theme.PANEL_BORDER
    pygame.draw.rect(screen, border_color, rect, width=2 if is_selected else 1, border_radius=10)

    accent_bar = pygame.Rect(rect.x, rect.y, 5, rect.height)
    pygame.draw.rect(screen, accent, accent_bar, border_top_left_radius=10, border_bottom_left_radius=10)

    badge_center = (rect.x + 42, rect.centery)
    pygame.draw.circle(screen, accent, badge_center, 19)
    num_text = cached_text(fonts["badge"], str(index + 1), (22, 20, 28))
    ntw, nth = num_text.get_size()
    screen.blit(num_text, (badge_center[0] - ntw // 2, badge_center[1] - nth // 2))

    title = cached_text(fonts["menu_title"], name, theme.TEXT_PRIMARY)
    screen.blit(title, (rect.x + 74, rect.y + rect.height // 2 - title.get_height() - 2))

    seconds = song_duration_seconds(notes, DEFAULT_BPM)
    meta = f"{len(notes)} notas  -  ~{seconds / 60:.1f} min a {DEFAULT_BPM} BPM"
    meta_text = cached_text(fonts["menu_meta"], meta, theme.TEXT_DIM)
    screen.blit(meta_text, (rect.x + 74, rect.y + rect.height // 2 + 4))

    if is_selected:
        icon_note(screen, (rect.right - 26, rect.centery), 20, accent)


def draw_song_menu(screen, fonts, songs, selected_index, mouse_pos=(0, 0)):
    render_text_with_shadow(
        screen, fonts["title"], "Elige una cancion para practicar",
        theme.TEXT_PRIMARY, (STAGE_X, 26),
    )
    subtitle = "Cada tarjeta muestra cuantas notas tiene y cuanto dura aprox. al tempo por defecto."
    screen.blit(cached_text(fonts["subtitle"], subtitle, theme.TEXT_DIM), (STAGE_X, 64))

    rects = card_rects(len(songs))
    for i, ((name, notes), rect) in enumerate(zip(songs, rects)):
        is_hover = rect.collidepoint(mouse_pos)
        _draw_card(screen, fonts, i, name, notes, rect, i == selected_index, is_hover)

    hint = "Flechas arriba/abajo o clic: moverte  -  Enter o el numero: elegir  -  P: cancelar"
    screen.blit(cached_text(fonts["subtitle"], hint, theme.TEXT_DIM), (STAGE_X, HEIGHT - 40))
