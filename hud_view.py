"""
hud_view.py - Cabecera con titulo, instrucciones y progreso de la cancion
=============================================================================
Todo lo que se dibuja ARRIBA del piano (dentro del "escenario" central,
entre los dos paneles laterales) cuando estas en modo libre o
practicando una cancion. Sigue la jerarquia cancion -> nota actual ->
piano: el nombre de la cancion se destaca, la instruccion de la nota
actual va justo debajo con una barra de progreso bien visible, y las
proximas teclas fisicas se listan como chips justo encima del piano.

El puntaje/combo en vivo y el popup de feedback (+15, -5...) viven en
side_panels.py (panel derecho), no aqui, para no competir por espacio
con el titulo. El menu de seleccion de canciones tiene su propio
archivo (menu_view.py) porque ocupa toda la pantalla en vez de solo
la cabecera.
"""

import pygame

import theme
from config import STAGE_X, STAGE_WIDTH, MODE_SONG, OFFSET_TO_LABEL
from music_theory import label_for_absolute_midi, note_name_for_offset, needed_base_for_midi
from visuals import render_text_with_shadow, rounded_rect_vertical_gradient, soft_glow, icon_note, cached_text


def draw_hud(screen, fonts, state):
    icon_note(screen, (STAGE_X + 12, 30), 26, theme.TEXT_ACCENT)
    render_text_with_shadow(
        screen, fonts["title"], "Piano de escritorio",
        theme.TEXT_PRIMARY, (STAGE_X + 32, 14),
    )

    octave_info = (
        f"Octava base: {note_name_for_offset(0, state['base_midi'])} | "
        f"Tempo: {state['bpm']} BPM (+/-) | F11: pantalla completa"
    )
    screen.blit(cached_text(fonts["subtitle"], octave_info, theme.TEXT_DIM), (STAGE_X, 58))

    if state["message"] and pygame.time.get_ticks() < state["message_until"]:
        screen.blit(cached_text(fonts["body_bold"], state["message"], theme.TARGET_GLOW),
                    (STAGE_X, 96))
        return

    if state["mode"] == MODE_SONG:
        _draw_song_progress(screen, fonts, state)
    else:
        hint = ("Flechas arriba/abajo: octava (C1-C5) | P: practicar canciones | "
                "F11: pantalla completa | ESC: salir")
        screen.blit(cached_text(fonts["subtitle"], hint, theme.TEXT_DIM), (STAGE_X, 96))


def _draw_song_progress(screen, fonts, state):
    base_midi = state["base_midi"]
    name = state["song_name"]
    midis = state["song_midis"]
    durations = state["song_durations"]
    idx = state["song_index"]

    # Jerarquia: etiqueta pequena arriba, nombre de la cancion grande
    # debajo -- es lo primero que el ojo debe encontrar en esta zona.
    screen.blit(cached_text(fonts["menu_meta"], "PRACTICANDO", theme.TEXT_DIM), (STAGE_X, 92))
    title_surf = cached_text(fonts["menu_title"], name, theme.TEXT_PRIMARY)
    screen.blit(title_surf, (STAGE_X, 110))
    counter = cached_text(fonts["subtitle"], f"nota {min(idx + 1, len(midis))}/{len(midis)}", theme.TEXT_DIM)
    screen.blit(counter, (STAGE_X + title_surf.get_width() + 14, 110 + title_surf.get_height() - counter.get_height()))

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
            screen.blit(cached_text(fonts["body"], warn, theme.WARN_GLOW), (STAGE_X, 144))
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
            screen.blit(cached_text(fonts["body"], hold_text, theme.TEXT_PRIMARY), (STAGE_X, 144))
            _draw_progress_bar(screen, STAGE_X, 174, min(440, STAGE_WIDTH - 40), 20, fraction)

    _draw_upcoming_chips(screen, fonts, midis, idx, base_midi)


def _draw_progress_bar(screen, x, y, w, h, fraction):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, theme.PROGRESS_BG, rect, border_radius=h // 2)
    if fraction > 0:
        fill_w = max(h, int(w * fraction))
        fill_rect = pygame.Rect(x, y, fill_w, h)
        bot_c = tuple(max(0, c - 60) for c in theme.TARGET_GLOW)
        rounded_rect_vertical_gradient(screen, fill_rect, theme.TARGET_GLOW, bot_c, radius=h // 2)
        # Brillo puntual: solo aparece cuando la nota esta a punto de
        # completarse, no todo el tiempo que se sostiene la tecla.
        if fraction >= 0.85:
            soft_glow(screen, (fill_rect.right - h // 2, fill_rect.centery), radius=int(h * 1.3),
                      color=theme.TARGET_GLOW, max_alpha=90)
    pygame.draw.rect(screen, theme.PANEL_BORDER, rect, width=1, border_radius=h // 2)


def _draw_upcoming_chips(screen, fonts, midis, idx, base_midi):
    upcoming = midis[idx:idx + 10]
    x = STAGE_X
    y = 208
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

        chip = cached_text(fonts["chip"], label, fg)
        pad = 7
        w, h = chip.get_size()
        rect = pygame.Rect(x, y, w + pad * 2, h + pad * 2)
        pygame.draw.rect(screen, bg, rect, border_radius=8)
        pygame.draw.rect(screen, theme.PANEL_BORDER, rect, width=1, border_radius=8)
        screen.blit(chip, (x + pad, y + pad))
        x += w + pad * 2 + 8
