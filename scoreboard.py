"""
scoreboard.py - Guarda y carga los mejores puntajes por canción.
==================================================================
Separado de main.py para poder cambiar cómo se guardan los puntajes
(por ejemplo, mover a una base de datos) sin tocar el resto de la app.

Los puntajes se guardan en scores.json, en la misma carpeta que este
archivo, con la forma:
    { "Nombre de la canción": [950, 700, 500], ... }
(siempre ordenados de mayor a menor, se guardan como máximo TOP_N).
"""

import json
import os

SCORES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.json")
TOP_N = 5


def load_all_scores():
    if not os.path.isfile(SCORES_PATH):
        return {}
    try:
        with open(SCORES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def load_scores_for(song_name):
    return load_all_scores().get(song_name, [])


def save_score(song_name, score):
    """Agrega un puntaje nuevo para la canción y devuelve el top actualizado."""
    data = load_all_scores()
    scores = data.get(song_name, [])
    scores.append(score)
    scores = sorted(scores, reverse=True)[:TOP_N]
    data[song_name] = scores
    try:
        with open(SCORES_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"No se pudo guardar el puntaje: {e}")
    return scores
