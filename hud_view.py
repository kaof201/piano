"""
hud_view.py - Cabecera con titulo, instrucciones y progreso de la cancion
=============================================================================
Todo lo que se dibuja ARRIBA del piano cuando estas en modo libre o
practicando una cancion: titulo, linea de estado, y en modo practica
la barra de progreso de la nota actual + la tira de proximas notas.

El menu de seleccion de canciones tiene su propio archivo
(menu_view.py) porque ocupa toda la pantalla en vez de solo la
cabecera.
"""

import pygame

import theme
from config import SIDE_MARGIN, MODE_SONG, OFFSET_TO_LABEL
from music_theory import label_for_absolute_midi, note_name_for_offset, needed_base_for_midi
from visuals import render_text_with_shadow, rounded_rect_vertical_gradient


def draw_hud(screen, fonts, state):
    render_text_with_shadow(
        screen, fonts["title"], "Piano de escritorio",
        theme.TEXT_PRIMARY, (SIDE_MARGIN, 14),
    )

    octave_info = (
        f"Octava base: {note_name_for_offset(0, state['base_midi'])}   |   "
        f"Tempo: {state['bpm']} BPM (+/-)   |   F11: pantalla completa"
    )
    screen.blit(fonts["subtitle"].render(octave_info, True, theme.TEXT_DIM), (SIDE_MARGIN, 58))

    if state["message"] and pygame.time.get_ticks() < state["message_until"]:
        screen.blit(fonts["body_bold"].render(state["message"], True, theme.TARGET_GLOW),
                    (SIDE_MARGIN, 92))
        return

    if state["mode"] == MODE_SONG:
        _draw_song_progress(screen, fonts, state)
    else:
        hint = ("Flechas arriba/abajo: octava (C1-C5)   |   P: practicar canciones   |   "
                "F11: pantalla completa   |   ESC: salir")
        screen.blit(fonts["subtitle"].render(hint, True, theme.TEXT_DIM), (SIDE_MARGIN, 96))


def _draw_song_progress(screen, fonts, state):
    base_midi = state["base_midi"]
    name = state["song_name"]
    midis = state["song_midis"]
    durations = state["song_durations"]
    idx = state["song_index"]

    progress = f"Practicando: {name}   (nota {min(idx + 1, len(midis))}/{len(midis)})"
    screen.blit(fonts["body_bold"].render(progress, True, theme.TEXT_PRIMARY), (SIDE_MARGIN, 92))

    if idx < len(midis):
        target_midi = midis[idx]
        target_offset_view = target_midi - base_midi
        in_view = 0 <= target_offset_view <= 24

        if not in_view:
            # Respaldo visual: en la practica normal el programa ya salta
            # de octava solo, esto no deberia llegar a verse.
            needed_base = needed_base_for_midi(target_midi, base_midi)
            needed_name = note_name_for_offset(0, needed_base)
            warn = f"Cambiando de octava automaticamente a {needed_name}..."
            screen.blit(fonts["body"].render(warn, True, theme.WARN_GLOW), (SIDE_MARGIN, 118))
        else:
            seconds_per_beat = 60.0 / state["bpm"]
            required = durations[idx] * seconds_per_beat
            if state["holding_offset"] == target_offset_view:
                elapsed = (pygame.time.get_ticks() - state["hold_start"]) / 1000.0
            else:
                elapsed = 0.0
            fraction = min(1.0, elapsed / required) if required > 0 else 1.0

            key_label = OFFSET_TO_LABEL[target_offset_view]
            hold_text = f"Manten presionada la tecla {key_label} durante ~{required:.2f}s"
            screen.blit(fonts["body"].render(hold_text, True, theme.TEXT_PRIMARY), (SIDE_MARGIN, 118))

            _draw_progress_bar(screen, SIDE_MARGIN, 146, 320, 16, fraction)

    _draw_upcoming_chips(screen, fonts, midis, idx, base_midi)


def _draw_progress_bar(screen, x, y, w, h, fraction):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, theme.PROGRESS_BG, rect, border_radius=h // 2)
    if fraction > 0:
        fill_w = max(h, int(w * fraction))
        fill_rect = pygame.Rect(x, y, fill_w, h)
        bot_c = tuple(max(0, c - 60) for c in theme.TARGET_GLOW)
        rounded_rect_vertical_gradient(screen, fill_rect, theme.TARGET_GLOW, bot_c, radius=h // 2)


def _draw_upcoming_chips(screen, fonts, midis, idx, base_midi):
    upcoming = midis[idx:idx + 10]
    x = SIDE_MARGIN
    y = 178
    for i, midi in enumerate(upcoming):
        label, in_view = label_for_absolute_midi(midi, base_midi)
        if i == 0:
            bg = theme.TARGET_GLOW if in_view else theme.WARN_GLOW
            fg = (18, 18, 20)
        elif i == 1:
            bg = theme.NEXT_GLOW if in_view else (80, 80, 90)
            fg = (255, 255, 255) if in_view else theme.TEXT_PRIMARY
        else:
            bg = theme.PANEL_BG
            fg = theme.TEXT_PRIMARY
        chip = fonts["chip"].render(label, True, fg)
        pad = 7
        w, h = chip.get_size()
        rect = pygame.Rect(x, y, w + pad * 2, h + pad * 2)
        pygame.draw.rect(screen, bg, rect, border_radius=8)
        pygame.draw.rect(screen, theme.PANEL_BORDER, rect, width=1, border_radius=8)
        screen.blit(chip, (x + pad, y + pad))
        x += w + pad * 2 + 8
