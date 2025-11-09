import csv
import time
from pathlib import Path
from typing import Dict, Any

REPORT_PATH = Path("output/reporte_procesamiento.csv")

CSV_FIELDS = [
    "id", "nombre_archivo", "extension", "num_paginas",
    "tipo_contenido", "tipo_documento",
    "ocr_tiempo_s", "llm_tiempo_s",
    "ocr_calidad", "extraccion_calidad",
    "ocr_modo", "estado",
    "error", "timestamp"
]


def init_report():
    """Inicializa el archivo CSV con los headers."""
    REPORT_PATH.parent.mkdir(exist_ok=True)
    if not REPORT_PATH.exists():
        with open(REPORT_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def append_record(record: Dict[str, Any]):
    """
    Escribe una fila al reporte CSV.
    Solo escribe campos que existen en CSV_FIELDS.
    Convierte None a string vacío.
    """
    filtered = {k: (record.get(k) or "") for k in CSV_FIELDS}
    with open(REPORT_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(filtered)


class Timer:
    """Context manager para medir tiempos."""

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.elapsed = self.end - self.start