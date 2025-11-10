import csv
import time
from pathlib import Path
from typing import Dict, Any

# 📂 Carpeta base para todos los reportes
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# 📋 Campos del CSV
CSV_FIELDS = [
    "id", "nombre_archivo", "extension", "num_paginas",
    "tipo_contenido", "tipo_documento",
    "ocr_tiempo_s", "llm_tiempo_s",
    "ocr_calidad", "extraccion_calidad",
    "ocr_modo", "estado",
    "error", "timestamp"
]


def get_report_path(expediente_name: str = None) -> Path:
    """
    Devuelve la ruta del reporte CSV para un expediente.
    Si no se especifica expediente, devuelve el reporte global.
    """
    if expediente_name:
        return OUTPUT_DIR / f"reporte_{expediente_name}.csv"
    return OUTPUT_DIR / "reporte_global.csv"


def init_report(expediente_name: str = None):
    """
    Inicializa el archivo CSV del expediente o el global.
    Crea encabezados si el archivo no existe.
    """
    path = get_report_path(expediente_name)
    path.parent.mkdir(exist_ok=True)

    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def append_record(record: Dict[str, Any], expediente_name: str = None):
    """
    Agrega un registro (fila) al CSV del expediente correspondiente.
    Convierte `None` en string vacío para evitar errores.
    """
    path = get_report_path(expediente_name)
    filtered = {k: (record.get(k) or "") for k in CSV_FIELDS}

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(filtered)


def consolidate_reports():
    """
    Consolida todos los reportes individuales en un único reporte global.
    """
    global_path = get_report_path(None)
    init_report(None)

    with open(global_path, "a", newline="", encoding="utf-8") as global_file:
        writer = csv.DictWriter(global_file, fieldnames=CSV_FIELDS)

        for file_path in OUTPUT_DIR.glob("reporte_*.csv"):
            if file_path.name == "reporte_global.csv":
                continue  # Evita recursión

            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    writer.writerow(row)

    print(f"📊 Reporte global consolidado en: {global_path.name}")


class Timer:
    """Context manager para medir tiempos de ejecución."""
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.elapsed = self.end - self.start
