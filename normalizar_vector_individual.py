# Función para normalizar un vector entre 0 y 1
def normalize_vector(vector):
    max_value = max(vector)
    return [round(x / max_value, 3) if max_value > 0 else 0 for x in vector]

# -------------------------
# VECTOR YA GENERADO
# -------------------------

# Vector de ejemplo ya construido (géneros + recentness + playtime)
# Este es solo un ejemplo; reemplázalo por el que tú tengas.
user_vector = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3]

# Normalizar el vector
normalized_vector = normalize_vector(user_vector)

# Mostrar resultados
print("✅ Vector original:", user_vector)
print("✅ Vector normalizado:", normalized_vector)