import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Vector individual normalizado de Valentina
valentina_vector = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.75]

# Vectores promedio actuales de los grupos
group_vectors = {
    "Grupo 1": [0.05, 0.208, 0.083, 0.175, 0.083, 0.0, 0.0, 0.175, 0.0, 0.062, 0.0, 0.0, 0.0, 0.062, 0.062, 0.0, 0.125, 0.0, 0.812, 1.0],
    "Grupo 2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.3, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.7, 0.5],
    "Grupo 3": [0.2, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.2],
    "Grupo 4": [0.05, 0.0, 0.1, 0.05, 0.3, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 1.0]
}

# Calcular similitud coseno entre Valentina y cada grupo
similarities = {}
for group_name, group_vector in group_vectors.items():
    sim = cosine_similarity([valentina_vector], [group_vector])[0][0]
    similarities[group_name] = sim

# Ordenar los grupos por similitud de mayor a menor
sorted_groups = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

# Mostrar resultados
print("\n🔍 Similitud con cada grupo:")
for group, score in sorted_groups:
    print(f"{group}: {round(score, 3)}")

# Preguntar al usuario con qué grupo quiere unirse
print("\n🤔 ¿Con qué grupo deseas unirte?")
for i, (group, _) in enumerate(sorted_groups, 1):
    print(f"{i}. {group}")
choice = int(input("Elige el número del grupo: "))

# Obtener nombre del grupo elegido
chosen_group_name = sorted_groups[choice - 1][0]
print(f"\n✅ Has elegido unirte a {chosen_group_name}")

# Recalcular nuevo vector promedio del grupo con Valentina incluida
original_vector = group_vectors[chosen_group_name]
new_group_matrix = np.array([original_vector, valentina_vector])
new_group_vector = np.mean(new_group_matrix, axis=0)

# Convertir a lista de floats normales para una impresión limpia
new_group_vector = [round(float(x), 3) for x in new_group_vector]

# Mostrar nuevo vector promedio limpio
print(f"\n📈 Nuevo vector promedio para {chosen_group_name}:")
print(new_group_vector)
