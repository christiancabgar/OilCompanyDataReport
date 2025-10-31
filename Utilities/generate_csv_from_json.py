"""
generate_csv_from_json.py

Descripción:
Este script convierte los registros JSON generados en la carpeta `set_datos_sinteticos`
en archivos CSV agrupados por tipo de dato. Se generará una nueva carpeta llamada
`set_datos_sinteticos_csv`, que contendrá subcarpetas equivalentes a las originales
(PRO-ICF, PRO-IM, PRO-OCF, PRO-OM). Dentro de cada una, se guardará un único CSV
que consolidará todos los registros JSON de la carpeta correspondiente.

Estructura esperada:
set_datos_sinteticos/
 ├── PRO-ICF/
 │    ├── 20220801-PRO-ICF.json
 │    ├── 20220802-PRO-ICF.json
 │    └── ...
 ├── PRO-IM/
 │    ├── ...

Salida:
set_datos_sinteticos_csv/
 ├── PRO-ICF/PRO-ICF.csv
 ├── PRO-IM/PRO-IM.csv
 ├── PRO-OCF/PRO-OCF.csv
 └── PRO-OM/PRO-OM.csv

El script aplana de forma recursiva las estructuras JSON para que cada campo anidado
se convierta en una columna del CSV, con nombres tipo `data.value1`, `meta.source`, etc.

Uso:
  python3 Utilities/generate_csv_from_json.py
"""

import os
import json
import csv
from typing import Any, Dict

BASE_DIR = "C:\\Users\\chris\\Personal\\Universidad\\Prácticas externas\\Proyectos\\OilCompanyDataReport"
INPUT_DIR = os.path.join(BASE_DIR, "set_datos_sinteticos_json")
OUTPUT_DIR = os.path.join(BASE_DIR, "set_datos_sinteticos_csv")

# -----------------------------
# Funciones auxiliares
# -----------------------------

def flatten_json(y: Dict[str, Any], prefix: str = "", sep: str = ".") -> Dict[str, Any]:
    """Aplana un JSON anidado en un diccionario plano con claves tipo 'a.b.c'"""
    out = {}

    def _flatten(x: Any, name: str = ""):
        if isinstance(x, dict):
            for a in x:
                _flatten(x[a], f"{name}{a}{sep}")
        elif isinstance(x, list):
            for i, a in enumerate(x):
                _flatten(a, f"{name}{i}{sep}")
        else:
            out[name[:-1]] = x

    _flatten(y, prefix)
    return out

def process_folder(input_folder: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    files = [f for f in os.listdir(input_folder) if f.lower().endswith('.json')]

    all_rows = []
    for file in sorted(files):
        path = os.path.join(input_folder, file)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            flat = flatten_json(data)
            flat['source_file'] = file  # mantener referencia al archivo original
            all_rows.append(flat)
        except Exception as e:
            print(f"Error leyendo {file}: {e}")

    if not all_rows:
        print(f"No se encontraron archivos JSON en {input_folder}")
        return

    # obtener todas las columnas únicas
    fieldnames = sorted(set().union(*[row.keys() for row in all_rows]))

    # nombre del CSV basado en la carpeta
    folder_name = os.path.basename(input_folder.rstrip(os.sep))
    output_csv = os.path.join(output_folder, f"{folder_name}.csv")

    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"CSV generado: {output_csv} ({len(all_rows)} registros)")

# -----------------------------
# Ejecución principal
# -----------------------------

def main():
    if not os.path.isdir(INPUT_DIR):
        print(f"No se encontró el directorio de entrada: {INPUT_DIR}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    folders = [f for f in os.listdir(INPUT_DIR) if os.path.isdir(os.path.join(INPUT_DIR, f))]

    if not folders:
        print("No se encontraron subcarpetas en set_datos_sinteticos.")
        return

    for folder in folders:
        input_folder = os.path.join(INPUT_DIR, folder)
        output_folder = os.path.join(OUTPUT_DIR, folder)
        process_folder(input_folder, output_folder)

if __name__ == '__main__':
    main()
