"""
piano_view.py - Dibujo de las teclas del piano (las 2 filas apiladas)
=========================================================================
Sabe como se ve una tecla: blanca o negra, en reposo, presionada, o
marcada como "toca esto ahora" / "esto sigue" durante el modo
practica. No sabe nada de audio, canciones ni del bucle principal:
solo recibe el estado ya resuelto (que offsets estan activos, cual es
el objetivo y cual el siguiente) y pinta.
"""

import pygame

import theme
from config import (
    ROW_LOW, ROW_HIGH, TOP_MARGIN, WHITE_KEY_H, ROW_GAP,
    WHITE_KEY_W, BLACK_KEY_W, BLACK_KEY_H, SIDE_MARGIN, WIDTH,
    OFFSET_TO_LABEL, PRESS_DIP, MODE_SONG,
)
from visuals import rounded_rect_vertical_gradient, drop_shadow_rect, soft_glow


def _row_start_x(row_layout):
    n_whites = sum(1 for _, black in row_layout if not black)
    row_width = n_whites * WHITE_KEY_W
    return SIDE_MARGIN + (WIDTH - 2 * SIDE_MARGIN - row_width) // 2


def _draw_white_keys(screen, label_font, row_layout, y_top, start_x, active_offsets, target_offset, next_offset):
    white_positions = {}

    # Sombras primero, para que ninguna tecla tape el brillo de otra.
    x = start_x
    for offset, is_black in row_layout:
        if is_black:
            continue
        rect = pygame.Rect(x, y_top, WHITE_KEY_W - 3, WHITE_KEY_H)
        drop_shadow_rect(screen, rect, radius=10, offset=(0, 8), alpha=110)
        white_positions[offset] = x
        x += WHITE_KEY_W

    x = start_x
    for offset, is_black in row_layout:
        if is_black:
            continue
        active = offset in active_offsets
        dip = PRESS_DIP if active else 0
        rect = pygame.Rect(x, y_top + dip, WHITE_KEY_W - 3, WHITE_KEY_H - dip)

        top_c = theme.WHITE_ACTIVE_TOP if active else theme.WHITE_TOP
        bot_c = theme.WHITE_ACTIVE_BOTTOM if active else theme.WHITE_BOTTOM
        rounded_rect_vertical_gradient(screen, rect, top_c, bot_c, radius=10)
        pygame.draw.rect(screen, theme.WHITE_BORDER, rect, width=2, border_radius=10)

        if offset == target_offset:
            soft_glow(screen, rect.center, radius=int(WHITE_KEY_W * 0.62), color=theme.TARGET_GLOW, max_alpha=95)
            pygame.draw.rect(screen, theme.TARGET_GLOW, rect, width=5, border_radius=10)
        elif offset == next_offset:
            soft_glow(screen, rect.center, radius=int(WHITE_KEY_W * 0.55), color=theme.NEXT_GLOW, max_alpha=85)
            pygame.draw.rect(screen, theme.NEXT_GLOW, rect, width=4, border_radius=10)

        label = OFFSET_TO_LABEL[offset]
        text = label_font.render(label, True, theme.KEY_LABEL_DARK)
        tw, th = text.get_size()
        screen.blit(text, (x + (WHITE_KEY_W - 3 - tw) // 2, rect.bottom - th - 16))
        x += WHITE_KEY_W

    return white_positions


def _draw_black_keys(screen, label_font, row_layout, y_top, start_x, white_positions, active_offsets, target_offset, next_offset):
    for offset, is_black in row_layout:
        if not is_black:
            continue
        prev_white = offset - 1
        base_x = white_positions.get(prev_white, start_x)
        bx = base_x + WHITE_KEY_W - BLACK_KEY_W // 2

        active = offset in active_offsets
        dip = PRESS_DIP if active else 0
        rect = pygame.Rect(bx, y_top + dip, BLACK_KEY_W, BLACK_KEY_H - dip)

        drop_shadow_rect(screen, rect, radius=8, offset=(0, 6), alpha=140)
        top_c = theme.BLACK_ACTIVE_TOP if active else theme.BLACK_TOP
        bot_c = theme.BLACK_ACTIVE_BOTTOM if active else theme.BLACK_BOTTOM
        rounded_rect_vertical_gradient(screen, rect, top_c, bot_c, radius=8)

        # Brillo superior, como en una tecla negra de piano real.
        gloss = pygame.Rect(rect.x + 6, rect.y + 4, max(0, rect.width - 12), 9)
        pygame.draw.rect(screen, theme.BLACK_GLOSS, gloss, border_radius=5)

        if offset == target_offset:
            soft_glow(screen, rect.center, radius=int(BLACK_KEY_W * 1.0), color=theme.TARGET_GLOW, max_alpha=95)
            pygame.draw.rect(screen, theme.TARGET_GLOW, rect, width=4, border_radius=8)
        elif offset == next_offset:
            soft_glow(screen, rect.center, radius=int(BLACK_KEY_W * 0.85), color=theme.NEXT_GLOW, max_alpha=85)
            pygame.draw.rect(screen, theme.NEXT_GLOW, rect, width=3, border_radius=8)

        label = OFFSET_TO_LABEL[offset]
        text = label_font.render(label, True, theme.KEY_LABEL_LIGHT)
        tw, th = text.get_size()
        screen.blit(text, (bx + (BLACK_KEY_W - tw) // 2, rect.bottom - th - 14))


def draw_key_row(screen, label_font, row_layout, y_top, active_offsets, target_offset, next_offset):
    start_x = _row_start_x(row_layout)
    white_positions = _draw_white_keys(screen, label_font, row_layout, y_top, start_x,
                                        active_offsets, target_offset, next_offset)
    _draw_black_keys(screen, label_font, row_layout, y_top, start_x, white_positions,
                      active_offsets, target_offset, next_offset)


def draw_piano(screen, label_font, active_offsets, state):
    target_offset = None
    next_offset = None
    if state["mode"] == MODE_SONG and state["song_midis"]:
        idx = state["song_index"]
        base_midi = state["base_midi"]
        if idx < len(state["song_midis"]):
            t_off = state["song_midis"][idx] - base_midi
            if 0 <= t_off <= 24:
                target_offset = t_off
        if idx + 1 < len(state["song_midis"]):
            n_off = state["song_midis"][idx + 1] - base_midi
            if 0 <= n_off <= 24:
                next_offset = n_off

    y_high = TOP_MARGIN
    y_low = TOP_MARGIN + WHITE_KEY_H + ROW_GAP

    draw_key_row(screen, label_font, ROW_HIGH, y_high, active_offsets, target_offset, next_offset)
    draw_key_row(screen, label_font, ROW_LOW, y_low, active_offsets, target_offset, next_offset)
