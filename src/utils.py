from datetime import datetime

def format_date(date_str: str) -> str:
    # Formatea una fecha ISO (YYYY-MM-DD) a DD/MM/YYYY.
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return date_str

def print_menu(options):
    # Imprime un menú numerado a partir de una lista de opciones.
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")

def input_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    # Solicita un entero al usuario, validando rango si se especifica.
    while True:
        try:
            value = int(input(prompt))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print("Valor fuera de rango.")
                continue
            return value
        except ValueError:
            print("Por favor, ingrese un número entero.")
