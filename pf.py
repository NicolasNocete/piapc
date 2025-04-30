import random
import pygame  # Importar la biblioteca Pygame para gráficos y eventos
from busqueda_en_profundidad import busqueda_en_profundidad  # Importar búsqueda en profundidad
from busqueda_en_anchura import busqueda_en_anchura  # Importar búsqueda en anchura
from busqueda_a_estrella import a_estrella  # Importar algoritmo A*

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla y la cuadrícula
WIDTH, HEIGHT = 800, 600  # Dimensiones de la pantalla
ROWS, COLS = 10, 10  # Número de filas y columnas en la cuadrícula
CELL_SIZE = WIDTH // COLS  # Tamaño de cada celda en píxeles

# Crear la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding en Pygame")  # Título de la ventana

# Definir colores
WHITE = (255, 255, 255)  # Color blanco
BLACK = (0, 0, 0)  # Color negro
RED = (255, 0, 0)  # Color rojo
GREEN = (0, 255, 0)  # Color verde
BLUE = (0, 0, 255)  # Color azul


# 📌 Función de heurística para A* (distancia Manhattan)
def heuristic(a, b):
    """
    Calculate the Manhattan distance between two points.

    The Manhattan distance is the sum of the absolute differences of their Cartesian coordinates.
    It is commonly used in grid-based pathfinding algorithms.

    Parameters:
    a (tuple): A tuple representing the coordinates (x, y) of the first point.
    b (tuple): A tuple representing the coordinates (x, y) of the second point.

    Returns:
    int: The Manhattan distance between the two points.
    """
    # La distancia de Manhattan es una medida de distancia en un espacio en cuadrícula,
    # calculada como la suma de las diferencias absolutas entre las coordenadas correspondientes.
    # Calcular la distancia Manhattan entre dos puntos
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# 📌 Generar grafo a partir de la cuadrícula
def generar_grafo(grid):
    # Crear un grafo donde cada celda está conectada a sus vecinos accesibles
    return {
        (x, y): [
            (x + dx, y + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Vecinos arriba, abajo, izquierda, derecha
            if 0 <= x + dx < COLS and 0 <= y + dy < ROWS and grid[y + dy][x + dx] == 0  # Verificar límites y obstáculos
        ]
        for y in range(ROWS)
        for x in range(COLS)
    }

def generar_obstaculos(grid):
    # Generar obstáculos aleatorios en la cuadrícula
    for y in range(ROWS):
        for x in range(COLS):
            if x!=0 and y!=0 and grid[y][x] == 0 and random.random() < 0.2:  # Probabilidad del 20% de ser un obstáculo
                grid[y][x] = 1  # Marcar como obstáculo
                
# Definir obstáculos en la cuadrícula
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]  # Inicializar la cuadrícula vacía
obstacles = generar_obstaculos(grid)  # Generar obstáculos aleatorios

#obstacles = [(3, 3), (3, 4), (3, 5), (5, 5), (6, 5)]  # Lista de posiciones de obstáculos
#for ob in obstacles:
#    grid[ob[1]][ob[0]] = 1  # Marcar las celdas como obstáculos

grafo = generar_grafo(grid)  # Generar el grafo a partir de la cuadrícula

# Diccionario de algoritmos disponibles
ALGORITHMS = {
    "bfs": lambda start, goal: busqueda_en_anchura(grafo, start, goal),  # Búsqueda en anchura
    "dfs": lambda start, goal: busqueda_en_profundidad(grafo, start, goal),  # Búsqueda en profundidad
    "astar": lambda start, goal: a_estrella(grafo, start, goal, heuristic),  # A*
}

# 📌 Selector de algoritmo
selected_algorithm = "bfs"  # Algoritmo por defecto (puede cambiarse con teclas)

# 📌 Clase del personaje
class Character:
    def __init__(self, x, y):
        # Inicializar la posición del personaje
        self.x, self.y = x, y
        self.path = []  # Inicializar el camino vacío

    def move_to(self, target_x, target_y):
        # Mover al personaje al objetivo usando el algoritmo seleccionado
        algorithm = ALGORITHMS[selected_algorithm]  # Seleccionar el algoritmo
        result = algorithm((self.x, self.y), (target_x, target_y))  # Ejecutar el algoritmo
        # Validar que el resultado sea una lista de tuplas válidas
        if isinstance(result, list) and all(isinstance(pos, tuple) and len(pos) == 2 for pos in result):
            self.path = result  # Asignar el camino encontrado
        else:
            self.path = []  # Si no hay camino, dejar vacío

    def update(self):
        # Actualizar la posición del personaje siguiendo el camino
        if self.path:  # Si hay un camino
            next_pos = self.path[0]  # Obtener la siguiente posición
            if (self.x, self.y) == next_pos:  # Si ya está en la posición
                self.path.pop(0)  # Eliminar la posición del camino
            else:
                target_x, target_y = next_pos
                # Moverse hacia la siguiente posición
                if self.x < target_x:
                    self.x += 1
                elif self.x > target_x:
                    self.x -= 1
                if self.y < target_y:
                    self.y += 1
                elif self.y > target_y:
                    self.y -= 1

    def draw(self):
        # Dibujar el personaje en la pantalla
        pygame.draw.rect(screen, BLUE, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# 📌 Clase de objetivo
class Goal:
    def __init__(self, x, y):
        # Inicializar la posición del objetivo
        self.x, self.y = x, y

    def draw(self):
        # Dibujar el objetivo en la pantalla
        pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# 📌 Inicialización del personaje y el objetivo
player = Character(0, 0)  # Crear el personaje en la posición inicial
goal = Goal(8, 8)  # Crear el objetivo en la posición inicial

# 📌 Loop principal del juego
running = True
while running:
    screen.fill(WHITE)  # Limpiar la pantalla con color blanco

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Si se cierra la ventana
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Si se hace clic con el ratón
            mx, my = pygame.mouse.get_pos()  # Obtener la posición del ratón
            gx, gy = mx // CELL_SIZE, my // CELL_SIZE  # Convertir a coordenadas de la cuadrícula
            if grid[gy][gx] == 0:  # Verificar que no sea un obstáculo
                goal.x, goal.y = gx, gy  # Mover el objetivo
                player.move_to(goal.x, goal.y)  # Calcular el camino hacia el objetivo
        elif event.type == pygame.KEYDOWN:  # Si se presiona una tecla
            if event.key == pygame.K_1:  # Cambiar a A*
                selected_algorithm = "astar"
            elif event.key == pygame.K_2:  # Cambiar a DFS
                selected_algorithm = "dfs"
            elif event.key == pygame.K_3:  # Cambiar a BFS
                selected_algorithm = "bfs"

    # Dibujar la cuadrícula
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # Crear un rectángulo
            pygame.draw.rect(screen, BLACK, rect, 1)  # Dibujar el borde de la celda
            if grid[y][x] == 1:  # Si es un obstáculo
                pygame.draw.rect(screen, RED, rect)  # Dibujar el obstáculo

    # Dibujar la ruta encontrada
    for px, py in player.path:  # Iterar sobre las posiciones del camino
        pygame.draw.rect(screen, (200, 200, 0), (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Dibujar el camino

    player.update()  # Actualizar la posición del personaje
    player.draw()  # Dibujar el personaje
    goal.draw()  # Dibujar el objetivo

    pygame.display.flip()  # Actualizar la pantalla
    pygame.time.delay(100)  # Pausar brevemente para controlar la velocidad del juego

pygame.quit()  # Salir de Pygame
