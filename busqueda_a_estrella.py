import heapq


# Definir una función para el algoritmo A*
def a_estrella(grafo, inicio, objetivo):
  # Inicializar el conjunto de nodos visitados y el diccionario de costos
  visitados = set()
  costos = {inicio: 0}
  # Inicializar la cola de prioridad con el nodo de inicio y su costo estimado
  cola_prioridad = [(0, inicio)]
  # Inicializar el diccionario para registrar el camino recorrido
  camino_rec = {inicio: None}

  # Mientras haya nodos en la cola de prioridad
  while cola_prioridad:
    # Extraer el nodo con el costo mínimo estimado de la cola de prioridad
    costo_actual, nodo_actual = heapq.heappop(cola_prioridad)

    # Si el nodo actual es el objetivo, se ha encontrado la solución
    if nodo_actual == objetivo:
      return construir_camino(camino_rec, inicio, objetivo), costos[objetivo]

    # Marcar el nodo actual como visitado
    visitados.add(nodo_actual)

    # Explorar los nodos vecinos del nodo actual
    for vecino, costo in grafo[nodo_actual].items():
      # Calcular el costo total estimado para llegar al vecino
      costo_total = costo_actual + costo

      # Si el vecino no ha sido visitado o el nuevo costo es menor que el costo anterior
      if vecino not in visitados or costo_total < costos.get(
          vecino, float('inf')):
        # Actualizar el costo del vecino en el diccionario de costos
        costos[vecino] = costo_total
        # Calcular la prioridad del vecino (costo total estimado + costo estimado hasta el objetivo)
        prioridad = costo_total + heuristic(grafo, vecino, objetivo)
        # Agregar el vecino a la cola de prioridad
        heapq.heappush(cola_prioridad, (prioridad, vecino))
        # Registrar el camino recorrido hasta el vecino
        camino_rec[vecino] = nodo_actual

  # Si no se encontró el objetivo después de explorar todos los nodos
  return None, None


# Función heurística para estimar el costo desde un nodo hasta el objetivo
def heuristic(grafo, nodo, objetivo):
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


# Ejemplo de grafo de prueba ponderado (representado como un diccionario de diccionarios)
grafo_ponderado = {
    'A': {
        'B': 5,
        'C': 7
    },
    'B': {
        'A': 5,
        'D': 8,
        'E': 4
    },
    'C': {
        'A': 7,
        'F': 6
    },
    'D': {
        'B': 8
    },
    'E': {
        'B': 4,
        'F': 3
    },
    'F': {
        'C': 6,
        'E': 3
    }
}

# Nodo de inicio y nodo objetivo
nodo_inicio = 'A'
nodo_objetivo = 'F'

# Llamar a la función A* para encontrar el camino más corto desde el nodo inicial hasta el objetivo
camino_mas_corto, costo_camino_mas_corto = a_estrella(grafo_ponderado,
                                                      nodo_inicio,
                                                      nodo_objetivo)

if camino_mas_corto:
  print("Camino encontrado en A*:", camino_mas_corto)
  print("Costo del camino más corto:", costo_camino_mas_corto)
  print("_____________________________________________________")
else:
  print("No se encontró un camino desde", nodo_inicio, "hasta", nodo_objetivo)
  print("_____________________________________________________")
