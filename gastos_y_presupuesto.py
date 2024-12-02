import matplotlib.pyplot as plt
# Ingresa el presupuesto
def ingresar_presupuesto():
    presupuesto = float(input("Ingrese el presupuesto total: "))
    return presupuesto

# Ingresa los gastos
def ingresar_gastos():
    categorias = {}
    while True:
        categoria = input("Ingrese la categoría del gasto (o 'salir' para terminar): ")
        if categoria.lower() == 'salir':
            break
        valor = float(input(f"Ingrese el valor del gasto en {categoria}: "))
        categorias[categoria] = valor
    return categorias

def graficar_gastos(categorias):
    plt.subplot(1, 2, 1)  
    plt.bar(categorias.keys(), categorias.values(), color='blue')
    plt.xlabel('Categorías')
    plt.ylabel('Gastos')
    plt.title('Gastos por Categoría')

def graficar_presupuesto_vs_gastos(presupuesto, categorias):
    total_gastos = sum(categorias.values())
    plt.subplot(1, 2, 2)  # 1 fila, 2 columnas, segundo subplot
    plt.bar(['Presupuesto', 'Gastos'], [presupuesto, total_gastos], color=['green', 'red'])
    plt.xlabel('Comparación')
    plt.ylabel('Valor')
    plt.title('Comparación de Presupuesto y Gastos')

def main():
    presupuesto = ingresar_presupuesto()
    categorias = ingresar_gastos()
    plt.figure(figsize=(15, 5))  # Crear una figura con tamaño adecuado
    graficar_gastos(categorias)
    graficar_presupuesto_vs_gastos(presupuesto, categorias)
    plt.tight_layout()  # Ajustar el layout para que no se solapen las gráficas
    plt.show()

if __name__ == "__main__":
    main()
    
class HistorialDeGastos:
    def __init__(self):
        self.gastos_mensuales = {}

    def agregar_gasto(self, mes, monto):
        if mes in self.gastos_mensuales:
            self.gastos_mensuales[mes] += monto
        else:
            self.gastos_mensuales[mes] = monto

    def mostrar_historial(self):
        print("Historial mensual de gastos:")
        for mes, monto in sorted(self.gastos_mensuales.items()):
            print(f"{mes}: ${monto:.2f}")
            plt.figure(figsize=(10, 5))
            plt.bar(self.gastos_mensuales.keys(), self.gastos_mensuales.values(), color='purple')
            plt.xlabel('Meses')
            plt.ylabel('Gastos')
            plt.title('Historial de Gastos Mensuales')
            plt.show()