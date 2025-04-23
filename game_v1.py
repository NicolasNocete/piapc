import pygame
from dataclasses import dataclass, field

# Inicializar Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Máquina de Estados - Personaje")

# Definir el reloj para controlar el tiempo
clock = pygame.time.Clock()

@dataclass
class State:
    name: str
    transitions: dict = field(default_factory=dict)
    duration: int = 0  # Duración del estado en milisegundos (0 = indefinido)
    start_time: int = 0  # Guarda el tiempo en que entró a este estado

    def add_transition(self, event, next_state, condition=None):
        """Agrega una transición con una condición opcional"""
        self.transitions[event] = (next_state, condition)

    def enter(self):
        """Registra el tiempo de entrada si tiene duración definida"""
        if self.duration > 0:
            self.start_time = pygame.time.get_ticks()

class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.current_state.enter()

    def trigger(self, event, **kwargs):
        """Ejecuta una transición basada en el evento y condiciones."""
        if event in self.current_state.transitions:
            next_state, condition = self.current_state.transitions[event]
            if condition is None or condition(kwargs):  
                print(f"🎮 Transición: {self.current_state.name} ➝ {next_state.name} ({event})")
                self.current_state = next_state
                self.current_state.enter()
            else:
                print(f"❌ No se puede ejecutar '{event}' desde {self.current_state.name}")
        else:
            print(f"❌ Acción '{event}' no permitida en estado '{self.current_state.name}'")

    def update(self):
        """Verifica si el estado debe cambiar automáticamente al terminar el tiempo"""
        if self.current_state.duration > 0:
            elapsed = pygame.time.get_ticks() - self.current_state.start_time
            if elapsed >= self.current_state.duration:
                self.trigger("terminar")

# 🎮 Definir los estados del personaje con duraciones
reposo = State("Reposo")
caminando = State("Caminando")
atacando = State("Atacando", duration=1000)  # 1 segundo
saltando = State("Saltando")
daniado = State("Dañado", duration=1500)  # 1.5 segundos
muerto = State("Muerto")

# 📌 Definir transiciones con condiciones
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

# 🎮 Game Loop
running = True
while running:
    screen.fill((30, 30, 30))  # Fondo oscuro
    personaje.update()  # Verifica si el estado debe cambiar automáticamente

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Controles del teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                personaje.trigger("moverse")
            if event.key == pygame.K_d:
                personaje.trigger("moverse")
            if event.key == pygame.K_SPACE:
                personaje.trigger("saltar")
            if event.key == pygame.K_f:
                personaje.trigger("atacar")
            if event.key == pygame.K_r:
                personaje.trigger("recibir_daño")

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d]:
                personaje.trigger("detenerse")
            if event.key == pygame.K_SPACE:
                personaje.trigger("tocar_suelo")

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()