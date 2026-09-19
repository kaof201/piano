"""
songs.py - Canciones integradas para practicar con el piano de escritorio
==========================================================================
Este archivo está separado de main.py a propósito: para agregar una
canción nueva en el futuro, solo hay que añadir una entrada más a la
lista SONGS de aquí abajo. main.py no necesita cambiar.

Formato de cada canción:
    ("Nombre visible", [(nota, duracion), (nota, duracion), ...])

- "nota": nombre de la nota, igual a como las nombra main.py.
  Ejemplos válidos: "C4", "Cs4" (C sostenido / C#4), "D4", "G3", etc.
- "duracion": número relativo en tiempos/beats (1 = negra, 0.5 = corchea,
  2 = blanca, etc). Junto con el tempo (BPM) define cuánto dura cada nota
  y cuándo cae la siguiente en el modo práctica.

Para agregar una canción nueva:
1. Copia una entrada de ejemplo de abajo.
2. Cambia el nombre y la lista de notas.
3. Guarda el archivo. main.py la detecta automáticamente en el menú (tecla P).
"""

SONGS = [
    ("Estrellita dónde estás", [
        ("C4", 1), ("C4", 1), ("G4", 1), ("G4", 1), ("A4", 1), ("A4", 1), ("G4", 2),
        ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 1), ("D4", 1), ("C4", 2),
        ("G4", 1), ("G4", 1), ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 2),
        ("G4", 1), ("G4", 1), ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 2),
        ("C4", 1), ("C4", 1), ("G4", 1), ("G4", 1), ("A4", 1), ("A4", 1), ("G4", 2),
        ("F4", 1), ("F4", 1), ("E4", 1), ("E4", 1), ("D4", 1), ("D4", 1), ("C4", 2),
    ]),

    ("Fray Santiago", [
        ("C4", 1), ("D4", 1), ("E4", 1), ("C4", 1),
        ("C4", 1), ("D4", 1), ("E4", 1), ("C4", 1),
        ("E4", 1), ("F4", 1), ("G4", 2),
        ("E4", 1), ("F4", 1), ("G4", 2),
        ("G4", 0.5), ("A4", 0.5), ("G4", 0.5), ("F4", 0.5), ("E4", 1), ("C4", 1),
        ("G4", 0.5), ("A4", 0.5), ("G4", 0.5), ("F4", 0.5), ("E4", 1), ("C4", 1),
        ("C4", 1), ("G3", 1), ("C4", 2),
        ("C4", 1), ("G3", 1), ("C4", 2),
    ]),

    ("Mary tenía un corderito", [
        ("E4", 1), ("D4", 1), ("C4", 1), ("D4", 1), ("E4", 1), ("E4", 1), ("E4", 2),
        ("D4", 1), ("D4", 1), ("D4", 2),
        ("E4", 1), ("G4", 1), ("G4", 2),
        ("E4", 1), ("D4", 1), ("C4", 1), ("D4", 1), ("E4", 1), ("E4", 1), ("E4", 1), ("E4", 1),
        ("D4", 1), ("D4", 1), ("E4", 1), ("D4", 1), ("C4", 2),
    ]),
]
