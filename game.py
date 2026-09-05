"""
game.py - Bucle principal y estado de la aplicacion
=======================================================
Aqui vive el "controlador": maneja eventos de teclado, actualiza el
estado (que tecla esta sonando, en que nota de la cancion vas, cuanto
llevas sosteniendola) y en cada frame le pide a los modulos de dibujo
(hud_view, piano_view, menu_view, background) que pinten su parte.

Ningun archivo de dibujo conoce el estado completo del juego a
proposito; game.py es el unico lugar donde hay que mirar si algo en
la logica del juego no se comporta como se espera.
"""

import sys

import pygame

import theme
from config import (
    SAMPLE_RATE, BASE_MIDI_DEFAULT, OCTAVE_SHIFT_RANGE, DEFAULT_BPM,
    BPM_MIN, BPM_MAX, BPM_STEP, HOLD_TOLERANCE, KEY_OFFSETS,
    NUM_KEYS, PLUS_KEYS, MINUS_KEYS, FULLSCREEN_KEYS,
    MENU_UP_KEYS, MENU_DOWN_KEYS, MENU_CONFIRM_KEYS,
    WIDTH, HEIGHT, MODE_FREE, MODE_MENU, MODE_SONG,
)
from audio import load_sounds
from music_theory import get_song_midis_and_durations, needed_base_for_midi
from songs import SONGS
from background import AnimatedBackground
from hud_view import draw_hud
from piano_view import draw_piano
from menu_view import draw_song_menu


class PianoApp:
    def __init__(self):
        pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)
        pygame.init()
        pygame.mixer.set_num_channels(32)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
        pygame.display.set_caption("Piano de escritorio")
        self.fonts = theme.load_fonts()
        self.clock = pygame.time.Clock()
        self.background = AnimatedBackground(WIDTH, HEIGHT)

        self.base_midi = BASE_MIDI_DEFAULT
        self.sounds, loaded_from_file = load_sounds(self.base_midi)
        if loaded_from_file:
            print(f"Se cargaron {loaded_from_file} samples reales desde samples/.")
        else:
            print("No se encontraron samples en samples/. Usando sonido sintetizado.")

        self.active_offsets = set()
        self.active_keys_down = set()

        self.state = {
            "mode": MODE_FREE,
            "base_midi": self.base_midi,
            "bpm": DEFAULT_BPM,
            "song_name": "",
            "song_midis": [],
            "song_durations": [],
            "song_index": 0,
            "holding_offset": None,
            "hold_start": 0,
            "note_start": 0,
            "message": "",
            "message_until": 0,
            "menu_selected": 0,
        }

    # ------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = self._handle_keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self._handle_keyup(event.key)

            self._update_song_progress()
            self.background.update(dt)
            self._draw()

        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------
    # Entrada
    # ------------------------------------------------------------
    def _handle_keydown(self, key):
        state = self.state

        if key == pygame.K_ESCAPE:
            return False

        if key in FULLSCREEN_KEYS:
            pygame.display.toggle_fullscreen()
            return True

        if key == pygame.K_p:
            if state["mode"] == MODE_FREE:
                state["mode"] = MODE_MENU
                state["menu_selected"] = 0
            else:
                state["mode"] = MODE_FREE
                state["holding_offset"] = None
            return True

        if key in PLUS_KEYS:
            state["bpm"] = min(BPM_MAX, state["bpm"] + BPM_STEP)
            return True

        if key in MINUS_KEYS:
            state["bpm"] = max(BPM_MIN, state["bpm"] - BPM_STEP)
            return True

        if state["mode"] == MODE_MENU:
            self._handle_menu_keydown(key)
            return True

        if key == pygame.K_UP:
            self._shift_octave(12)
            return True
        if key == pygame.K_DOWN:
            self._shift_octave(-12)
            return True

        if key in KEY_OFFSETS and key not in self.active_keys_down:
            self._press_piano_key(key)
            return True

        return True

    def _handle_menu_keydown(self, key):
        state = self.state
        song_count = len(SONGS)
        if song_count == 0:
            return

        if key in MENU_UP_KEYS:
            state["menu_selected"] = (state["menu_selected"] - 1) % song_count
        elif key in MENU_DOWN_KEYS:
            state["menu_selected"] = (state["menu_selected"] + 1) % song_count
        elif key in MENU_CONFIRM_KEYS:
            self._start_song(state["menu_selected"])
        elif key in NUM_KEYS:
            idx = NUM_KEYS.index(key)
            if idx < song_count:
                state["menu_selected"] = idx
                self._start_song(idx)

    def _handle_keyup(self, key):
        if key not in KEY_OFFSETS:
            return
        self.active_keys_down.discard(key)
        offset = KEY_OFFSETS[key]
        self.active_offsets.discard(offset)

        state = self.state
        if state["mode"] == MODE_SONG and state["holding_offset"] == offset:
            state["holding_offset"] = None

    # ------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------
    def _shift_octave(self, semitones):
        new_base = self.base_midi + semitones
        low, high = OCTAVE_SHIFT_RANGE
        if BASE_MIDI_DEFAULT + low <= new_base <= BASE_MIDI_DEFAULT + high:
            self.base_midi = new_base
            self.state["base_midi"] = new_base
            self.sounds, _ = load_sounds(new_base)

    def _press_piano_key(self, key):
        self.active_keys_down.add(key)
        offset = KEY_OFFSETS[key]
        self.active_offsets.add(offset)
        self.sounds[offset].play()

        state = self.state
        if state["mode"] == MODE_SONG and state["song_midis"]:
            idx = state["song_index"]
            if idx < len(state["song_midis"]):
                target_offset_view = state["song_midis"][idx] - self.base_midi
                if 0 <= target_offset_view <= 24 and offset == target_offset_view:
                    state["holding_offset"] = offset
                    state["hold_start"] = pygame.time.get_ticks()

    def _start_song(self, idx):
        name, notes = SONGS[idx]
        midis, durations = get_song_midis_and_durations(notes)
        state = self.state
        state["song_name"] = name
        state["song_midis"] = midis
        state["song_durations"] = durations
        state["song_index"] = 0
        state["holding_offset"] = None
        state["note_start"] = pygame.time.get_ticks()
        state["mode"] = MODE_SONG

        if midis:
            needed = needed_base_for_midi(midis[0], self.base_midi)
            if needed != self.base_midi:
                self.base_midi = needed
                state["base_midi"] = needed
                self.sounds, _ = load_sounds(needed)

    # ------------------------------------------------------------
    # Actualizacion por frame
    # ------------------------------------------------------------
    def _update_song_progress(self):
        state = self.state
        if state["mode"] != MODE_SONG or state["holding_offset"] is None:
            return

        idx = state["song_index"]
        if idx >= len(state["song_midis"]):
            return

        target_offset_view = state["song_midis"][idx] - self.base_midi
        if state["holding_offset"] != target_offset_view:
            # La octava cambio mientras sostenia (o algo quedo desincronizado).
            state["holding_offset"] = None
            return

        seconds_per_beat = 60.0 / state["bpm"]
        required = state["song_durations"][idx] * seconds_per_beat
        elapsed = (pygame.time.get_ticks() - state["hold_start"]) / 1000.0
        if elapsed < required * HOLD_TOLERANCE:
            return

        state["holding_offset"] = None
        state["song_index"] += 1
        state["note_start"] = pygame.time.get_ticks()

        if state["song_index"] >= len(state["song_midis"]):
            state["message"] = f"Cancion completa: {state['song_name']}!"
            state["message_until"] = pygame.time.get_ticks() + 2500
            state["mode"] = MODE_FREE
            state["song_index"] = 0
            state["song_midis"] = []
            state["song_durations"] = []
            return

        next_midi = state["song_midis"][state["song_index"]]
        needed = needed_base_for_midi(next_midi, self.base_midi)
        if needed != self.base_midi:
            self.base_midi = needed
            state["base_midi"] = needed
            self.sounds, _ = load_sounds(needed)

    # ------------------------------------------------------------
    # Dibujo
    # ------------------------------------------------------------
    def _draw(self):
        self.background.draw(self.screen)

        if self.state["mode"] == MODE_MENU:
            draw_song_menu(self.screen, self.fonts, SONGS, self.state["menu_selected"])
        else:
            draw_hud(self.screen, self.fonts, self.state)
            draw_piano(self.screen, self.fonts["key_label"], self.active_offsets, self.state)

        pygame.display.flip()
