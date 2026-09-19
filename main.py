"""
Piano de escritorio - modo "notas que caen" con puntaje y combo
==================================================================
Cubre 2 octavas a la vez (25 notas), con DOS teclados apilados
(arriba = octava alta, abajo = octava baja, igual que en el teclado
físico) y un carril de notas cayendo arriba del teclado de arriba,
al estilo Guitar Hero: debes tocar la tecla justo cuando la nota
llega a la línea blanca.

Controles de teclado:
  Teclado ARRIBA (octava alta):  Q W E R T Y U I   (negras: 2 3 5 6 7)
  Teclado ABAJO  (octava baja):  Z X C V B N M     (negras: S D G H J)
  Flechas ARRIBA/ABAJO: cambia la octava visible (también hay un
    selector con el mouse arriba a la derecha).
  + / - : sube/baja el tempo (también hay un selector con el mouse).
  P: abre/cierra el menú de canciones para practicar.
  F11: pantalla completa / ventana normal.
  ESC: salir.

Modo práctica (P):
  - Las notas caen por el carril y debes tocar la tecla cuando lleguen
    a la línea blanca: "¡Perfecto!" si el tiempo es muy exacto, "Bien"
    si acertaste dentro de la ventana, o la nota se marca como fallada
    si no la tocas a tiempo.
  - La tecla que toca AHORA se resalta en VERDE en el teclado físico,
    la que sigue DESPUÉS en AZUL, para ir preparando la mano.
  - Si la siguiente nota no está en las 2 octavas visibles, aparece un
    aviso ("Sube/Baja a la octava X") antes de que llegue.
  - Puntaje y combo se acumulan; al terminar la canción se guarda el
    puntaje en el marcador (ver scoreboard.py) y se muestra a la
    derecha junto con tus mejores puntajes anteriores de esa canción.

Las canciones están en songs.py (separado, para agregar más sin tocar
este archivo). El marcador persiste en scores.json vía scoreboard.py.

Sonido:
  - Si existe una carpeta "samples/" con archivos .wav nombrados como
    la nota (ej: C3.wav, Cs3.wav... la 's' es sostenido), se usan esos
    samples reales. Si falta alguno, se sintetiza automáticamente.
"""

import os
import sys

import numpy as np
import pygame

from songs import SONGS
from scoreboard import load_scores_for, save_score

# ------------------------------------------------------------------
# Configuración general
# ------------------------------------------------------------------

SAMPLE_RATE = 44100
BASE_MIDI_DEFAULT = 48  # C3 = MIDI 48
OCTAVE_SHIFT_STEPS = (-2, -1, 0, 1, 2)  # pasos de 12 semitonos permitidos (C1..C7)

DEFAULT_BPM = 100
BPM_MIN, BPM_MAX, BPM_STEP = 40, 240, 5
TEMPO_PRESETS = [60, 80, 100, 120, 140, 160, 180, 200]

VISUAL_LEAD = 2.0     # segundos que tarda una nota en caer desde arriba hasta la línea
LEAD_IN = 2.3          # segundos de espera antes de que la primera nota sea exigible
HIT_WINDOW = 0.25      # ventana total para acertar una nota (segundos)
PERFECT_WINDOW = 0.08  # dentro de esta ventana cuenta como "perfecto"
LOOKAHEAD_WARNING = 3.0  # con cuánta anticipación avisar que hay que cambiar de octava

NOTE_NAMES = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]

OFFSET_TO_KEY = {
    0: pygame.K_z,  1: pygame.K_s,  2: pygame.K_x,  3: pygame.K_d,
    4: pygame.K_c,  5: pygame.K_v,  6: pygame.K_g,  7: pygame.K_b,
    8: pygame.K_h,  9: pygame.K_n,  10: pygame.K_j, 11: pygame.K_m,
    12: pygame.K_q, 13: pygame.K_2, 14: pygame.K_w, 15: pygame.K_3,
    16: pygame.K_e, 17: pygame.K_r, 18: pygame.K_5, 19: pygame.K_t,
    20: pygame.K_6, 21: pygame.K_y, 22: pygame.K_7, 23: pygame.K_u,
    24: pygame.K_i,
}
KEY_OFFSETS = {v: k for k, v in OFFSET_TO_KEY.items()}

OFFSET_TO_LABEL = {
    0: "Z", 1: "S", 2: "X", 3: "D", 4: "C", 5: "V", 6: "G", 7: "B",
    8: "H", 9: "N", 10: "J", 11: "M", 12: "Q", 13: "2", 14: "W",
    15: "3", 16: "E", 17: "R", 18: "5", 19: "T", 20: "6", 21: "Y",
    22: "7", 23: "U", 24: "I",
}

ROW_LOW = [(0, False), (1, True), (2, False), (3, True), (4, False),
           (5, False), (6, True), (7, False), (8, True), (9, False),
           (10, True), (11, False)]
ROW_HIGH = [(12, False), (13, True), (14, False), (15, True), (16, False),
            (17, False), (18, True), (19, False), (20, True), (21, False),
            (22, True), (23, False), (24, False)]

NUM_KEYS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
PLUS_KEYS = [pygame.K_EQUALS, pygame.K_KP_PLUS]
MINUS_KEYS = [pygame.K_MINUS, pygame.K_KP_MINUS]

# ------------------------------------------------------------------
# Tamaños del lienzo interno (se escala solo al tamaño de la ventana/pantalla)
# ------------------------------------------------------------------
WHITE_KEY_W = 92
WHITE_KEY_H = 280
BLACK_KEY_W = 58
BLACK_KEY_H = 175
ROW_GAP = 30
BOTTOM_MARGIN = 30
SIDE_MARGIN = 24

TITLE_Y = 14
SUBTITLE_Y = 54
STATUS_Y = 86
HIGHWAY_TOP = 116
HIGHWAY_HEIGHT = 260

MAX_WHITES = max(
    sum(1 for _, black in ROW_LOW if not black),
    sum(1 for _, black in ROW_HIGH if not black),
)
KB_WIDTH = SIDE_MARGIN * 2 + MAX_WHITES * WHITE_KEY_W   # ancho del área del teclado/carril
RIGHT_PANEL_WIDTH = 210
PANEL_GAP = 20
CANVAS_WIDTH = KB_WIDTH + PANEL_GAP + RIGHT_PANEL_WIDTH

TOP_MARGIN = HIGHWAY_TOP + HIGHWAY_HEIGHT + 8
CANVAS_HEIGHT = TOP_MARGIN + WHITE_KEY_H + ROW_GAP + WHITE_KEY_H + BOTTOM_MARGIN

MODE_FREE = "free"
MODE_MENU = "menu"
MODE_SONG = "song"

COLOR_BG = (24, 24, 28)
COLOR_WHITE_KEY = (250, 250, 250)
COLOR_WHITE_ACTIVE = (255, 205, 60)
COLOR_BLACK_KEY = (20, 20, 20)
COLOR_BLACK_ACTIVE = (255, 165, 20)
COLOR_TARGET_NOW = (60, 220, 90)
COLOR_TARGET_NEXT = (70, 165, 235)
COLOR_TEXT = (235, 235, 235)
COLOR_DIM = (150, 150, 155)
COLOR_WARN = (255, 170, 60)
COLOR_NOTE_HIGH = (90, 175, 235)
COLOR_NOTE_LOW = (255, 150, 70)
COLOR_PANEL_BG = (36, 36, 42)
COLOR_DROPDOWN_BG = (55, 55, 64)
COLOR_DROPDOWN_BORDER = (110, 110, 120)


def midi_to_freq(midi_note):
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


def note_name_for_offset(offset, base_midi):
    return note_name_for_midi(base_midi + offset)


def note_name_for_midi(midi):
    name = NOTE_NAMES[midi % 12]
    octave = (midi // 12) - 1
    return f"{name}{octave}"


def note_name_to_midi(name):
    idx = 0
    while idx < len(name) and not (name[idx].isdigit() or name[idx] == "-"):
        idx += 1
    letter, octave = name[:idx], int(name[idx:])
    return (octave + 1) * 12 + NOTE_NAMES.index(letter)


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
    for offset in range(25):
        midi = base_midi + offset
        name = note_name_for_midi(midi)
        wav_path = os.path.join(samples_dir, f"{name}.wav")
        if os.path.isfile(wav_path):
            sounds[offset] = pygame.mixer.Sound(wav_path)
            loaded_from_file += 1
        else:
            sounds[offset] = synth_piano_tone(midi_to_freq(midi))
    return sounds, loaded_from_file


def find_reachable_base(target_midi, current_base):
    candidates = []
    for k in OCTAVE_SHIFT_STEPS:
        base = BASE_MIDI_DEFAULT + 12 * k
        if 0 <= target_midi - base <= 24:
            candidates.append(base)
    if not candidates:
        return None
    return min(candidates, key=lambda b: abs(b - current_base))


def describe_target(target_midi, current_base):
    offset = target_midi - current_base
    if 0 <= offset <= 24:
        return ("key", offset)
    return ("shift", find_reachable_base(target_midi, current_base))


def compute_column_map():
    """x, ancho y si-es-negra para cada uno de los 25 offsets, usando el
    patrón de ROW_HIGH como referencia (ROW_LOW comparte el mismo patrón,
    así que una nota C en cualquiera de las 2 octavas cae en la misma
    columna del carril)."""
    n_whites = sum(1 for _, b in ROW_HIGH if not b)
    row_width = n_whites * WHITE_KEY_W
    start_x = SIDE_MARGIN + (KB_WIDTH - 2 * SIDE_MARGIN - row_width) // 2

    col = {}
    white_positions = {}
    x = start_x
    for offset, is_black in ROW_HIGH:
        if not is_black:
            white_positions[offset] = x
            col[offset] = (x, WHITE_KEY_W - 3, False)
            x += WHITE_KEY_W
    for offset, is_black in ROW_HIGH:
        if is_black:
            base_x = white_positions.get(offset - 1, start_x)
            bx = base_x + WHITE_KEY_W - BLACK_KEY_W // 2
            col[offset] = (bx, BLACK_KEY_W, True)
    for offset in range(12):
        col[offset] = col[offset + 12]
    return col


COLUMN_MAP = compute_column_map()


def schedule_notes(notes, start_time, seconds_per_beat):
    schedule = []
    cum = 0.0
    for name, dur in notes:
        st = start_time + cum * seconds_per_beat
        schedule.append({
            "midi": note_name_to_midi(name),
            "dur": dur,
            "start": st,
            "end": st + dur * seconds_per_beat,
            "result": None,
        })
        cum += dur
    return schedule


def reschedule_remaining(state):
    sched = state["schedule"]
    idx = state["song_index"]
    if idx >= len(sched):
        return
    spb = 60.0 / state["bpm"]
    base_time = state["song_time"]
    cum = 0.0
    for i in range(idx, len(sched)):
        sched[i]["start"] = base_time + cum * spb
        sched[i]["end"] = sched[i]["start"] + sched[i]["dur"] * spb
        cum += sched[i]["dur"]


# ------------------------------------------------------------------
# Widget: dropdown simple con mouse
# ------------------------------------------------------------------

class Dropdown:
    def __init__(self, rect, options, get_label, on_select):
        self.rect = pygame.Rect(rect)
        self.options = options  # lista de (texto, valor)
        self.get_label = get_label
        self.on_select = on_select
        self.is_open = False

    def option_rects(self):
        return [pygame.Rect(self.rect.x, self.rect.bottom + i * self.rect.height,
                             self.rect.width, self.rect.height)
                for i in range(len(self.options))]

    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            self.is_open = not self.is_open
            return
        if self.is_open:
            for (label, value), r in zip(self.options, self.option_rects()):
                if r.collidepoint(pos):
                    self.on_select(value)
                    self.is_open = False
                    return
            self.is_open = False

    def draw(self, canvas, font):
        pygame.draw.rect(canvas, COLOR_DROPDOWN_BG, self.rect, border_radius=6)
        pygame.draw.rect(canvas, COLOR_DROPDOWN_BORDER, self.rect, width=1, border_radius=6)
        text = font.render(f"{self.get_label()}  \u25be", True, COLOR_TEXT)
        canvas.blit(text, (self.rect.x + 10, self.rect.y + (self.rect.height - text.get_height()) // 2))
        if self.is_open:
            for (label, _value), r in zip(self.options, self.option_rects()):
                pygame.draw.rect(canvas, (45, 45, 52), r)
                pygame.draw.rect(canvas, (90, 90, 100), r, width=1)
                opt_text = font.render(label, True, COLOR_TEXT)
                canvas.blit(opt_text, (r.x + 10, r.y + (r.height - opt_text.get_height()) // 2))


# ------------------------------------------------------------------
# Dibujo
# ------------------------------------------------------------------

def draw_key_row(canvas, label_font, row_layout, y_top, active_offsets, now_offset, next_offset):
    n_whites = sum(1 for _, black in row_layout if not black)
    row_width = n_whites * WHITE_KEY_W
    start_x = SIDE_MARGIN + (KB_WIDTH - 2 * SIDE_MARGIN - row_width) // 2

    white_positions = {}
    x = start_x
    for offset, is_black in row_layout:
        if not is_black:
            white_positions[offset] = x
            color = COLOR_WHITE_ACTIVE if offset in active_offsets else COLOR_WHITE_KEY
            rect = pygame.Rect(x, y_top, WHITE_KEY_W - 3, WHITE_KEY_H)
            pygame.draw.rect(canvas, color, rect, border_radius=8)
            pygame.draw.rect(canvas, (15, 15, 15), rect, width=2, border_radius=8)
            if offset == now_offset:
                pygame.draw.rect(canvas, COLOR_TARGET_NOW, rect, width=6, border_radius=8)
            elif offset == next_offset:
                pygame.draw.rect(canvas, COLOR_TARGET_NEXT, rect, width=6, border_radius=8)
            label = OFFSET_TO_LABEL[offset]
            text = label_font.render(label, True, (20, 20, 20))
            tw, th = text.get_size()
            canvas.blit(text, (x + (WHITE_KEY_W - 3 - tw) // 2, y_top + WHITE_KEY_H - th - 16))
            x += WHITE_KEY_W

    for offset, is_black in row_layout:
        if is_black:
            base_x = white_positions.get(offset - 1, start_x)
            bx = base_x + WHITE_KEY_W - BLACK_KEY_W // 2
            color = COLOR_BLACK_ACTIVE if offset in active_offsets else COLOR_BLACK_KEY
            rect = pygame.Rect(bx, y_top, BLACK_KEY_W, BLACK_KEY_H)
            pygame.draw.rect(canvas, color, rect, border_radius=6)
            if offset == now_offset:
                pygame.draw.rect(canvas, COLOR_TARGET_NOW, rect, width=5, border_radius=6)
            elif offset == next_offset:
                pygame.draw.rect(canvas, COLOR_TARGET_NEXT, rect, width=5, border_radius=6)
            label = OFFSET_TO_LABEL[offset]
            text = label_font.render(label, True, (255, 255, 255))
            tw, th = text.get_size()
            canvas.blit(text, (bx + (BLACK_KEY_W - tw) // 2, y_top + BLACK_KEY_H - th - 14))


def draw_highway(canvas, state):
    rect = pygame.Rect(0, HIGHWAY_TOP, KB_WIDTH, HIGHWAY_HEIGHT)
    pygame.draw.rect(canvas, (16, 16, 20), rect)
    pygame.draw.line(canvas, (255, 255, 255), (0, HIGHWAY_TOP + HIGHWAY_HEIGHT - 2),
                      (KB_WIDTH, HIGHWAY_TOP + HIGHWAY_HEIGHT - 2), 3)

    if state["mode"] != MODE_SONG:
        return

    spb = 60.0 / state["bpm"]
    now = state["song_time"]
    for note in state["schedule"]:
        time_until = note["start"] - now
        if time_until > VISUAL_LEAD or time_until < -0.2:
            continue
        offset = note["midi"] - state["base_midi"]
        if not (0 <= offset <= 24):
            continue
        x, w, _is_black = COLUMN_MAP[offset]
        frac = 1 - (time_until / VISUAL_LEAD)
        y_bottom = HIGHWAY_TOP + HIGHWAY_HEIGHT * frac
        dur_seconds = note["dur"] * spb
        h = max(8, dur_seconds / VISUAL_LEAD * HIGHWAY_HEIGHT)
        y_top = y_bottom - h

        if note["result"] == "perfect":
            color = (255, 255, 255)
        elif note["result"] == "good":
            color = (210, 210, 130)
        elif note["result"] == "miss":
            color = (130, 60, 60)
        else:
            color = COLOR_NOTE_HIGH if offset >= 12 else COLOR_NOTE_LOW

        pygame.draw.rect(canvas, color, pygame.Rect(int(x), int(y_top), int(w), int(h)), border_radius=5)


def draw_top_area(canvas, font, big_font, state):
    canvas.blit(big_font.render("Piano de escritorio", True, (255, 255, 255)), (SIDE_MARGIN, TITLE_Y))

    subtitle = "F11: pantalla completa   |   P: practicar   |   ESC: salir"
    canvas.blit(font.render(subtitle, True, COLOR_DIM), (SIDE_MARGIN, SUBTITLE_Y))

    if state["message"] and pygame.time.get_ticks() < state["message_until"]:
        canvas.blit(font.render(state["message"], True, COLOR_TARGET_NOW), (SIDE_MARGIN, STATUS_Y))
        return

    if state["mode"] == MODE_MENU:
        y = STATUS_Y
        for i, (name, _notes) in enumerate(SONGS):
            canvas.blit(font.render(f"{i + 1}. {name}", True, COLOR_TEXT), (SIDE_MARGIN, y))
            y += 22
        canvas.blit(font.render("Presiona el número para elegir  |  P para cancelar",
                                 True, COLOR_DIM), (SIDE_MARGIN, y + 4))

    elif state["mode"] == MODE_SONG:
        idx = state["song_index"]
        total = len(state["schedule"])
        line = (f"{state['song_name']}   |   Nota {min(idx + 1, total)}/{total}   |   "
                f"Puntaje: {state['score']}   |   Combo x{state['combo']}")
        canvas.blit(font.render(line, True, COLOR_TEXT), (SIDE_MARGIN, STATUS_Y))

        # Aviso de cambio de octava si alguna nota próxima lo necesita
        for note in state["schedule"][idx:]:
            if note["start"] - state["song_time"] > LOOKAHEAD_WARNING:
                break
            kind, value = describe_target(note["midi"], state["base_midi"])
            if kind == "shift":
                arrow = "\u25b2 Sube" if value > state["base_midi"] else "\u25bc Baja"
                target_name = note_name_for_offset(0, value)
                msg = f"{arrow} a la octava {target_name} (flechas \u2191/\u2193 o el selector de arriba)"
                canvas.blit(font.render(msg, True, COLOR_WARN), (SIDE_MARGIN, HIGHWAY_TOP - 24))
                break

        if state["feedback"] and pygame.time.get_ticks() < state["feedback_until"]:
            fb = big_font.render(state["feedback"], True, COLOR_TARGET_NOW)
            canvas.blit(fb, (KB_WIDTH // 2 - fb.get_width() // 2, HIGHWAY_TOP + HIGHWAY_HEIGHT // 2 - 20))

    else:
        canvas.blit(font.render(
            "Flechas arriba/abajo: octava   |   +/-: tempo   |   Selectores arriba a la derecha",
            True, COLOR_DIM), (SIDE_MARGIN, STATUS_Y))


def draw_side_panel(canvas, font, big_font, state):
    px = KB_WIDTH + PANEL_GAP
    rect = pygame.Rect(px, STATUS_Y, RIGHT_PANEL_WIDTH, CANVAS_HEIGHT - STATUS_Y - 20)
    pygame.draw.rect(canvas, COLOR_PANEL_BG, rect, border_radius=8)

    y = rect.y + 14
    canvas.blit(big_font.render("Puntajes", True, COLOR_TEXT), (px + 14, y))
    y += 40

    song_name = state["song_name"] or (state["leaderboard_song"] or "")
    if song_name:
        name_text = font.render(song_name, True, COLOR_DIM)
        canvas.blit(name_text, (px + 14, y))
        y += 26

    if state["mode"] == MODE_SONG:
        canvas.blit(font.render(f"Puntaje actual: {state['score']}", True, COLOR_TARGET_NOW), (px + 14, y))
        y += 22
        canvas.blit(font.render(f"Combo: x{state['combo']}  (máx x{state['max_combo']})",
                                 True, COLOR_TEXT), (px + 14, y))
        y += 34

    canvas.blit(font.render("Mejores puntajes:", True, COLOR_DIM), (px + 14, y))
    y += 24
    board = state["leaderboard"]
    if not board:
        canvas.blit(font.render("Aún sin puntajes", True, COLOR_DIM), (px + 14, y))
    else:
        for i, s in enumerate(board):
            canvas.blit(font.render(f"{i + 1}. {s}", True, COLOR_TEXT), (px + 14, y))
            y += 22


def draw_piano(canvas, font, big_font, label_font, active_offsets, state, dropdowns):
    canvas.fill(COLOR_BG)
    draw_top_area(canvas, font, big_font, state)
    draw_highway(canvas, state)

    now_offset, next_offset = None, None
    if state["mode"] == MODE_SONG:
        sched = state["schedule"]
        idx = state["song_index"]
        if idx < len(sched):
            kind, value = describe_target(sched[idx]["midi"], state["base_midi"])
            if kind == "key" and abs(state["song_time"] - sched[idx]["start"]) <= HIT_WINDOW:
                now_offset = value
        if idx + 1 < len(sched):
            kind2, value2 = describe_target(sched[idx + 1]["midi"], state["base_midi"])
            if kind2 == "key":
                next_offset = value2

    y_high = TOP_MARGIN
    y_low = TOP_MARGIN + WHITE_KEY_H + ROW_GAP
    draw_key_row(canvas, label_font, ROW_HIGH, y_high, active_offsets, now_offset, next_offset)
    draw_key_row(canvas, label_font, ROW_LOW, y_low, active_offsets, now_offset, next_offset)

    draw_side_panel(canvas, font, big_font, state)

    for dd in dropdowns:
        dd.draw(canvas, font)


def compute_scale_offset(window_size, canvas_size):
    win_w, win_h = window_size
    cw, ch = canvas_size
    scale = min(win_w / cw, win_h / ch)
    new_w, new_h = max(1, int(cw * scale)), max(1, int(ch * scale))
    return scale, (win_w - new_w) // 2, (win_h - new_h) // 2


def blit_scaled(window_screen, canvas):
    scale, offx, offy = compute_scale_offset(window_screen.get_size(), (CANVAS_WIDTH, CANVAS_HEIGHT))
    new_w, new_h = int(CANVAS_WIDTH * scale), int(CANVAS_HEIGHT * scale)
    scaled = pygame.transform.smoothscale(canvas, (max(1, new_w), max(1, new_h)))
    window_screen.fill((0, 0, 0))
    window_screen.blit(scaled, (offx, offy))


def start_song(state, idx, base_midi_ref):
    name, notes = SONGS[idx]
    spb = 60.0 / state["bpm"]
    state["song_name"] = name
    state["schedule"] = schedule_notes(notes, LEAD_IN, spb)
    state["song_time"] = 0.0
    state["song_index"] = 0
    state["score"] = 0
    state["combo"] = 0
    state["max_combo"] = 0
    state["feedback"] = ""
    state["feedback_until"] = 0
    state["leaderboard"] = load_scores_for(name)
    state["leaderboard_song"] = name
    state["mode"] = MODE_SONG


def finish_song(state):
    board = save_score(state["song_name"], state["score"])
    state["leaderboard"] = board
    state["message"] = f"\u00a1Canci\u00f3n completa! Puntaje: {state['score']} (combo m\u00e1x x{state['max_combo']})"
    state["message_until"] = pygame.time.get_ticks() + 3000
    state["mode"] = MODE_FREE


def update_song_timing(state, dt):
    if state["mode"] != MODE_SONG:
        return
    state["song_time"] += dt
    sched = state["schedule"]
    while state["song_index"] < len(sched):
        note = sched[state["song_index"]]
        if state["song_time"] > note["start"] + HIT_WINDOW:
            note["result"] = "miss"
            state["combo"] = 0
            state["feedback"] = "Fallaste"
            state["feedback_until"] = pygame.time.get_ticks() + 500
            state["song_index"] += 1
        else:
            break
    if state["song_index"] >= len(sched):
        finish_song(state)


def try_hit(state, offset):
    if state["mode"] != MODE_SONG:
        return
    sched = state["schedule"]
    idx = state["song_index"]
    if idx >= len(sched):
        return
    note = sched[idx]
    kind, value = describe_target(note["midi"], state["base_midi"])
    if kind != "key" or value != offset:
        return
    diff = abs(state["song_time"] - note["start"])
    if diff > HIT_WINDOW:
        return
    result = "perfect" if diff <= PERFECT_WINDOW else "good"
    note["result"] = result
    multiplier = 1 + min(3, state["combo"] // 10)
    points = (150 if result == "perfect" else 100) * multiplier
    state["score"] += points
    state["combo"] += 1
    state["max_combo"] = max(state["max_combo"], state["combo"])
    state["feedback"] = "\u00a1Perfecto!" if result == "perfect" else "\u00a1Bien!"
    state["feedback_until"] = pygame.time.get_ticks() + 400
    state["song_index"] += 1
    if state["song_index"] >= len(sched):
        finish_song(state)


def main():
    pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)
    pygame.init()
    pygame.mixer.set_num_channels(32)

    window_screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Piano de escritorio")
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    is_fullscreen = False

    font = pygame.font.SysFont("Arial", 17)
    big_font = pygame.font.SysFont("Arial", 26, bold=True)
    label_font = pygame.font.SysFont("Arial", 22, bold=True)
    clock = pygame.time.Clock()

    state = {
        "mode": MODE_FREE,
        "base_midi": BASE_MIDI_DEFAULT,
        "bpm": DEFAULT_BPM,
        "sounds": None,
        "song_name": "",
        "schedule": [],
        "song_time": 0.0,
        "song_index": 0,
        "score": 0,
        "combo": 0,
        "max_combo": 0,
        "feedback": "",
        "feedback_until": 0,
        "message": "",
        "message_until": 0,
        "leaderboard": [],
        "leaderboard_song": "",
    }
    sounds, loaded_from_file = load_sounds(state["base_midi"])
    state["sounds"] = sounds
    if loaded_from_file:
        print(f"Se cargaron {loaded_from_file} samples reales desde samples/.")
    else:
        print("No se encontraron samples en samples/. Usando sonido sintetizado.")

    def on_select_octave(base_value):
        state["base_midi"] = base_value
        state["sounds"], _ = load_sounds(base_value)

    def on_select_tempo(bpm_value):
        state["bpm"] = bpm_value
        reschedule_remaining(state)

    octave_options = [(note_name_for_offset(0, BASE_MIDI_DEFAULT + 12 * k), BASE_MIDI_DEFAULT + 12 * k)
                       for k in OCTAVE_SHIFT_STEPS]
    tempo_options = [(f"{b} BPM", b) for b in TEMPO_PRESETS]

    octave_dropdown = Dropdown(
        (CANVAS_WIDTH - 340, TITLE_Y, 155, 32), octave_options,
        get_label=lambda: f"Octava: {note_name_for_offset(0, state['base_midi'])}",
        on_select=on_select_octave)
    tempo_dropdown = Dropdown(
        (CANVAS_WIDTH - 175, TITLE_Y, 150, 32), tempo_options,
        get_label=lambda: f"{state['bpm']} BPM",
        on_select=on_select_tempo)
    dropdowns = [octave_dropdown, tempo_dropdown]

    active_offsets = set()
    active_keys_down = set()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
                window_screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                scale, offx, offy = compute_scale_offset(window_screen.get_size(), (CANVAS_WIDTH, CANVAS_HEIGHT))
                cx = (event.pos[0] - offx) / scale
                cy = (event.pos[1] - offy) / scale
                for dd in dropdowns:
                    dd.handle_click((cx, cy))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        window_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        window_screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.RESIZABLE)

                elif event.key == pygame.K_p:
                    state["mode"] = MODE_MENU if state["mode"] == MODE_FREE else MODE_FREE

                elif event.key in PLUS_KEYS:
                    on_select_tempo(min(BPM_MAX, state["bpm"] + BPM_STEP))

                elif event.key in MINUS_KEYS:
                    on_select_tempo(max(BPM_MIN, state["bpm"] - BPM_STEP))

                elif event.key == pygame.K_UP and state["mode"] != MODE_MENU:
                    new_base = state["base_midi"] + 12
                    if new_base <= BASE_MIDI_DEFAULT + 12 * max(OCTAVE_SHIFT_STEPS):
                        on_select_octave(new_base)

                elif event.key == pygame.K_DOWN and state["mode"] != MODE_MENU:
                    new_base = state["base_midi"] - 12
                    if new_base >= BASE_MIDI_DEFAULT + 12 * min(OCTAVE_SHIFT_STEPS):
                        on_select_octave(new_base)

                elif state["mode"] == MODE_MENU and event.key in NUM_KEYS:
                    idx = NUM_KEYS.index(event.key)
                    if idx < len(SONGS):
                        if state["base_midi"] != BASE_MIDI_DEFAULT:
                            on_select_octave(BASE_MIDI_DEFAULT)
                        start_song(state, idx, BASE_MIDI_DEFAULT)

                elif state["mode"] != MODE_MENU and event.key in KEY_OFFSETS \
                        and event.key not in active_keys_down:
                    active_keys_down.add(event.key)
                    offset = KEY_OFFSETS[event.key]
                    active_offsets.add(offset)
                    state["sounds"][offset].play()
                    try_hit(state, offset)

            elif event.type == pygame.KEYUP:
                if event.key in KEY_OFFSETS:
                    active_keys_down.discard(event.key)
                    active_offsets.discard(KEY_OFFSETS[event.key])

        update_song_timing(state, dt)

        canvas_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        draw_piano(canvas_surface, font, big_font, label_font, active_offsets, state, dropdowns)
        blit_scaled(window_screen, canvas_surface)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
