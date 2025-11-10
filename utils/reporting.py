import csv
import time
from pathlib import Path
from typing import Dict, Any

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

CSV_FIELDS = [
    "id", "nombre_archivo", "extension", "num_paginas",
    "tipo_contenido", "tipo_documento",
    "ocr_tiempo_s", "llm_tiempo_s",
    "ocr_calidad", "extraccion_calidad",
    "ocr_modo", "estado",
    "error", "explicacion", "timestamp"  # 👈 Nueva columna
]


def get_report_path(expediente_name: str = None) -> Path:
    """
    Devuelve la ruta del CSV.
    - Si expediente_name: output/{expediente_name}/reporte_{expediente_name}.csv
    - Si None: output/reporte_global.csv
    """
    if expediente_name:
        expediente_dir = OUTPUT_DIR / expediente_name
        expediente_dir.mkdir(parents=True, exist_ok=True)
        return expediente_dir / f"reporte_{expediente_name}.csv"
    return OUTPUT_DIR / "reporte_global.csv"


def init_report(expediente_name: str = None):
    """Inicializa el CSV con headers si no existe."""
    path = get_report_path(expediente_name)

    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def append_record(record: Dict[str, Any], expediente_name: str = None):
    """Agrega un registro al CSV del expediente."""
    path = get_report_path(expediente_name)
    filtered = {k: (record.get(k) or "") for k in CSV_FIELDS}

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(filtered)


def consolidate_reports():
    """Consolida todos los reportes individuales en reporte_global.csv"""
    global_path = get_report_path(None)
    init_report(None)

    # Buscar CSVs dentro de subcarpetas de expedientes
    expediente_dirs = [d for d in OUTPUT_DIR.iterdir() if d.is_dir()]

    with open(global_path, "a", newline="", encoding="utf-8") as global_file:
        writer = csv.DictWriter(global_file, fieldnames=CSV_FIELDS)

        for exp_dir in expediente_dirs:
            csv_file = exp_dir / f"reporte_{exp_dir.name}.csv"
            if csv_file.exists():
                with open(csv_file, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        writer.writerow(row)

    print(f"📊 Reporte global consolidado: {global_path}")


class Timer:
    """Context manager para medir tiempos."""
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.elapsed = self.end - self.start