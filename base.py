
# Comentario

# imprimir en pantalla
print("Hola Mundo")

# input de datos
nombre = input("Ingrese su nombre: ")

print("el nombre ingresado es " + nombre)

numero = 2
palabra = "hola"
esCorrecto = True

print(palabra * numero)

#condicionales
if (numero == 2):
    print("El numero es 2")
    hola = "hola"
elif (numero == 3):
    print("El numero es 3")
else:
    print("El numero no es 2")

#ciclos de control
for i in range(0, 5):
    print(i)

numero = 0
while (numero < 5):
    print(numero)
    numero += 2

#listas
lista = [1, 2, 3, 4, 5]
print(lista[0])

#diccionarios
diccionario = {"nombre": "Juan", "edad": 22}
print(diccionario["nombre"])


#funciones
def saludar():
    print("Hola desde la funcion")

def sumar(a, b):
    return a + b

saludar()

suma = sumar(2,3)
print("suma " + str(suma))
# f strings
print(f"suma formateada {suma}")
# f string con redondeo de suma a dos decimales
print(f"suma formateada {suma:.2f}")

    