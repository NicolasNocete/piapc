class CuentaBancaria:
    def __init__(self, saldo):
        self.saldo = saldo

    def depositar(self, cantidad):
        self.saldo += cantidad

    def retirar(self, cantidad):
        self.saldo -= cantidad

# Crear un objeto de la clase CuentaBancaria
cuenta = CuentaBancaria(100)

# Modificar el saldo mediante métodos
cuenta.depositar(50)
cuenta.retirar(20)

print(cuenta.saldo)  # Output: 130
