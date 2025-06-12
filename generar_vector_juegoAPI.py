import requests
import json
import datetime
from datetime import datetime

# Lista fija de géneros (copiada del archivo original)
GENRES_LIST = [
    "action", "indie", "adventure", "rpg", "strategy", "shooter",
    "casual", "simulation", "puzzle", "arcade", "platformer", "racing",
    "massively-multiplayer", "sports", "fighting", "family", "card", "educational"
]

# Función para convertir géneros a vector one-hot
def get_genre_vector(game_genres):
    # Convierte los géneros del juego a sus slugs en minúsculas
    game_genre_slugs = [genre["slug"].lower() for genre in game_genres]
    # Crea vector de 0s y 1s
    return [1 if genre in game_genre_slugs else 0 for genre in GENRES_LIST]

# Función para mapear fecha de lanzamiento a valor de recencia
def map_recentness(release_date_str):
    if not release_date_str:
        return 3  # Valor por defecto si no hay fecha
    
    try:
        # Convertir string a fecha
        release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        years_old = (today - release_date).days / 365

        # Mapear años desde lanzamiento a escala de recencia
        if years_old < 1:  # Menos de un año
            return 5  # Muy reciente
        elif years_old < 3:
            return 4  # Bastante reciente
        elif years_old < 5:
            return 3  # Medianamente reciente
        elif years_old < 10:
            return 2  # Algo antiguo
        else:
            return 1  # Clásico/viejo
    except Exception as e:
        print(f"Error procesando fecha {release_date_str}: {e}")
        return 3  # Valor por defecto en caso de error

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

# Función para obtener juegos desde la API RAWG
def fetch_games_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener datos: {response.status_code}")
        return None

# Función principal para generar vectores de juegos
def generate_game_vector(game):
    # Obtener vector de géneros
    genre_vector = get_genre_vector(game.get("genres", []))
    
    # Mapear recencia basada en fecha de lanzamiento
    recentness = map_recentness(game.get("released"))
    
    # Mapear tiempo de juego
    playtime = map_playtime(game.get("playtime", 0))
    
    # Combinar todo en un solo vector
    return genre_vector + [recentness, playtime]

# Procesar todos los juegos de la API y generar resultados
def process_games_from_api(api_url):
    # Obtener datos de la API
    data = fetch_games_from_api(api_url)
    
    if not data:
        return []
    
    results = []
    
    # Procesar cada juego
    for game in data.get("results", []):
        game_vector = generate_game_vector(game)
        normalized_vector = normalize_vector(game_vector)
        
        # Guardar información del juego y sus vectores
        results.append({
            "name": game.get("name"),
            "vector": game_vector,
            "normalized_vector": normalized_vector
        })
    
    return results

# Ejecutar si se llama directamente
if __name__ == "__main__":
    API_URL = "https://api.rawg.io/api/games?key=39ffc44387634851a4576b77fbd49bba&platforms=4&tags=9&metacritic=80,100"
    
    print("Procesando juegos de la API RAWG...\n")
    
    games_data = process_games_from_api(API_URL)
    
    print(f"Se encontraron {len(games_data)} juegos:")
    
    # Mostrar resultados para cada juego
    for i, game_data in enumerate(games_data):
        print(f"\n{i+1}. {game_data['name']}")
        print(f"   Vector: {game_data['vector']}")
        print(f"   Vector normalizado: {game_data['normalized_vector']}")
