import requests

BASE_URL = "https://mindicador.cl/api"

def get_indicator(indicator: str):
    """
    Obtiene los datos actuales e históricos de un indicador económico desde la API de mindicador.cl

    Args:
        indicator (str): Nombre del indicador (ej: 'dolar', 'uf', etc.)

    Returns:
        dict: Datos del indicador o None si hay error.
    """
    url = f"{BASE_URL}/{indicator}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al consultar la API: {e}")
        return None