# 🧮 Función para calcular el vector promedio
def calculate_group_vector(vectors):
    if not vectors:
        return []
    
    vector_length = len(vectors[0])
    group_vector = [0.0] * vector_length
    
    for vec in vectors:
        for i in range(vector_length):
            group_vector[i] += vec[i]
    
    group_vector = [round(x / len(vectors), 3) for x in group_vector]
    return group_vector

# 🧪 Vectores normalizados de los 4 usuarios
daniel =     [0.0, 0.333, 0.333, 0.0, 0.333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0]
lina =       [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.25, 0.25, 0.0, 0.0, 0.0, 0.25, 1.0]
juan_jose =  [0.2, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0]
juan_esteban = [0.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 1.0, 1.0]

# Agrupamos los vectores
group_vectors = [daniel, lina, juan_jose, juan_esteban]

# Calculamos el vector grupal promedio
group_vector = calculate_group_vector(group_vectors)

# Mostramos el resultado
print("🧠 Vector promedio del grupo:", group_vector)