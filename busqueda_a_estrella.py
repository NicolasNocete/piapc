import heapq


# Definir una función para el algoritmo A*
def a_estrella(grafo, inicio, objetivo, heuristic):
    visitados = set()
    costos = {inicio: 0}
    cola_prioridad = [(0, inicio)]
    camino_rec = {inicio: None}

    while cola_prioridad:
        _, nodo_actual = heapq.heappop(cola_prioridad)

        if nodo_actual == objetivo:
            return construir_camino(camino_rec, inicio, objetivo)  # Retornar solo el camino

        visitados.add(nodo_actual)

        for vecino in grafo[nodo_actual]:  # Iterar sobre la lista de vecinos
            costo_total = costos[nodo_actual] + 1  # Asumir costo uniforme de 1

            if vecino not in visitados or costo_total < costos.get(vecino, float('inf')):
                costos[vecino] = costo_total
                prioridad = costo_total + heuristic(vecino, objetivo)
                heapq.heappush(cola_prioridad, (prioridad, vecino))
                camino_rec[vecino] = nodo_actual

    return None  # Si no se encuentra un camino


# Función heurística para estimar el costo desde un nodo hasta el objetivo
def heuristic(nodo, objetivo):
    # En este caso, simplemente devolvemos 0, ya que no tenemos información heurística
    return 0


# Función para construir el camino a partir del registro de camino recorrido
def construir_camino(camino_rec, inicio, objetivo):
    camino = []
    nodo_actual = objetivo
    while nodo_actual is not None:
        camino.insert(0, nodo_actual)
        nodo_actual = camino_rec[nodo_actual]
    return camino


# Ejemplo de grafo de prueba ponderado (representado como un diccionario de listas)
grafo_ponderado = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'E'],
    'F': ['C', 'F']
}

# Nodo de inicio y nodo objetivo
nodo_inicio = 'A'
nodo_objetivo = 'F'

# Llamar a la función A* para encontrar el camino más corto desde el nodo inicial hasta el objetivo
camino_mas_corto = a_estrella(grafo_ponderado,
                              nodo_inicio,
                              nodo_objetivo,
                              heuristic)

if camino_mas_corto:
    print("Camino encontrado en A*:", camino_mas_corto)
    print("_____________________________________________________")
else:
    print("No se encontró un camino desde", nodo_inicio, "hasta", nodo_objetivo)
    print("_____________________________________________________")
