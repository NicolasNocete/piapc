import pygame
import heapq

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla y la cuadrícula
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding con A* en Pygame")

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definir obstáculos en la cuadrícula
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
obstacles = [(3, 3), (3, 4), (3, 5), (5, 5), (6, 5)]
for ob in obstacles:
    grid[ob[1]][ob[0]] = 1  # Marcar como obstáculo

# 📌 Función de heurística para A* (distancia Manhattan)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# 📌 Implementación del algoritmo A*
def astar(start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = { (x, y): float('inf') for y in range(ROWS) for x in range(COLS) }
    f_score = { (x, y): float('inf') for y in range(ROWS) for x in range(COLS) }
    g_score[start] = 0
    f_score[start] = heuristic(start, goal)

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < COLS and 0 <= ny < ROWS and grid[ny][nx] == 0]

        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return []  # Retorna vacío si no hay camino

# 📌 Clase del personaje
class Character:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.path = []
        self.speed = 5  # Velocidad de movimiento

    def move_to(self, target_x, target_y):
        self.path = astar((self.x, self.y), (target_x, target_y))

    def update(self):
        if self.path:
            next_pos = self.path[0]
            if (self.x, self.y) == next_pos:
                self.path.pop(0)
            else:
                target_x, target_y = next_pos
                if self.x < target_x:
                    self.x += 1
                elif self.x > target_x:
                    self.x -= 1
                if self.y < target_y:
                    self.y += 1
                elif self.y > target_y:
                    self.y -= 1

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# 📌 Clase de objetivo
class Goal:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# 📌 Inicialización del personaje y el objetivo
player = Character(0, 0)
goal = Goal(8, 8)

# 📌 Loop principal del juego
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // CELL_SIZE, my // CELL_SIZE
            if grid[gy][gx] == 0:  # Solo permitir clic en celdas vacías
                goal.x, goal.y = gx, gy
                player.move_to(goal.x, goal.y)

    # Dibujar la cuadrícula
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if grid[y][x] == 1:  # Dibujar obstáculos
                pygame.draw.rect(screen, RED, rect)

    # Dibujar la ruta encontrada
    for px, py in player.path:
        pygame.draw.rect(screen, (200, 200, 0), (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    player.update()
    player.draw()
    goal.draw()

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
