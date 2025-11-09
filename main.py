from pathlib import Path
from detectors.content_detector import detect_content_type
from classifiers.text_classifier import classify_text_document
from classifiers.image_classifier import classify_image_document
from config import MODE, PDF_FOLDER, USE_LOCAL_MODEL, MODEL_IMAGE
from utils.reporting import init_report, append_record
import sys
import time


def main():
    """
    Orquestador principal del proyecto de clasificación documental.
    """
    print("🔧 Configuración activa:")
    print(f"   MODE = {MODE}")
    print(f"   USE_LOCAL_MODEL = {USE_LOCAL_MODEL}")
    print(f"   MODEL_IMAGE = {MODEL_IMAGE}")
    print(f"   Carpeta PDF_FOLDER = {PDF_FOLDER}\n")

    start_global = time.time()
    init_report()

    folder = Path(PDF_FOLDER)

    if not folder.exists() or not folder.is_dir():
        print(f"❌ Carpeta no encontrada: {folder}")
        sys.exit(1)

    pdf_files = list(folder.glob("*.pdf"))
    if not pdf_files:
        print("⚠️ No se encontraron archivos PDF.")
        sys.exit(0)

    print(f"\n📂 Analizando {len(pdf_files)} documentos en {folder}")

    for pdf_path in pdf_files:
        print(f"📄 Procesando {pdf_path.name}")
        start_doc = time.time()

        try:
            # 1️⃣ Detectar tipo de contenido
            content_info = detect_content_type(pdf_path)
            print(f"   🧩 Tipo: {content_info['content_type'].upper()}")

            # 2️⃣ Clasificar según MODE
            if MODE == "text":
                result = classify_text_document(pdf_path, content_info=content_info)
            elif MODE == "image":
                result = classify_image_document(pdf_path, content_info)
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

                # Datos del LLM
                if isinstance(data, dict):
                    record["tipo_documento"] = data.get("document_type", "Desconocido")
                    record["llm_tiempo_s"] = data.get("llm_time_s", 0.0)
                    explanation = data.get("explanation", "")
                else:
                    # Si data es objeto Classification
                    record["tipo_documento"] = data.characterizations[0].document_type
                    explanation = data.characterizations[0].explanation

                # Datos del OCR (si existen)
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

            # 5️⃣ Guardar en CSV
            append_record(record)

        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            append_record({
                "id": hash(pdf_path.name) % (10 ** 8),
                "nombre_archivo": pdf_path.name,
                "extension": pdf_path.suffix,
                "estado": "error",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            })

    elapsed = time.time() - start_global
    print(f"\n⏱️  Tiempo total: {elapsed:.2f}s")


if __name__ == "__main__":
    main()