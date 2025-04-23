class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

    def saludar(self):
        print(f"Hola, soy {self.nombre}")

class Estudiante(Persona):
    def __init__(self, nombre, grado):
        super().__init__(nombre)  # Llamar al constructor de la clase base
        self.grado = grado

    def estudiar(self):
        print(f"{self.nombre} está estudiando en el grado {self.grado}")

# Crear un objeto de la clase Estudiante
estudiante = Estudiante("Juan", "11º")
estudiante.saludar()  # Salida: Hola, soy Juan
estudiante.estudiar()  # Salida: Juan está estudiando en el grado 11º
