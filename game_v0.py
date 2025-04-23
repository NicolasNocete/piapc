from dataclasses import dataclass, field

@dataclass
class State:
    name: str
    transitions: dict = field(default_factory=dict)

    def add_transition(self, event, next_state, condition=None):
        """Agrega una transición con una condición opcional"""
        self.transitions[event] = (next_state, condition)

class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state

    def trigger(self, event, **kwargs):
        """Ejecuta una transición basada en el evento y condiciones."""
        if event in self.current_state.transitions:
            next_state, condition = self.current_state.transitions[event]
            if condition is None or condition(kwargs):  
                print(f"🎮 Transición: {self.current_state.name} ➝ {next_state.name} ({event})")
                self.current_state = next_state
            else:
                print(f"❌ No se puede ejecutar '{event}' desde {self.current_state.name}")
        else:
            print(f"❌ Acción '{event}' no permitida en estado '{self.current_state.name}'")

# 🎮 Definir los estados del personaje
reposo = State("Reposo")
caminando = State("Caminando")
atacando = State("Atacando")
saltando = State("Saltando")
daniado = State("Dañado")
muerto = State("Muerto")

# 📌 Definir transiciones entre estados
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

atacando.add_transition("terminar_ataque", reposo)
atacando.add_transition("recibir_daño", daniado)

daniado.add_transition("recuperarse", reposo)
daniado.add_transition("morir", muerto)

# 🚀 Crear la máquina de estados del personaje
personaje = StateMachine(reposo)

# 🔄 Simulación del comportamiento en el juego
acciones = [
    ("moverse", {}),
    ("saltar", {}),
    ("tocar_suelo", {}),
    ("atacar", {}),
    ("terminar_ataque", {}),
    ("recibir_daño", {}),
    ("recuperarse", {}),
    ("recibir_daño", {}),
    ("morir", {}),
]

for accion, context in acciones:
    personaje.trigger(accion, **context)