"""
side_panels.py - Los dos paneles laterales
==============================================
Aprovechan el espacio a los costados del teclado.

  - Panel IZQUIERDO ("Practica"): durante la practica de una cancion,
    muestra la letra sincronizada por palabra (si esa cancion tiene
    una en songs.LYRICS) y un "piano roll": un riel vertical con las
    proximas notas como bloques de color (sin mostrar la tecla del
    teclado que les corresponde -- eso ya lo indica el borde de color
    sobre la tecla real). La mas proxima esta abajo, pegada a la
    linea de "AHORA", y se va deslizando hacia ella a medida que la
    sostienes.

  - Panel DERECHO ("Puntajes"): el puntaje/combo en vivo (con el
    popup breve de feedback tipo "+15 (x1.5)" o "-5") y debajo, la
    tabla de mejores puntajes de la sesion para todas las canciones
    (se resetea al cerrar el programa).

Ninguno de los dos modifica el estado del juego, solo lo leen para
dibujar. Los unicos brillos que usan son puntuales (el popup y el
pop-in del texto), nunca halos permanentes.
"""

import pygame

import theme
from config import (
    LEFT_PANEL_X, RIGHT_PANEL_X, SIDE_PANEL_WIDTH, PANEL_TOP,
    HEIGHT, BOTTOM_MARGIN, MODE_SONG, ROLL_MAX_UPCOMING,
)
from music_theory import label_for_absolute_midi
from visuals import (
    rounded_rect_vertical_gradient, drop_shadow_rect, icon_note,
    icon_chart, icon_flame, icon_mic, icon_falling_notes, cached_text,
)

try:
    from songs import LYRICS
except ImportError:  # pragma: no cover - por si algun dia songs.py no la define
    LYRICS = {}

PANEL_BOTTOM = HEIGHT - BOTTOM_MARGIN // 2
POPUP_POP_MS = 140  # duracion del pequeno "pop" de aparicion del popup


def _panel_rect(x):
    return pygame.Rect(x, PANEL_TOP, SIDE_PANEL_WIDTH, PANEL_BOTTOM - PANEL_TOP)


def _panel_frame(screen, rect, title, fonts, icon_fn=None):
    drop_shadow_rect(screen, rect, radius=10, offset=(0, 3), alpha=60)
    rounded_rect_vertical_gradient(screen, rect, theme.PANEL_BG, theme.PANEL_BG_SOFT, radius=10)
    pygame.draw.rect(screen, theme.PANEL_BORDER, rect, width=1, border_radius=10)

    text_x = rect.x + 18
    if icon_fn:
        icon_fn(screen, pygame.Rect(rect.x + 16, rect.y + 14, 20, 20), theme.TEXT_ACCENT)
        text_x = rect.x + 44

    title_surf = cached_text(fonts["panel_title"], title, theme.TEXT_PRIMARY)
    screen.blit(title_surf, (text_x, rect.y + 16))
    underline_y = rect.y + 16 + title_surf.get_height() + 10
    pygame.draw.line(screen, theme.PANEL_BORDER, (rect.x + 18, underline_y), (rect.right - 18, underline_y), 1)
    return underline_y + 18


# ------------------------------------------------------------------
# Panel izquierdo: letra + piano roll
# ------------------------------------------------------------------
def draw_left_panel(screen, fonts, state):
    rect = _panel_rect(LEFT_PANEL_X)
    y = _panel_frame(screen, rect, "Practica", fonts, icon_fn=lambda s, r, c: icon_note(s, r.center, r.width, c))
    inner_x = rect.x + 18
    inner_w = rect.width - 36

    if state["mode"] != MODE_SONG or not state["song_midis"]:
        tip = cached_text(fonts["subtitle"], "Pulsa P para elegir una cancion", theme.TEXT_DIM)
        screen.blit(tip, (inner_x, y + 4))
        return

    y = _draw_lyrics(screen, fonts, inner_x, inner_w, y, state)
    pygame.draw.line(screen, theme.PANEL_BORDER, (inner_x, y), (inner_x + inner_w, y), 1)
    y += 18

    _draw_note_rail(screen, fonts, rect, inner_x, inner_w, y, state)


def _draw_lyrics(screen, fonts, x, w, y, state):
    icon_mic(screen, (x + 9, y + 10), 20, theme.TEXT_DIM)
    header = cached_text(fonts["menu_meta"], "LETRA", theme.TEXT_DIM)
    screen.blit(header, (x + 22, y + 2))
    y += header.get_height() + 14

    entry = LYRICS.get(state["song_name"])
    if entry is None:
        empty = cached_text(fonts["subtitle"], "(sin letra para esta pieza)", theme.TEXT_DIM)
        screen.blit(empty, (x, y))
        return y + empty.get_height() + 12

    cycle_len, words = entry
    idx = state["song_index"] % cycle_len

    current_word = ""
    next_word = ""
    for word_idx, word in words:
        if word_idx <= idx:
            current_word = word
        elif not next_word:
            next_word = word

    if current_word:
        current_surf = cached_text(fonts["body_bold"], current_word, theme.TEXT_ACCENT)
        screen.blit(current_surf, (x, y))
        y += current_surf.get_height() + 4
    if next_word:
        next_surf = cached_text(fonts["menu_meta"], next_word, theme.TEXT_DIM)
        screen.blit(next_surf, (x, y))
        y += next_surf.get_height()

    return y + 14


def _draw_note_rail(screen, fonts, rect, x, w, y, state):
    """El 'piano roll': un riel vertical angosto con las proximas
    notas apiladas como bloques de color (sin letras): la mas lejana
    arriba, la objetivo abajo del todo pegada a la linea de AHORA. Su
    bloque se desliza hacia esa linea a medida que avanza el tiempo
    que llevas sostenida la tecla real en el piano."""
    icon_falling_notes(screen, pygame.Rect(x, y + 2, 16, 16), theme.TEXT_DIM)
    header = cached_text(fonts["menu_meta"], "PROXIMAS NOTAS", theme.TEXT_DIM)
    screen.blit(header, (x + 22, y))
    y += header.get_height() + 14

    rail_top = y
    rail_bottom = rect.bottom - 22
    rail_height = max(60, rail_bottom - rail_top)
    now_line_y = rail_bottom

    midis = state["song_midis"]
    idx = state["song_index"]
    base_midi = state["base_midi"]
    upcoming = midis[idx:idx + ROLL_MAX_UPCOMING]
    if not upcoming:
        return

    slot_h = rail_height / ROLL_MAX_UPCOMING
    block_h = max(20, slot_h * 0.68)

    target_fraction = 0.0
    if state["holding_offset"] is not None and midis:
        target_offset_view = midis[idx] - base_midi if idx < len(midis) else None
        if target_offset_view == state["holding_offset"]:
            elapsed = (pygame.time.get_ticks() - state["hold_start"]) / 1000.0
            seconds_per_beat = 60.0 / state["bpm"]
            required = state["song_durations"][idx] * seconds_per_beat
            target_fraction = min(1.0, elapsed / required) if required > 0 else 1.0

    for i, midi in enumerate(upcoming):
        _, in_view = label_for_absolute_midi(midi, base_midi)
        slot_from_top = (len(upcoming) - 1) - i
        slot_top = rail_top + slot_from_top * slot_h

        if i == 0:
            color = theme.TARGET_GLOW if in_view else theme.WARN_GLOW
            slot_bottom_for_slide = slot_top + slot_h - block_h
            block_y = slot_top + (slot_bottom_for_slide - slot_top) * target_fraction
        elif i == 1:
            color = theme.NEXT_GLOW if in_view else (90, 88, 100)
            block_y = slot_top
        else:
            fade = max(60, 190 - i * 30)
            color = (fade, fade, fade)
            block_y = slot_top

        block_rect = pygame.Rect(x, int(block_y), w, int(block_h))
        rounded_rect_vertical_gradient(screen, block_rect, color, tuple(max(0, c - 35) for c in color), radius=6)
        icon_color = (24, 22, 30) if i <= 1 else (60, 58, 68)
        icon_note(screen, block_rect.center, block_rect.height * 0.75, icon_color)

    pygame.draw.line(screen, theme.PANEL_BORDER, (x, now_line_y), (x + w, now_line_y), 1)
    now_label = cached_text(fonts["menu_meta"], "AHORA", theme.TEXT_DIM)
    screen.blit(now_label, (x + w - now_label.get_width(), now_line_y + 6))


# ------------------------------------------------------------------
# Panel derecho: puntaje en vivo + mejores puntajes de la sesion
# ------------------------------------------------------------------
def draw_right_panel(screen, fonts, state, songs):
    rect = _panel_rect(RIGHT_PANEL_X)
    y = _panel_frame(screen, rect, "Puntajes", fonts, icon_fn=lambda s, r, c: icon_chart(s, r, c))
    inner_x = rect.x + 18
    inner_w = rect.width - 36

    if state["mode"] == MODE_SONG:
        y = _draw_live_score(screen, fonts, inner_x, y, state)
        pygame.draw.line(screen, theme.PANEL_BORDER, (inner_x, y), (inner_x + inner_w, y), 1)
        y += 18

    _draw_best_scores_table(screen, fonts, inner_x, inner_w, y, state, songs)


def _draw_live_score(screen, fonts, x, y, state):
    score_surf = cached_text(fonts["score_big"], str(state["score"]), theme.TEXT_ACCENT)
    screen.blit(score_surf, (x, y))
    y += score_surf.get_height() + 4

    icon_flame(screen, (x + 9, y + 10), 16, theme.TEXT_DIM)
    combo_text = f"Combo x{state['combo']}"
    if state["misses"]:
        combo_text += f"   Fallos: {state['misses']}"
    screen.blit(cached_text(fonts["subtitle"], combo_text, theme.TEXT_DIM), (x + 22, y))
    y += 28

    if state["popup_text"] and pygame.time.get_ticks() < state["popup_until"]:
        color = state["popup_color"] or theme.TEXT_ACCENT
        popup_surf = cached_text(fonts["body_bold"], state["popup_text"], color)
        # Pequeno "pop" de aparicion: entra un poco mas grande y se
        # asienta a tamano normal, en vez de aparecer de golpe.
        elapsed_since_shown = 900 - (state["popup_until"] - pygame.time.get_ticks())
        if 0 <= elapsed_since_shown < POPUP_POP_MS:
            scale = 1.0 + 0.25 * (1 - elapsed_since_shown / POPUP_POP_MS)
            w, h = popup_surf.get_size()
            popup_surf = pygame.transform.smoothscale(popup_surf, (max(1, int(w * scale)), max(1, int(h * scale))))
        screen.blit(popup_surf, (x, y))
        y += popup_surf.get_height()

    return y + 12


def _draw_best_scores_table(screen, fonts, x, w, y, state, songs):
    header = cached_text(fonts["menu_meta"], "MEJORES DE LA SESION", theme.TEXT_DIM)
    screen.blit(header, (x, y))
    y += header.get_height() + 12

    best = state["session_best"]
    active_name = state["song_name"] if state["mode"] == MODE_SONG else None

    for name, _notes in songs:
        is_active = name == active_name
        row_h = 42

        if is_active:
            row_rect = pygame.Rect(x - 8, y - 4, w + 16, row_h - 4)
            pygame.draw.rect(screen, theme.PANEL_SELECTED_BG, row_rect, border_radius=6)

        short_name = name if len(name) <= 26 else name[:24] + "..."
        fg = theme.TEXT_PRIMARY if is_active else theme.TEXT_DIM
        name_surf = cached_text(fonts["menu_meta"], short_name, fg)
        screen.blit(name_surf, (x, y))

        entry = best.get(name)
        value_text = f"{entry['score']} pts - combo {entry['combo']}" if entry else "-"
        value_surf = cached_text(fonts["menu_meta"], value_text, theme.TEXT_ACCENT if entry else theme.TEXT_DIM)
        screen.blit(value_surf, (x, y + name_surf.get_height() + 2))

        y += row_h
        if y > screen.get_height() - 40:
            break
