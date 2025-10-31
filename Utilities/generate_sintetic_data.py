"""
generate_synthetic_records.py

Descripción:
Lee un conjunto de archivos JSON "plantilla" ubicados en carpetas:
  PRO-ICF, PRO-IM, PRO-OCF, PRO-OM
Cada carpeta debe contener un JSON tipo (ej.: 20220801-PRO-ICF.json) con la estructura
mostrada por el usuario. El script toma la fecha del primer registro encontrado
(en cualquiera de los JSON) y genera registros sintéticos diarios desde esa fecha
hasta la fecha actual (por defecto hoy). Los valores numéricos de cada campo se
modifican aleatoriamente en un rango de +/− 10 (enteros) respecto al valor
original, asegurando que los valores resultantes no sean negativos.

Salida:
  - En cada carpeta PRO-*, se generará un fichero por día con el formato:
      YYYYMMDD-PRO-ICF.json, YYYYMMDD-PRO-IM.json, etc.

Uso:
  Coloque este script en el directorio que contiene las carpetas:
    PRO-ICF, PRO-IM, PRO-OCF, PRO-OM
  y ejecute:
    python3 generate_synthetic_records.py

Notas:
  - Detecta y mantiene el formato numérico (int/float).
  - Actualiza el campo de fecha en el JSON.
"""

import json
import os
import random
from datetime import datetime, timedelta
from copy import deepcopy

# --------- CONFIG ---------
FOLDERS = ["PRO-ICF", "PRO-IM", "PRO-OCF", "PRO-OM"]
DATE_FORMATS = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
RANDOM_SEED = 42
MAX_DELTA = 10  # +/-
# --------------------------

random.seed(RANDOM_SEED)

def parse_date(s: str) -> datetime:
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            pass
    try:
        return datetime.fromisoformat(s)
    except Exception:
        raise ValueError(f"No pude parsear la fecha: {s}")

def perturb_value(v):
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, int):
        return max(0, v + random.randint(-MAX_DELTA, MAX_DELTA))
    if isinstance(v, float):
        return max(0.0, v + random.uniform(-MAX_DELTA, MAX_DELTA))
    return v

def perturb_structure(obj):
    if isinstance(obj, dict):
        return {k: perturb_structure(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [perturb_structure(x) for x in obj]
    else:
        return perturb_value(obj)

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def find_date_in_json(j):
    if isinstance(j, dict) and "data" in j and isinstance(j["data"], dict):
        if "date" in j["data"]:
            date_str = j["data"]["date"]
            return parse_date(date_str)
    for fmt in DATE_FORMATS:
        for k, v in j.items():
            if isinstance(v, str):
                try:
                    return datetime.strptime(v, fmt)
                except Exception:
                    pass
    raise ValueError("No se encontró una fecha en el JSON.")

def load_templates(base_path="."):
    templates = {}
    for folder in FOLDERS:
        folder_path = os.path.join(base_path, folder)
        if not os.path.isdir(folder_path):
            continue
        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.json')]
        if not files:
            continue
        filepath = os.path.join(folder_path, files[0])
        templates[folder] = load_json(filepath)
    return templates

def update_date_field(j, date_obj):
    date_str = date_obj.strftime("%d/%m/%Y")
    if isinstance(j, dict) and "data" in j and isinstance(j["data"], dict):
        j["data"]["date"] = date_str
    return j

def generate_synthetic_files(templates, start_date, end_date, base_path="."):
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        for folder, tmpl in templates.items():
            perturbed = perturb_structure(deepcopy(tmpl))
            perturbed = update_date_field(perturbed, current_date)
            filename = f"{date_str}-{folder}.json"
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            output_path = os.path.join(folder_path, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(perturbed, f, ensure_ascii=False, indent=2)
        current_date += timedelta(days=1)

def main(base_path="C:\\Users\\chris\\Personal\\Universidad\\Prácticas externas\\Proyectos\\OilCompanyDataReport\\set_datos_sinteticos"):
    templates = load_templates(base_path)
    if not templates:
        print("No se encontraron plantillas JSON en las carpetas especificadas.")
        return

    dates = []
    for folder, tmpl in templates.items():
        try:
            dates.append(find_date_in_json(tmpl))
        except Exception as e:
            print(f"Advertencia: no se pudo obtener la fecha de {folder}: {e}")

    if not dates:
        print("No se pudo determinar la fecha inicial.")
        return

    start_date = min(dates)
    end_date = datetime.now()

    print(f"Generando archivos desde {start_date.date()} hasta {end_date.date()}...")
    generate_synthetic_files(templates, start_date, end_date, base_path)
    print("Generación completada.")

if __name__ == '__main__':
    main()
