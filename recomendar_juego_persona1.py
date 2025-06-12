import requests
import json
import datetime
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Lista fija de géneros
GENRES_LIST = [
    "action", "indie", "adventure", "rpg", "strategy", "shooter",
    "casual", "simulation", "puzzle", "arcade", "platformer", "racing",
    "massively-multiplayer", "sports", "fighting", "family", "card", "educational"
]

# Función para convertir géneros a vector one-hot
def get_genre_vector(game_genres):
    game_genre_slugs = [genre["slug"].lower() for genre in game_genres]
    return [1 if genre in game_genre_slugs else 0 for genre in GENRES_LIST]

# Función para mapear fecha de lanzamiento a valor de recencia
def map_recentness(release_date_str):
    if not release_date_str:
        return 3
    try:
        release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        years_old = (today - release_date).days / 365
        if years_old < 1:
            return 5
        elif years_old < 3:
            return 4
        elif years_old < 5:
            return 3
        elif years_old < 10:
            return 2
        else:
            return 1
    except Exception as e:
        print(f"Error procesando fecha {release_date_str}: {e}")
        return 3

# Función para mapear tiempo de juego
def map_playtime(playtime_hours):
    if playtime_hours < 5:
        return 1
    elif playtime_hours < 15:
        return 2
    elif playtime_hours < 30:
        return 3
    elif playtime_hours < 60:
        return 4
    else:
        return 5

# Normalización entre 0 y 1
def normalize_vector(vector):
    max_value = max(vector) if vector and max(vector) > 0 else 1
    return [round(x / max_value, 3) for x in vector]

# Obtener juegos desde la API RAWG
def fetch_games_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener datos: {response.status_code}")
        return None

# Generar vector de un juego
def generate_game_vector(game):
    genre_vector = get_genre_vector(game.get("genres", []))
    recentness = map_recentness(game.get("released"))
    playtime = map_playtime(game.get("playtime", 0))
    return genre_vector + [recentness, playtime]

# Procesar juegos y generar vectores normalizados
def process_games_from_api(api_url):
    data = fetch_games_from_api(api_url)
    if not data:
        return []
    
    results = []
    for game in data.get("results", []):
        game_vector = generate_game_vector(game)
        normalized_vector = normalize_vector(game_vector)
        results.append({
            "name": game.get("name"),
            "vector": game_vector,
            "normalized_vector": normalized_vector
        })
    return results

# Calcular las 3 mejores recomendaciones por similitud coseno
def recommend_top_games(group_vector, games_data, top_n=3):
    similarity_scores = []
    for game in games_data:
        game_vector = game["normalized_vector"]
        sim = cosine_similarity([group_vector], [game_vector])[0][0]
        similarity_scores.append((game["name"], sim))
    # Ordenar por similitud descendente
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    return similarity_scores[:top_n]

# Ejecutar si se llama directamente
if __name__ == "__main__":
    API_URL = "https://api.rawg.io/api/games?key=39ffc44387634851a4576b77fbd49bba&platforms=4&tags=9&metacritic=80,100"
    
    print("Procesando juegos de la API RAWG...\n")
    
    games_data = process_games_from_api(API_URL)
    
    print(f"Se encontraron {len(games_data)} juegos:")
    for i, game_data in enumerate(games_data):
        print(f"\n{i+1}. {game_data['name']}")
        print(f"   Vector: {game_data['vector']}")
        print(f"   Vector normalizado: {game_data['normalized_vector']}")

    # === Lógica final: recomendación basada en vector grupal ===
    group_vector = [0.15, 0.0, 0.05, 0.025, 0.15, 0.0, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.95, 0.875]

    top_games = recommend_top_games(group_vector, games_data)

    print("\n🎯 Top 3 juegos más recomendados para el grupo:")
    for i, (name, score) in enumerate(top_games, start=1):
        print(f"{i}. {name} — Similitud: {round(score, 3)}")

