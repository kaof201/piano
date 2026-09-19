"""
visuals.py - Utilidades genericas de dibujo (degradados, brillos, sombras)
=============================================================================
Funciones de bajo nivel que no saben nada de piano, canciones ni
menus: solo saben pintar pixeles bonitos sobre una Surface de pygame.
piano_view.py, menu_view.py, hud_view.py, side_panels.py y
background.py se apoyan en estas para no repetir codigo de "como se
ve un degradado" en cada archivo.

RENDIMIENTO: la mayoria de estas formas (el degradado de una tecla,
su sombra, el texto de una etiqueta) son IDENTICAS de un frame al
siguiente -- solo cambian cuando cambia de verdad el color, el
tamano o el texto (por ejemplo, al presionar una tecla). Dibujarlas
de cero 60 veces por segundo es trabajo desperdiciado, asi que las
funciones de aqui abajo cachean la Surface ya dibujada la primera
vez que ven una combinacion de parametros, y despues solo hacen un
blit (que es barato) en vez de volver a calcular pixel por pixel.
Los cachés son chicos porque el numero de combinaciones reales
(un puñado de tamaños de tecla x un puñado de colores) es chico.
"""

import numpy as np
import pygame

_gradient_cache = {}
_shadow_cache = {}
_glow_cache = {}
_text_cache = {}
_TEXT_CACHE_LIMIT = 400  # de sobra para una sesion normal; ver cached_text()


def vertical_gradient(size, color_top, color_bottom):
    """Crea una Surface del tamano dado con un degradado vertical.
    Usa numpy para calcular las filas de una sola vez en vez de un
    bucle de Python con pygame.draw.line por fila."""
    width, height = size
    if height <= 1 or width <= 0:
        surface = pygame.Surface((max(1, width), max(1, height)))
        surface.fill(color_top)
        return surface

    t = np.linspace(0.0, 1.0, height, dtype=np.float32).reshape(height, 1)
    top = np.array(color_top, dtype=np.float32)
    bottom = np.array(color_bottom, dtype=np.float32)
    rows = (top + (bottom - top) * t).astype(np.uint8)          # (height, 3)
    pixels = np.repeat(rows[:, np.newaxis, :], width, axis=1)    # (height, width, 3)
    pixels = np.transpose(pixels, (1, 0, 2))                     # pygame quiere (width, height, 3)
    return pygame.surfarray.make_surface(np.ascontiguousarray(pixels))


def _build_gradient_rect(width, height, color_top, color_bottom, radius):
    grad = vertical_gradient((width, height), color_top, color_bottom).convert_alpha()
    mask = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)
    grad.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return grad


def rounded_rect_vertical_gradient(surface, rect, color_top, color_bottom, radius):
    """Dibuja un rectangulo redondeado relleno con degradado vertical.
    La Surface real se construye una sola vez por combinacion de
    (tamano, colores, radio) y se reutiliza despues -- por eso esto
    es seguro de llamar todos los frames para las mismas teclas."""
    if rect.width <= 0 or rect.height <= 0:
        return
    key = (rect.width, rect.height, color_top, color_bottom, radius)
    cached = _gradient_cache.get(key)
    if cached is None:
        cached = _build_gradient_rect(rect.width, rect.height, color_top, color_bottom, radius)
        _gradient_cache[key] = cached
    surface.blit(cached, rect.topleft)


def _build_glow(radius, color, layers, max_alpha):
    glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for i in range(layers, 0, -1):
        alpha = int(max_alpha * (i / layers) ** 2)
        r = max(1, int(radius * (i / layers)))
        pygame.draw.circle(glow, (*color, alpha), (radius, radius), r)
    return glow


def soft_glow(surface, center, radius, color, layers=5, max_alpha=110):
    """Dibuja un halo suave (varios circulos translucidos concentricos)
    centrado en 'center'. Se usa solo para destellos puntuales
    (acierto/fallo, barra de progreso casi completa), asi que el
    cache aqui es un extra, no el ahorro principal."""
    radius = int(radius)
    if radius <= 0:
        return
    key = (radius, color, layers, max_alpha)
    glow = _glow_cache.get(key)
    if glow is None:
        glow = _build_glow(radius, color, layers, max_alpha)
        if len(_glow_cache) > 200:
            _glow_cache.clear()
        _glow_cache[key] = glow
    surface.blit(glow, (center[0] - radius, center[1] - radius), special_flags=pygame.BLEND_RGBA_ADD)


def _build_shadow(width, height, radius, alpha, blur_margin):
    shadow = pygame.Surface((width + blur_margin * 2, height + blur_margin * 2), pygame.SRCALPHA)
    base_rect = pygame.Rect(blur_margin, blur_margin, width, height)
    pygame.draw.rect(shadow, (0, 0, 0, alpha), base_rect, border_radius=radius)
    for step in range(1, blur_margin + 1, 2):
        fade_alpha = int(alpha * (1 - step / blur_margin) * 0.5)
        if fade_alpha <= 0:
            continue
        pygame.draw.rect(
            shadow, (0, 0, 0, fade_alpha), base_rect.inflate(step * 2, step * 2),
            border_radius=radius + step, width=step,
        )
    return shadow


def drop_shadow_rect(surface, rect, radius, offset=(0, 6), alpha=90, blur_margin=8):
    """Sombra suave debajo de un rectangulo redondeado. Igual que el
    degradado de arriba: la forma se construye una vez por (tamano,
    radio, alpha, margen) y se reutiliza -- la posicion (que si
    cambia por tecla) solo se aplica al hacer el blit final."""
    key = (rect.width, rect.height, radius, alpha, blur_margin)
    shadow = _shadow_cache.get(key)
    if shadow is None:
        shadow = _build_shadow(rect.width, rect.height, radius, alpha, blur_margin)
        _shadow_cache[key] = shadow
    surface.blit(shadow, (rect.x - blur_margin + offset[0], rect.y - blur_margin + offset[1]))


def cached_text(font, text, color):
    """Igual que font.render(), pero recordando el resultado. La
    gran mayoria del texto en esta app (letras de teclas, titulos de
    canciones, etiquetas fijas) es identico frame a frame; solo unos
    pocos textos cambian seguido (el puntaje, el contador de notas).
    Si el cache crece demasiado (una sesion muy larga generando
    muchos numeros de puntaje distintos) simplemente se vacia --
    volver a renderizar unos textos de vez en cuando no cuesta nada,
    lo caro era hacerlo EN CADA FRAME."""
    key = (id(font), text, color)
    surf = _text_cache.get(key)
    if surf is None:
        surf = font.render(text, True, color)
        if len(_text_cache) > _TEXT_CACHE_LIMIT:
            _text_cache.clear()
        _text_cache[key] = surf
    return surf


def render_text_with_shadow(surface, font, text, color, pos, shadow_color=(0, 0, 0, 140), shadow_offset=(2, 2)):
    shadow = cached_text(font, text, shadow_color[:3])
    surface.blit(shadow, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))
    label = cached_text(font, text, color)
    surface.blit(label, pos)
    return label.get_size()


# ------------------------------------------------------------------
# Iconos pequenos dibujados a mano (lineas/formas de pygame), en vez
# de depender de glifos de emoji que pueden no existir en la fuente
# del sistema. Cada uno se dibuja centrado en 'center', a un tamano
# aproximado de 'size' pixeles. Son baratos (pocas formas, superficies
# chicas) asi que no hace falta cachearlos como los degradados.
# ------------------------------------------------------------------
def icon_note(surface, center, size, color):
    """Una corchea sencilla: cabeza + plica + banderin."""
    cx, cy = center
    r = max(3, size * 0.16)
    head_x, head_y = cx - size * 0.22, cy + size * 0.28
    pygame.draw.circle(surface, color, (int(head_x), int(head_y)), int(r))
    stem_top = (head_x + r * 0.9, head_y - size * 0.55)
    stem_bottom = (head_x + r * 0.9, head_y)
    pygame.draw.line(surface, color, stem_bottom, stem_top, max(2, int(size * 0.1)))
    flag = [stem_top, (stem_top[0] + size * 0.32, stem_top[1] + size * 0.16),
            (stem_top[0] + size * 0.05, stem_top[1] + size * 0.38)]
    pygame.draw.polygon(surface, color, flag)


def icon_chart(surface, rect, color):
    """Tres barras de altura creciente, tipo grafico de progreso."""
    bar_w = max(3, rect.width // 5)
    gap = max(2, bar_w // 2)
    heights = [0.45, 0.7, 1.0]
    total_w = bar_w * 3 + gap * 2
    x = rect.centerx - total_w // 2
    base_y = rect.bottom
    for h in heights:
        bar_h = int(rect.height * h)
        bar_rect = pygame.Rect(x, base_y - bar_h, bar_w, bar_h)
        pygame.draw.rect(surface, color, bar_rect, border_radius=2)
        x += bar_w + gap


def icon_flame(surface, center, size, color):
    """Una llama simplificada (para el combo), como un poligono suave."""
    cx, cy = center
    points = [
        (cx, cy - size * 0.55),
        (cx + size * 0.28, cy - size * 0.05),
        (cx + size * 0.18, cy + size * 0.45),
        (cx, cy + size * 0.55),
        (cx - size * 0.18, cy + size * 0.45),
        (cx - size * 0.28, cy - size * 0.05),
    ]
    pygame.draw.polygon(surface, color, points)


def icon_mic(surface, center, size, color):
    """Un microfono sencillo (letra + soporte), para la seccion de letra."""
    cx, cy = center
    body = pygame.Rect(0, 0, size * 0.34, size * 0.6)
    body.center = (cx, cy - size * 0.05)
    pygame.draw.rect(surface, color, body, border_radius=int(size * 0.17))
    pygame.draw.arc(
        surface, color,
        pygame.Rect(cx - size * 0.32, cy - size * 0.15, size * 0.64, size * 0.55),
        3.4, 6.0, max(2, int(size * 0.08)),
    )
    pygame.draw.line(surface, color, (cx, cy + size * 0.28), (cx, cy + size * 0.45), max(2, int(size * 0.08)))
    pygame.draw.line(surface, color, (cx - size * 0.16, cy + size * 0.45), (cx + size * 0.16, cy + size * 0.45),
                      max(2, int(size * 0.08)))


def icon_target(surface, center, size, color):
    """Circulos concentricos tipo diana, para precision/progreso."""
    cx, cy = int(center[0]), int(center[1])
    pygame.draw.circle(surface, color, (cx, cy), int(size * 0.5), width=max(2, int(size * 0.09)))
    pygame.draw.circle(surface, color, (cx, cy), int(size * 0.22))


def icon_falling_notes(surface, rect, color):
    """Dos barras cayendo hacia una linea, para el riel de proximas notas."""
    bar_w = max(4, rect.width // 4)
    x1 = rect.centerx - bar_w - 2
    x2 = rect.centerx + 2
    pygame.draw.rect(surface, color, pygame.Rect(x1, rect.y, bar_w, int(rect.height * 0.55)), border_radius=2)
    pygame.draw.rect(surface, color, pygame.Rect(x2, rect.y + int(rect.height * 0.3), bar_w, int(rect.height * 0.7)),
                      border_radius=2)
    pygame.draw.line(surface, color, (rect.x, rect.bottom), (rect.right, rect.bottom), 2)
