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

def login():
    print("\n--- Inicio de sesión ---")
    try:
        username = input("Nombre de usuario: ").strip()
        password = input("Contraseña: ").strip()
        user = get_user(username)
        if user and check_password(password, user[2]):
            print("¡Bienvenido,", username + "!")
            return user
        else:
            print("Usuario o contraseña incorrectos.")
            return None
    except Exception as e:
        print(f"Error en el inicio de sesión: {e}")
        return None

def consultar_indicador(user):
    print("\n--- Consulta de Indicidores ---")
    indicadores = ['dolar', 'uf', 'euro', 'utm']
    try:
        print_menu(indicadores)
        idx = input_int("Seleccione un indicador: ", 1, len(indicadores))
        indicador = indicadores[idx - 1]
        datos = get_indicator(indicador)
        if datos and 'serie' in datos and datos['serie']:
            valor_actual = datos['serie'][0]['valor']
            fecha_actual = datos['serie'][0]['fecha'][:10]
            print(f"\nValor actual de {indicador.upper()}: {valor_actual} ({format_date(fecha_actual)})")
            try:
                save_query(user[0], indicador, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(valor_actual))
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
        for ind, fecha, valor in consultas:
            print(f"{user[1].upper()} - {ind.upper()} - {valor} ({fecha})")
    except Exception as e:
        print(f"Error al obtener el historial: {e}")

def admin_menu():
    print("\n--- Menú Administrador ---")
    while True:
        try:
            print_menu([
                "Ver historial de todas las consultas",
                "Ver usuarios y sus historiales",
                "Cerrar sesión de administrador"
            ])
            op = input_int("Seleccione una opción: ", 1, 3)
            if op == 1:
                try:
                    consultas = get_all_queries()
                    if not consultas:
                        print("No hay consultas registradas.")
                    else:
                        for username, ind, fecha, valor in consultas:
                            print(f"Usuario {username} - {ind.upper()} - {valor} ({fecha})")
                except Exception as e:
                    print(f"Error al obtener el historial general: {e}")
            elif op == 2:
                try:
                    conn = sqlite3.connect("ecodata.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, username FROM users")
                    users = cursor.fetchall()
                    conn.close()
                    if not users:
                        print("No hay usuarios registrados.")
                    else:
                        for user_id, username in users:
                            print(f"\nHistorial de {username}:")
                            try:
                                consultas = get_user_queries(user_id)
                                if not consultas:
                                    print("  Sin consultas registradas.")
                                else:
                                    for ind, fecha, valor in consultas:
                                        print(f"  {ind.upper()} - {valor} ({fecha})")
                            except Exception as e:
                                print(f"  Error al obtener historial de {username}: {e}")
                except Exception as e:
                    print(f"Error al obtener usuarios: {e}")
            elif op == 3:
                break
        except Exception as e:
            print(f"Error en el menú de administrador: {e}")

def main():
    try:
        init_db()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        sys.exit(1)
    while True:
        try:
            print("\n--- EcoData Chile ---")
            print_menu(["Registrarse", "Iniciar sesión", "Salir"])
            op = input_int("Seleccione una opción: ", 1, 3)
            if op == 1:
                register()
            elif op == 2:
                user = login()
                if user:
                    if user[1] == "admin":
                        admin_menu()
                    else:
                        while True:
                            try:
                                print("\n--- Menú Usuario ---")
                                print_menu(["Consultar indicador", "Ver historial", "Cerrar sesión"])
                                op2 = input_int("Seleccione una opción: ", 1, 3)
                                if op2 == 1:
                                    consultar_indicador(user)
                                elif op2 == 2:
                                    ver_historial(user)
                                elif op2 == 3:
                                    break
                            except Exception as e:
                                print(f"Error en el menú de usuario: {e}")
            elif op == 3:
                print("¡Hasta luego!")
                sys.exit()
        except Exception as e:
            print(f"Error general: {e}")

if __name__ == "__main__":
    main()