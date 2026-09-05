"""
background.py - Fondo animado del piano
==========================================
Un degradado vertical fijo (se calcula una sola vez al arrancar, no
en cada frame, por rendimiento) mas un puñado de particulas suaves
que flotan hacia arriba como notas escapandose del teclado. Es
puramente decorativo: no afecta la logica del juego ni el modo
practica.
"""

import math
import random

import pygame

from theme import BG_TOP, BG_BOTTOM, PARTICLE_COLOR
from visuals import vertical_gradient


class _Particle:
    __slots__ = ("x", "y", "speed", "radius", "sway_phase", "sway_speed", "base_alpha")

    def __init__(self, width, height):
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.speed = random.uniform(8, 22)
        self.radius = random.uniform(2, 5)
        self.sway_phase = random.uniform(0, 2 * math.pi)
        self.sway_speed = random.uniform(0.4, 1.0)
        self.base_alpha = random.uniform(30, 90)

    def update(self, dt, width, height):
        self.y -= self.speed * dt
        self.sway_phase += self.sway_speed * dt
        if self.y < -10:
            self.y = height + 10
            self.x = random.uniform(0, width)


class AnimatedBackground:
    def __init__(self, width, height, particle_count=26):
        self.width = width
        self.height = height
        self.gradient = vertical_gradient((width, height), BG_TOP, BG_BOTTOM)
        self.particles = [_Particle(width, height) for _ in range(particle_count)]
        self._glow_cache = {}

    def _glow_surface(self, radius, alpha):
        radius = max(1, int(radius))
        bucket = max(0, min(255, int(alpha // 15) * 15))
        key = (radius, bucket)
        cached = self._glow_cache.get(key)
        if cached is None:
            cached = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(cached, (*PARTICLE_COLOR, bucket), (radius, radius), radius)
            self._glow_cache[key] = cached
        return cached

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.gradient, (0, 0))
        for particle in self.particles:
            sway = math.sin(particle.sway_phase) * 14
            twinkle = 0.6 + 0.4 * abs(math.sin(particle.sway_phase * 1.7))
            glow = self._glow_surface(particle.radius, particle.base_alpha * twinkle)
            screen.blit(glow, (particle.x + sway - particle.radius, particle.y - particle.radius))
