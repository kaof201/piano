"""
music_theory.py - Conversion entre nombres de nota, MIDI y frecuencia
=======================================================================
Funciones puras (sin pygame, sin estado global) para moverse entre las
tres representaciones de una nota que usa el resto del programa:

  - nombre de nota en texto, ej. "Cs4"   (como en songs.py)
  - numero MIDI absoluto, ej. 61
  - frecuencia en Hz, ej. 277.18         (para sintetizar el tono)

Tambien vive aqui la logica de "a que octava base hay que saltar para
ver esta nota en las 2 octavas visibles", que usan tanto el modo
practica como el dibujo de las etiquetas.
"""

from config import NOTE_NAMES, VALID_BASES, OFFSET_TO_LABEL


def midi_to_freq(midi_note):
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


def note_name_for_offset(offset, base_midi):
    midi = base_midi + offset
    name = NOTE_NAMES[midi % 12]
    octave = (midi // 12) - 1
    return f"{name}{octave}"


def note_name_to_midi(name):
    """Convierte un nombre de nota (ej. 'Cs4') a su valor MIDI absoluto."""
    idx = 0
    while idx < len(name) and not (name[idx].isdigit() or name[idx] == "-"):
        idx += 1
    letter, octave = name[:idx], int(name[idx:])
    return (octave + 1) * 12 + NOTE_NAMES.index(letter)


def get_song_midis_and_durations(notes):
    """Convierte la lista de (nota, duracion_en_tiempos) de una cancion en
    valores MIDI absolutos + su duracion. No descarta notas fuera de
    C3-C5: el modo practica avisa como llegar a cualquier octava C1-C5."""
    midis, durations = [], []
    for name, dur in notes:
        midis.append(note_name_to_midi(name))
        durations.append(dur)
    return midis, durations


def label_for_absolute_midi(midi, base_midi):
    """Devuelve (texto, en_vista) para una nota absoluta dada la octava
    base actual. Si la nota esta dentro de las 2 octavas visibles,
    devuelve la letra de la tecla; si no, el nombre de la nota."""
    offset = midi - base_midi
    if 0 <= offset <= 24:
        return OFFSET_TO_LABEL[offset], True
    return note_name_for_offset(0, midi), False


def needed_base_for_midi(midi, current_base):
    """Octava base valida (una de VALID_BASES) a la que hay que moverse
    para que 'midi' quede visible en las 2 octavas mostradas. Si hay
    mas de una opcion posible (porque las 2 octavas visibles se
    solapan), se elige la mas cercana a la octava actual para pedir el
    menor numero de saltos con las flechas."""
    candidates = [b for b in VALID_BASES if 0 <= midi - b <= 24]
    if not candidates:
        candidates = VALID_BASES
    return min(candidates, key=lambda b: abs(b - current_base))


def song_duration_seconds(notes, bpm):
    """Duracion aproximada de una cancion (lista de (nota, duracion)) en
    segundos, para un BPM dado."""
    total_beats = sum(dur for _, dur in notes)
    return total_beats * (60.0 / bpm)
