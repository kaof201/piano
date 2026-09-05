"""
visuals.py - Utilidades genericas de dibujo (degradados, brillos, sombras)
=============================================================================
Funciones de bajo nivel que no saben nada de piano, canciones ni
menus: solo saben pintar pixeles bonitos sobre una Surface de pygame.
piano_view.py, menu_view.py, hud_view.py y background.py se apoyan en
estas para no repetir codigo de "como se ve un degradado" en cada
archivo.
"""

import pygame


def vertical_gradient(size, color_top, color_bottom):
    """Crea una Surface del tamano dado con un degradado vertical."""
    width, height = size
    surface = pygame.Surface(size)
    if height <= 1:
        surface.fill(color_top)
        return surface
    for y in range(height):
        t = y / (height - 1)
        color = tuple(
            int(color_top[i] + (color_bottom[i] - color_top[i]) * t)
            for i in range(3)
        )
        pygame.draw.line(surface, color, (0, y), (width, y))
    return surface


def rounded_rect_vertical_gradient(surface, rect, color_top, color_bottom, radius):
    """Dibuja un rectangulo redondeado relleno con degradado vertical,
    recortado a la forma redondeada usando una mascara de alpha."""
    if rect.width <= 0 or rect.height <= 0:
        return
    grad = vertical_gradient((rect.width, rect.height), color_top, color_bottom).convert_alpha()
    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)
    grad.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surface.blit(grad, rect.topleft)


def soft_glow(surface, center, radius, color, layers=5, max_alpha=110):
    """Dibuja un halo suave (varios circulos translucidos concentricos)
    centrado en 'center'. Se usa para resaltar teclas objetivo y
    tarjetas seleccionadas sin depender de shaders."""
    if radius <= 0:
        return
    glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for i in range(layers, 0, -1):
        alpha = int(max_alpha * (i / layers) ** 2)
        r = max(1, int(radius * (i / layers)))
        pygame.draw.circle(glow, (*color, alpha), (radius, radius), r)
    surface.blit(glow, (center[0] - radius, center[1] - radius), special_flags=pygame.BLEND_RGBA_ADD)


def drop_shadow_rect(surface, rect, radius, offset=(0, 6), alpha=90, blur_margin=8):
    """Sombra suave debajo de un rectangulo redondeado: una capa base
    solida mas unos anillos expandidos y translucidos para simular
    desenfoque sin depender de librerias externas de blur."""
    shadow = pygame.Surface((rect.width + blur_margin * 2, rect.height + blur_margin * 2), pygame.SRCALPHA)
    base_rect = pygame.Rect(blur_margin, blur_margin, rect.width, rect.height)
    pygame.draw.rect(shadow, (0, 0, 0, alpha), base_rect, border_radius=radius)
    for step in range(1, blur_margin + 1, 2):
        fade_alpha = int(alpha * (1 - step / blur_margin) * 0.5)
        if fade_alpha <= 0:
            continue
        pygame.draw.rect(
            shadow, (0, 0, 0, fade_alpha), base_rect.inflate(step * 2, step * 2),
            border_radius=radius + step, width=step,
        )
    surface.blit(shadow, (rect.x - blur_margin + offset[0], rect.y - blur_margin + offset[1]))


def render_text_with_shadow(surface, font, text, color, pos, shadow_color=(0, 0, 0, 140), shadow_offset=(2, 2)):
    shadow = font.render(text, True, shadow_color[:3])
    surface.blit(shadow, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))
    label = font.render(text, True, color)
    surface.blit(label, pos)
    return label.get_size()
