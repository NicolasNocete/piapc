# Definir una función para el algoritmo de búsqueda en profundidad
def busqueda_en_profundidad(grafo,
                            inicio,
                            objetivo,
                            visitados=None,
                            camino=None):
  if visitados is None:
    visitados = set()
  if camino is None:
    camino = []

  # Marcar el nodo actual como visitado y agregarlo al camino
  visitados.add(inicio)
  camino.append(inicio)

  # Si el nodo actual es el objetivo, se ha encontrado la solución
  if inicio == objetivo:
    return camino

  # Explorar los nodos vecinos del nodo actual
  for vecino in grafo[inicio]:
    if vecino not in visitados:
      # Llamar recursivamente a la función para explorar el vecino
      resultado = busqueda_en_profundidad(grafo, vecino, objetivo, visitados,
                                          camino)
      if resultado is not None:
        return resultado

  # Si no se encuentra el objetivo a partir del nodo actual, retroceder
  camino.pop()
  return None


# Función para imprimir el camino encontrado
def imprimir_camino(camino):
  print("Camino encontrado en busqueda en profundidad:")
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

# Llamar a la función busqueda_en_profundidad para buscar el camino desde el nodo inicial hasta el objetivo
camino_encontrado = busqueda_en_profundidad(grafo, nodo_inicio, nodo_objetivo)

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
