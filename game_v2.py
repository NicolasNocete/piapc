import pygame
from dataclasses import dataclass, field

# Configuración de pantalla
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Máquina de Estados - Personaje")
clock = pygame.time.Clock()

# Definir constantes del personaje
GRAVITY = 1
JUMP_FORCE = -15
SPEED = 5
GROUND_Y = HEIGHT - 100

# Definir colores por estado
state_colors = {
    "Reposo": (0, 255, 0),      # Verde
    "Caminando": (0, 0, 255),    # Azul
    "Saltando": (255, 255, 0),   # Amarillo
    "Atacando": (255, 0, 255),   # Morado
    "Dañado": (255, 0, 0),       # Rojo
    "Muerto": (0, 0, 0)          # Negro
}

@dataclass
class State:
    name: str
    transitions: dict = field(default_factory=dict)
    duration: int = 0  
    start_time: int = 0  

    def add_transition(self, event, next_state, condition=None):
        self.transitions[event] = (next_state, condition)

    def enter(self):
        if self.duration > 0:
            self.start_time = pygame.time.get_ticks()

class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.current_state.enter()
        self.health = 3  
        self.dead = False  # Nueva variable para bloquear acciones tras la muerte

    def trigger(self, event, **kwargs):
        if self.dead:
            return  # No permitir transiciones si está muerto
        
        if event in self.current_state.transitions:
            next_state, condition = self.current_state.transitions[event]
            if condition is None or condition(kwargs):  
                print(f"🎮 Transición: {self.current_state.name} ➝ {next_state.name} ({event})")
                self.current_state = next_state
                self.current_state.enter()

                # Si la transición fue a "Muerto", bloquear todo movimiento
                if next_state.name == "Muerto":
                    self.dead = True
            else:
                print(f"❌ No se puede ejecutar '{event}' desde {self.current_state.name}")

    def update(self):
        if self.current_state.duration > 0:
            elapsed = pygame.time.get_ticks() - self.current_state.start_time
            if elapsed >= self.current_state.duration:
                self.trigger("terminar")

    def take_damage(self):
        if self.dead:
            return  # No permitir recibir más daño si ya está muerto

        self.health -= 1
        print(f"💔 Vida restante: {self.health}")
        if self.health <= 0:
            self.trigger("morir")
            self.dead = True  # Bloquea cualquier otra acción            
        else:
            self.trigger("recibir_daño")

# 🎮 Definir los estados del personaje con duraciones
reposo = State("Reposo")
caminando = State("Caminando")
atacando = State("Atacando", duration=1000)  
saltando = State("Saltando")
daniado = State("Dañado", duration=1500)  
muerto = State("Muerto")

# 📌 Definir transiciones
reposo.add_transition("moverse", caminando)
reposo.add_transition("saltar", saltando)
reposo.add_transition("atacar", atacando)
reposo.add_transition("recibir_daño", daniado)

caminando.add_transition("detenerse", reposo)
caminando.add_transition("saltar", saltando)
caminando.add_transition("atacar", atacando)
caminando.add_transition("recibir_daño", daniado)

saltando.add_transition("tocar_suelo", reposo)
saltando.add_transition("recibir_daño", daniado)

atacando.add_transition("terminar", reposo)

daniado.add_transition("terminar", reposo)
daniado.add_transition("morir", muerto)

# 🚀 Crear la máquina de estados del personaje
personaje = StateMachine(reposo)

# 🎮 Variables de movimiento y física
x, y = WIDTH // 2, GROUND_Y
velocity_y = 0
on_ground = True
moving_left = False
moving_right = False

# 🎮 Game Loop
running = True
while running:
    screen.fill((200, 200, 200))  
    personaje.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not personaje.dead:  # No permitir acciones si está muerto
            if event.key == pygame.K_a:
                moving_left = True
                personaje.trigger("moverse")
            if event.key == pygame.K_d:
                moving_right = True
                personaje.trigger("moverse")
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = JUMP_FORCE
                personaje.trigger("saltar")
                on_ground = False
            if event.key == pygame.K_f:
                personaje.trigger("atacar")
            if event.key == pygame.K_r:
                personaje.take_damage()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
                if not moving_right:
                    personaje.trigger("detenerse")
            if event.key == pygame.K_d:
                moving_right = False
                if not moving_left:
                    personaje.trigger("detenerse")
            if event.key == pygame.K_SPACE:
                personaje.trigger("tocar_suelo")

    # 🏃‍♂️ Movimiento horizontal
    if not personaje.dead:  # No permitir movimiento si está muerto
        if moving_left:
            x -= SPEED
        if moving_right:
            x += SPEED

    # 🏃‍♂️ Física del personaje (gravedad)
    velocity_y += GRAVITY
    y += velocity_y
    if y >= GROUND_Y:  
        y = GROUND_Y
        velocity_y = 0
        on_ground = True
        if personaje.current_state.name == "Saltando":
            personaje.trigger("tocar_suelo")

    # 🎨 Dibujar el personaje como un rectángulo con el color del estado actual
    pygame.draw.rect(screen, state_colors[personaje.current_state.name], (x, y, 50, 50))

    pygame.display.flip()
    clock.tick(30)  

pygame.quit()
