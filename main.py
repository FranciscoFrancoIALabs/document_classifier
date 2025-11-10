from pathlib import Path
from detectors.content_detector import detect_content_type
from classifiers.text_classifier import classify_text_document
from classifiers.image_classifier import classify_image_document
from config import MODE, PDF_FOLDER, USE_LOCAL_MODEL, MODEL_IMAGE
from utils.reporting import init_report, append_record, consolidate_reports
import sys
import time


def process_folder(folder_path: Path, global_start_time: float):
    """
    Procesa todos los PDFs dentro de una carpeta individual (expediente).
    """
    print(f"\n📁 Procesando expediente: {folder_path.name}")
    init_report(folder_path.name)

    pdf_files = list(folder_path.glob("*.pdf"))
    if not pdf_files:
        print(f"⚠️  No se encontraron archivos PDF en {folder_path}")
        return

    for pdf_path in pdf_files:
        print(f"📄 Procesando {pdf_path.name}")
        start_doc = time.time()

        try:
            # 1️⃣ Detectar tipo de contenido
            content_info = detect_content_type(pdf_path)
            print(f"   🧩 Tipo: {content_info['content_type'].upper()}")

            # 2️⃣ Clasificar según MODE
            if MODE == "text":
                # Clasificación por texto embebido (no necesita expediente_name)
                result = classify_text_document(pdf_path, content_info=content_info)
            elif MODE == "image":
                # Clasificación por imagen/OCR — pasa expediente_name para agrupar salidas
                result = classify_image_document(pdf_path, content_info, expediente_name=folder_path.name)
            else:
                print("⚠️ MODE debe ser 'text' o 'image'")
                continue

            # 3️⃣ Construir registro para CSV
            elapsed_doc = time.time() - start_doc

            record = {
                "id": hash(pdf_path.name) % (10 ** 8),
                "nombre_archivo": pdf_path.name,
                "extension": pdf_path.suffix,
                "num_paginas": content_info.get("total_pages", 0),
                "tipo_contenido": content_info["content_type"],
                "tipo_documento": None,
                "ocr_tiempo_s": 0.0,
                "llm_tiempo_s": 0.0,
                "ocr_calidad": "N/A",
                "extraccion_calidad": "N/A",
                "ocr_modo": "N/A",
                "estado": result["status"],
                "error": result.get("reason", ""),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            # 4️⃣ Procesar resultado
            if result["status"] == "ok":
                data = result["data"]

                if isinstance(data, dict):
                    record["tipo_documento"] = data.get("document_type", "Desconocido")
                    record["llm_tiempo_s"] = data.get("llm_time_s", 0.0)
                    explanation = data.get("explanation", "")
                else:
                    record["tipo_documento"] = data.characterizations[0].document_type
                    explanation = data.characterizations[0].explanation

                # 👇 Guardar explicación completa
                record["explicacion"] = explanation

                if "ocr_data" in result:
                    ocr_data = result["ocr_data"]
                    record["ocr_tiempo_s"] = ocr_data.get("ocr_tiempo_s", 0.0)
                    record["ocr_calidad"] = ocr_data.get("ocr_calidad", "N/A")
                    record["ocr_modo"] = "PaddleOCR-VL"

                print(f"   ✅ Clasificación: {record['tipo_documento']}")
                print(f"   🧠 Explicación: {explanation[:150]}...")
                print(f"   ⏱️  Tiempo: {elapsed_doc:.2f}s\n")

            else:
                print(f"   ⚠️  {result['status'].upper()}: {result.get('reason', 'Sin detalles')}\n")

            append_record(record, folder_path.name)

        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            append_record({
                "id": hash(pdf_path.name) % (10 ** 8),
                "nombre_archivo": pdf_path.name,
                "extension": pdf_path.suffix,
                "estado": "error",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }, folder_path.name)

    elapsed = time.time() - global_start_time
    print(f"⏱️  Expediente {folder_path.name} completado en {elapsed:.2f}s\n")


def main():
    """
    Orquestador principal del proyecto de clasificación documental.
    """
    print("🔧 Configuración activa:")
    print(f"   MODE = {MODE}")
    print(f"   USE_LOCAL_MODEL = {USE_LOCAL_MODEL}")
    print(f"   MODEL_IMAGE = {MODEL_IMAGE}")
    print(f"   Carpeta PDF_FOLDER = {PDF_FOLDER}\n")

    folder = Path(PDF_FOLDER)
    if not folder.exists() or not folder.is_dir():
        print(f"❌ Carpeta no encontrada: {folder}")
        sys.exit(1)

    # 🔹 Detectar si hay subcarpetas (expedientes)
    subfolders = [f for f in folder.iterdir() if f.is_dir()]

    start_global = time.time()

    if subfolders:
        print(f"📂 {len(subfolders)} expedientes encontrados. Procesando en lote...\n")
        for subfolder in subfolders:
            process_folder(subfolder, start_global)

        consolidate_reports()  # 🔸 Generar reporte global al final
    else:
        print("📂 Sin subcarpetas. Procesando PDFs en la raíz...\n")
        process_folder(folder, start_global)

    total_elapsed = time.time() - start_global
    print(f"\n🏁 Procesamiento total completado en {total_elapsed:.2f}s")


if __name__ == "__main__":
    main()
