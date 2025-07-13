# EcoData

## Descripcion del proyecto

Aplicación que permite a sus usuarios consultar los principales indicadores económicos del país y guardar sus consultas para análisis posterior.

- Programación orientada a objetos (POO)
- Conexión a base de datos (SQLite)
- Operaciones CRUD
- Consumo de API externa
- Deserialización de JSON
- Registro de datos en base de datos

## Estructura del Repositorio
```

EcoData/
├── README.md             # Documentacion del proyecto
├── requirements.txt      # Dependencias del proyecto
└── src/
    ├── main.py           # Archivo principal del sistema
    ├── api_client.py     # Api utilizada en el sistema
    ├── database.py       # Base de datos del sistema
    ├── auth.py           # Autentificador y generador de hash
    └── utils.py          # Utilidades del sistema

```
## Instalacion y uso
1. Clonar repositorio:
    ```bash
    git clone https://github.com/frodox13/EcoData.git
    ```
2. Navegar al Directorio del proyecto:
    ```bash
    cd EcoData
    ```
3. Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4. Ejecutar la aplicación:
    ```bash
    python main.py
    ```