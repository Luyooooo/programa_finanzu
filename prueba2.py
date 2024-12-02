import os
import json

# Directorio base donde se guardarán las carpetas de los usuarios
BASE_DIR = "usuarios"

# Crea el directorio base si no existe
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)
    print(f"Directorio base creado: {BASE_DIR}")
else:
    print(f"Directorio base ya existe: {BASE_DIR}")

def registrar_usuario():
    #Registra un nuevo usuario creando una carpeta con su información básica.
    nombre_usuario = input("Ingrese un nombre de usuario: ")
    user_path = os.path.join(BASE_DIR, nombre_usuario)
    print(f"Ruta del usuario: {user_path}")

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
    #Autentica a un usuario existente verificando su contraseña.
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    user_path = os.path.join(BASE_DIR, nombre_usuario)
    print(f"Ruta del usuario: {user_path}")

    if not os.path.exists(user_path):
        print("El usuario no existe.")
        return None

    contraseña = input("Ingrese su contraseña: ")

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
    #Permite registrar o actualizar el presupuesto de un usuario autenticado.
    if not user_path:
        print("Debe iniciar sesión primero.")
        return

    print(f"Ruta del usuario: {user_path}")

    try:
        presupuesto = float(input("Ingrese el monto de su presupuesto: "))
        with open(os.path.join(user_path, "informacion.txt"), "r+") as file:
            lines = file.readlines()
            lines[2] = f"Presupuesto: {presupuesto}\n"  # Actualiza el presupuesto
            file.seek(0)
            file.writelines(lines)

        print("Presupuesto registrado exitosamente.")
    except ValueError:
        print("Monto inválido. Intente nuevamente.")

def ingresar_gastos(user_path):
    #Permite al usuario ingresar y registrar gastos categorizados.
    if not user_path:
        print("Debe iniciar sesión primero.")
        return

    print(f"Ruta del usuario: {user_path}")

    try:
        # Leer los datos existentes
        with open(os.path.join(user_path, "informacion.txt"), "r+") as file:
            lines = file.readlines()
            gastos = json.loads(lines[3].split(": ", 1)[1].strip())

        while True:
            categoria = input("Ingrese la categoría del gasto (o 'salir' para terminar): ")
            if categoria.lower() == "salir":
                break

            valor = float(input(f"Ingrese el valor del gasto en {categoria}: "))
            if categoria in gastos:
                gastos[categoria] += valor
            else:
                gastos[categoria] = valor

        # Actualizar los gastos en el archivo
        with open(os.path.join(user_path, "informacion.txt"), "r+") as file:
            lines[3] = f"Gastos: {json.dumps(gastos)}\n"
            file.seek(0)
            file.writelines(lines)

        print("Gastos registrados exitosamente.")
    except ValueError:
        print("Valor inválido. Intente nuevamente.")

def ver_datos_usuario(user_path):
    #Muestra la información básica y presupuesto de un usuario autenticado.
    if not user_path:
        print("Debe iniciar sesión primero.")
        return

    print(f"Ruta del usuario: {user_path}")

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

def ver_historial_mensual(user_path):
    # Muestra el historial de gastos mensual de un usuario autenticado.
    if not user_path:
        print("Debe iniciar sesión primero.")
        return

    print(f"Ruta del usuario: {user_path}")

    with open(os.path.join(user_path, "informacion.txt"), "r") as file:
        lines = file.readlines()
        gastos = json.loads(lines[3].split(": ", 1)[1].strip())

        print("\n--- Historial de gastos mensual ---")
        for categoria, valor in gastos.items():
            print(f"  - {categoria}: {valor}")

def ejecutar():
    #Función principal que gestiona el menú del sistema.
    user_path = None
    print("Iniciando el programa...")
    while True:
        print("\n1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Registrar presupuesto")
        print("4. Ingresar gastos")
        print("5. Ver datos del usuario")
        print("6. Ver historial de gastos mensual")
        print("7. Salir")

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
            ver_datos_usuario(user_path)
        elif opcion == "6":
            ver_historial_mensual(user_path)
        elif opcion == "7":
            print("Adiós.")
            break
        else:
            print("Opción no válida.")

# Ejecutar el programa
ejecutar()