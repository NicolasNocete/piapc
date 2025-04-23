from collections import deque


# Definir una función para el algoritmo de búsqueda en anchura
def busqueda_en_anchura(grafo, inicio, objetivo):
  # Inicializar una cola para almacenar los nodos que se deben visitar
  cola = deque([(inicio, [inicio])])
  # Inicializar un conjunto para almacenar los nodos visitados
  visitados = set([inicio])

  # Mientras haya nodos en la cola
  while cola:
    # Extraer el primer nodo de la cola y su camino hasta ahora
    nodo_actual, camino_actual = cola.popleft()
    # Si el nodo actual es el objetivo, se ha encontrado la solución
    if nodo_actual == objetivo:
      return camino_actual  # Se encontró el objetivo
    # Explorar los nodos vecinos del nodo actual
    for vecino in grafo[nodo_actual]:
      # Si el vecino no ha sido visitado
      if vecino not in visitados:
        # Marcar el vecino como visitado
        visitados.add(vecino)
        # Agregar el vecino y su camino al camino hasta ahora a la cola para exploración posterior
        cola.append((vecino, camino_actual + [vecino]))

  # Si no se encontró el objetivo después de explorar todos los nodos
  return None  # No se encontró el objetivo


# Función para imprimir el camino paso a paso
def imprimir_camino(camino):
  print("Camino encontrado en busqueda en anchura:")
  for i, nodo in enumerate(camino):
    print("Paso", i + 1, ":", nodo)


# Ejemplo de grafo de prueba (representado como un diccionario)
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Nodo de inicio y nodo objetivo
nodo_inicio = 'A'
nodo_objetivo = 'F'

# Llamar a la función busqueda_en_anchura para buscar el camino desde el nodo inicial hasta el objetivo
camino_encontrado = busqueda_en_anchura(grafo, nodo_inicio, nodo_objetivo)

if camino_encontrado:
  imprimir_camino(camino_encontrado)
  print("Resultado: Se encontró un camino desde", nodo_inicio, "hasta",
        nodo_objetivo)
  print("_____________________________________________________")
else:
  print("No se encontró un camino desde", nodo_inicio, "hasta", nodo_objetivo)
  print("Resultado: No se encontró un camino desde", nodo_inicio, "hasta",
        nodo_objetivo)
  print("_____________________________________________________")
