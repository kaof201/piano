"""
audio.py - Generacion y carga de sonido
==========================================
Dos formas de conseguir el sonido de cada tecla:

  1. Samples reales: si existe una carpeta "samples/" junto al
     programa con archivos .wav nombrados como la nota (C3.wav,
     Cs3.wav, D3.wav... la 's' es sostenido/sharp), se usan esos.
  2. Sintesis: si falta el archivo de una nota, se genera un tono
     con timbre de piano (varios armonicos + caida exponencial).

load_sounds() se llama cada vez que cambias de octava (flechas
arriba/abajo) o arrancas una cancion, porque las 25 teclas visibles
corresponden a MIDI distintos y hay que regenerar/recargar los 25
sonidos.
"""

import os

import numpy as np
import pygame

from config import SAMPLE_RATE
from music_theory import midi_to_freq, note_name_for_offset


def synth_piano_tone(freq, duration=2.0):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    harmonics = [1.0, 0.55, 0.30, 0.18, 0.10, 0.06]
    wave = np.zeros_like(t)
    for i, amp in enumerate(harmonics, start=1):
        wave += amp * np.sin(2 * np.pi * freq * i * t)

    attack_len = int(SAMPLE_RATE * 0.005)
    envelope = np.exp(-t * 3.0)
    if attack_len > 0:
        envelope[:attack_len] *= np.linspace(0, 1, attack_len)

    wave = wave * envelope
    wave = wave / np.max(np.abs(wave) + 1e-9)
    wave = (wave * 32767 * 0.6).astype(np.int16)
    stereo = np.column_stack([wave, wave])
    return pygame.sndarray.make_sound(np.ascontiguousarray(stereo))


def load_sounds(base_midi):
    samples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")
    sounds = {}
    loaded_from_file = 0
    sinteticas = []

    for offset in range(25):
        midi = base_midi + offset
        name = note_name_for_offset(offset, base_midi)
        wav_path = os.path.join(samples_dir, f"{name}.wav")

        if os.path.isfile(wav_path):
            sounds[offset] = pygame.mixer.Sound(wav_path)
            loaded_from_file += 1
        else:
            sounds[offset] = synth_piano_tone(midi_to_freq(midi))
            sinteticas.append(name)

    octava_nombre = note_name_for_offset(0, base_midi)
    if sinteticas:
        print(f"[{octava_nombre}] {loaded_from_file}/25 reales. "
              f"Sinteticas: {', '.join(sinteticas)}")
    else:
        print(f"[{octava_nombre}] 25/25 notas reales cargadas. OK")

    return sounds, loaded_from_file
