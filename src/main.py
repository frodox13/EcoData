from database import init_db, add_user, get_user, save_query, get_user_queries, get_all_queries
from auth import hash_password, check_password
from api_client import get_indicator
from utils import format_date, print_menu, input_int
from datetime import datetime
import sys
import sqlite3

def register():
    print("\n--- Registro de usuario ---")
    try:
        username = input("Nombre de usuario: ").strip()
        password = input("Contraseña: ").strip()
        password_hash = hash_password(password)
        if add_user(username, password_hash):
            print("Usuario registrado exitosamente.")
        else:
            print("El nombre de usuario ya existe.")
    except Exception as e:
        print(f"Error en el registro: {e}")

def login(is_admin=False):
    print("\n--- Inicio de sesión ---")
    try:
        username = input("Nombre de usuario: ").strip()
        password = input("Contraseña: ").strip()
        user = get_user(username)
        if user and check_password(password, user[2]):
            if is_admin and username != "admin":
                print("Solo el usuario 'admin' puede acceder como administrador.")
                return None
            if not is_admin and username == "admin":
                print("El usuario 'admin' solo puede acceder como administrador.")
                return None
            print("¡Bienvenido,", username + "!")
            return user
        else:
            print("Usuario o contraseña incorrectos.")
            return None
    except Exception as e:
        print(f"Error en el inicio de sesión: {e}")
        return None

def consultar_indicador(user):
    print("\n--- Consulta de Indicadores ---")
    indicadores = ['dolar', 'uf', 'euro', 'utm']
    try:
        print_menu(indicadores)
        idx = input_int("Seleccione un indicador: ", 1, len(indicadores))
        indicador = indicadores[idx - 1]
        datos = get_indicator(indicador)
        if datos and 'serie' in datos and datos['serie']:
            valor_actual = datos['serie'][0]['valor']
            value_date = datos['serie'][0]['fecha'][:19].replace("T", " ")  # Fecha de actualización de la API
            query_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")      # Fecha de consulta
            print(f"\nValor actual de {indicador.upper()}: {valor_actual}")
            print(f"Fecha actualización valor: {value_date}")
            print(f"Fecha de consulta: {query_date}")
            try:
                save_query(user[0], indicador, query_date, value_date, str(valor_actual))
            except Exception as e:
                print(f"Error al guardar la consulta: {e}")
        else:
            print("No se pudo obtener el indicador.")
    except Exception as e:
        print(f"Error al consultar el indicador: {e}")

def ver_historial(user):
    print("\n--- Historial de Consultas ---")
    try:
        consultas = get_user_queries(user[0])
        if not consultas:
            print("No hay consultas registradas.")
            return
        for ind, query_date, value_date, valor in consultas:
            print(f"{user[1].upper()} - {ind.upper()} - {valor} (Consulta: {query_date} | Actualización: {value_date})")
    except Exception as e:
        print(f"Error al obtener el historial: {e}")

def ver_historial_global():
    print("\n--- Historial Global de Consultas ---")
    try:
        consultas = get_all_queries()
        if not consultas:
            print("No hay consultas registradas.")
        else:
            for username, ind, query_date, value_date, valor in consultas:
                print(f"Usuario {username} - {ind.upper()} - {valor} (Consulta: {query_date} | Actualización: {value_date})")
    except Exception as e:
        print(f"Error al obtener el historial global: {e}")

def crear_admin_por_defecto():
    # Crea el usuario admin si no existe
    if not get_user("admin"):
        password_hash = hash_password("admin")
        add_user("admin", password_hash)

def main():
    try:
        init_db()
        crear_admin_por_defecto()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        sys.exit(1)

    while True:
        print("\n--- EcoData Chile ---")
        print_menu(["Administrador", "Usuario regular", "Salir"])
        tipo_usuario = input_int("Seleccione el tipo de usuario: ", 1, 3)
        if tipo_usuario == 1:
            # Administrador
            while True:
                print_menu(["Iniciar sesión", "Salir"])
                op = input_int("Seleccione una opción: ", 1, 2)
                if op == 1:
                    user = login(is_admin=True)
                    if user:
                        while True:
                            print("\n--- Menú Administrador ---")
                            print_menu([
                                "Consultar indicador",
                                "Ver historial global de consultas",
                                "Cerrar sesión"
                            ])
                            op_admin = input_int("Seleccione una opción: ", 1, 3)
                            if op_admin == 1:
                                consultar_indicador(user)
                            elif op_admin == 2:
                                ver_historial_global()
                            elif op_admin == 3:
                                break
                        break
                elif op == 2:
                    break
        elif tipo_usuario == 2:
            # Usuario regular
            while True:
                print_menu(["Registrarse", "Iniciar sesión", "Salir"])
                op = input_int("Seleccione una opción: ", 1, 3)
                if op == 1:
                    register()
                elif op == 2:
                    user = login(is_admin=False)
                    if user:
                        while True:
                            print("\n--- Menú Usuario ---")
                            print_menu(["Consultar indicador", "Ver historial", "Cerrar sesión"])
                            op2 = input_int("Seleccione una opción: ", 1, 3)
                            if op2 == 1:
                                consultar_indicador(user)
                            elif op2 == 2:
                                ver_historial(user)
                            elif op2 == 3:
                                break
                        break
                elif op == 3:
                    break
        elif tipo_usuario == 3:
            print("¡Hasta luego!")
            sys.exit()

if __name__ == "__main__":
    main()