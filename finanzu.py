import matplotlib.pyplot as plt
import os
import json
from datetime import datetime

# Directorio base donde se guardarán las carpetas de los usuarios
BASE_DIR = "usuarios"

# Crea el directorio base si no existe
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

def registrar_usuario():
    # Registra un nuevo usuario creando una carpeta con su información básica.
    nombre_usuario = input("Ingrese un nombre de usuario: ")
    user_path = os.path.join(BASE_DIR, nombre_usuario)

    if os.path.exists(user_path):
        print("El usuario ya existe. Intente con otro nombre.")
        return

    os.makedirs(user_path)
    correo = input("Ingrese su correo: ")
    contraseña = input("Ingrese su contraseña: ")

    with open(os.path.join(user_path, "informacion.txt"), "w") as file:
        file.write(f"Correo: {correo}\n")
        file.write(f"Contraseña: {contraseña}\n")
        file.write(f"Presupuesto: 0\n")  # Presupuesto inicial vacío
        file.write(f"Gastos: {json.dumps({})}\n")  # Gastos inicial vacío

    print("Usuario registrado exitosamente.")

def autenticar_usuario():
    # Autentica a un usuario existente verificando su contraseña.
    nombre_usuario = input("Ingrese su nombre de usuario: ").strip()
    user_path = os.path.join(BASE_DIR, nombre_usuario)

    if not os.path.exists(user_path):
        print("El usuario no existe.")
        return None

    contraseña = input("Ingrese su contraseña: ").strip()  

    with open(os.path.join(user_path, "informacion.txt"), "r") as file:
        lines = file.readlines()
        stored_password = lines[1].split(": ")[1].strip()  

    if contraseña == stored_password:
        print("Autenticación exitosa.")
        return user_path
    else:
        print("Contraseña incorrecta.")
        return None

def registrar_presupuesto(user_path):
    # Permite registrar o actualizar el presupuesto de un usuario autenticado.
    if not user_path:
        print("Debe iniciar sesión primero.")
        return

    try:
        presupuesto = float(input("Ingrese el monto de su presupuesto: ").strip())
        with open(os.path.join(user_path, "informacion.txt"), "r+") as file:
            lines = file.readlines()
            lines[2] = f"Presupuesto: {presupuesto}\n"  # Actualiza el presupuesto
            file.seek(0)
            file.writelines(lines)

        print("Presupuesto registrado exitosamente.")
    except ValueError:
        print("Monto inválido. Intente nuevamente.")

def ingresar_gastos(user_path):
    # Permite al usuario ingresar y sobrescribir gastos categorizados.
    if not user_path:
        print("Debe iniciar sesión primero.")
        return

    try:
        # Crear un nuevo diccionario para los nuevos gastos
        nuevos_gastos = {}

        while True:
            categoria = input("Ingrese la categoría del gasto (o 'salir' para terminar): ").strip()
            if categoria.lower() == "salir":
                break

            valor = float(input(f"Ingrese el valor del gasto en {categoria}: ").strip())
            nuevos_gastos[categoria] = valor  # Sobrescribe los valores anteriores con los nuevos

        # Actualizar los gastos en el archivo
        with open(os.path.join(user_path, "informacion.txt"), "r+") as file:
            lines = file.readlines()
            lines[3] = f"Gastos: {json.dumps(nuevos_gastos)}\n"  # Sobrescribe los gastos
            file.seek(0)
            file.writelines(lines)

        print("Gastos registrados exitosamente.")
    except ValueError:
        print("Valor inválido. Intente nuevamente.")


def guardar_reporte(user_path, reporte):
    if not user_path:
        print("Primero debe iniciar sesión.")
        return
    historial_path = os.path.join(user_path, "historial_reportes.json")
    if not os.path.exists(historial_path):
        with open(historial_path,"w") as file:
            json.dump([],file,indent=4)
    with open(historial_path, "r") as file:
        historial = json.load(file)
    historial.append(reporte)
    with open(historial_path, "w") as file:
        json.dump(historial, file, indent=4)

def graficar_gastos(categorias):
    plt.subplot(1, 2, 1)  
    plt.bar(categorias.keys(), categorias.values(), color="blue")
    plt.xlabel("Categorías")
    plt.ylabel("Gastos")
    plt.title("Gastos por categoría")

def graficar_presupuesto_vs_gastos(presupuesto, categorias):
    total_gastos = sum(categorias.values())
    plt.subplot(1, 2, 2)  
    plt.bar(["Presupuesto", "Gastos"], [presupuesto, total_gastos], color=["green", "red"])
    plt.ylabel("Valor")
    plt.xlabel("Comparación")
    plt.title("Comparación de presupuesto y gastos")

def generar_reporte(user_path):
    if not user_path:
        print("Primero debe iniciar sesión.")
        return
    with open(os.path.join(user_path, "informacion.txt"), "r") as file:
        lines = file.readlines()
        presupuesto = float(lines[2].split(": ")[1].strip())
        gastos = json.loads(lines[3].split(": ", 1)[1].strip())
    
    total_gastos = sum(gastos.values())
    if presupuesto > 0:
        porcentaje_gastado = (total_gastos * 100) / presupuesto
    else:
        porcentaje_gastado = 0

    reporte = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "presupuesto": presupuesto,
        "total_gastos": total_gastos,
        "porcentaje_gastado": porcentaje_gastado,  
        "detalle_gastos": gastos
    }
    
    guardar_reporte(user_path, reporte)

    print("\n--- Reporte de gastos ---")
    print(f"Presupuesto: {presupuesto:.2f}")
    print(f"Total de gastos: {total_gastos:.2f}")
    print(f"Porcentaje gastado: {porcentaje_gastado:.2f}%\n")
    
    if presupuesto > 0 and total_gastos > presupuesto:
        print("\n¡ADVERTENCIA! Has superado el presupuesto.")
    elif presupuesto > 0 and total_gastos > presupuesto * 0.9:
        print("¡ADVERTENCIA! Has superado el 90% de tu presupuesto.")
    
    # Genera los gráficos
    plt.figure(figsize=(12, 6))
    graficar_gastos(gastos)
    graficar_presupuesto_vs_gastos(presupuesto, gastos)
    plt.tight_layout()
    plt.show()

def ver_datos_usuario(user_path):
    # Muestra la información básica y presupuesto de un usuario autenticado.
    if not user_path:
        print("Debe iniciar sesión primero.")
        return

    with open(os.path.join(user_path, "informacion.txt"), "r") as file:
        lines = file.readlines()
        correo = lines[0].split(": ")[1].strip()
        presupuesto = lines[2].split(": ")[1].strip()
        gastos = json.loads(lines[3].split(": ", 1)[1].strip())

        print("\n--- Información del usuario ---")
        print(f"Correo: {correo}")
        print(f"Presupuesto: {presupuesto}")
        print("Gastos:")
        for categoria, valor in gastos.items():
            print(f"  - {categoria}: {valor}")
def ver_historial(user_path):
    #muestra el historial de reportes del usuario identificado
    if not user_path:
        print("primero debe iniciar sesion")
        return
    historial_path=os.path.join(user_path,"historial_reportes.json")
    if not os.path.exists(historial_path):
        print("no hay reportes todavia")
        return
    with open(historial_path,"r") as file:
        historial=json.load(file)
    print("\n--- historial de reportes ---")
    for reporte in historial:
        print(f"fecha: {reporte['fecha']}")
        print(f"presupuesto: {reporte['presupuesto']:.2f}")
        print(f"total gastos: {reporte['total_gastos']:.2f}")
        print(f"porcentaje gastado: {reporte['porcentaje_gastado']:.2f}%")
        print("detalle de gastos: ")
        for categoria,valor in reporte['detalle_gastos'].items():
            print(f" - {categoria}: {valor:.2f}")
        print("-"*30)
    

def ejecutar():
    # Función principal que gestiona el menú del sistema.
    user_path = None
    while True:
        print("\n1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Registrar presupuesto")
        print("4. Ingresar gastos")
        print("5. Generar reporte de gastos con gráficos")
        print("6. ver historial de reportes")
        print("7. ver datos de usuario")
        print("8. salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            user_path = autenticar_usuario()
        elif opcion == "3":
            registrar_presupuesto(user_path)
        elif opcion == "4":
            ingresar_gastos(user_path)
        elif opcion == "5":
            generar_reporte(user_path)
        elif opcion == "6":
            ver_historial(user_path)
        elif opcion=="7":
            ver_datos_usuario(user_path)
        elif opcion=="8":
            print("adios")
            break
        else:
            print("Opción no válida.")

# Ejecutar el programa
ejecutar()
