from pathlib import Path
from detectors.content_detector import detect_content_type
from classifiers.text_classifier import classify_text_document
from classifiers.image_classifier import classify_image_document
from config import MODE, PDF_FOLDER
import sys


def main():
    """
    Orquestador principal del proyecto de clasificación documental.
    Puede ejecutar clasificación por texto o por imagen (modo multimodal).
    """
    folder = Path(PDF_FOLDER)

    if not folder.exists() or not folder.is_dir():
        print(f"❌ Carpeta no encontrada: {folder}")
        sys.exit(1)

    pdf_files = list(folder.glob("*.pdf"))
    if not pdf_files:
        print("⚠️ No se encontraron archivos PDF en la carpeta especificada.")
        sys.exit(0)

    print(f"\n📂 Analizando {len(pdf_files)} documentos en {folder}")
    print(f"⚙️  Modo activo: {MODE.upper()}\n")

    for pdf_path in pdf_files:
        print(f"📄 Procesando {pdf_path.name}")

        try:
            # Detectar tipo de contenido (texto / imagen / híbrido)
            content_info = detect_content_type(pdf_path)
            print(f"   🧩 Tipo de contenido detectado: {content_info['content_type'].upper()}")

            # Selección del clasificador
            if MODE == "text":
                result = classify_text_document(pdf_path, content_info)
            elif MODE == "image":
                result = classify_image_document(pdf_path, content_info)
            else:
                print("⚠️ Modo desconocido, usa 'text' o 'image' en config.py")
                continue

            # Mostrar resultados
            if result.get("status") == "ok":
                data = result["data"]
                doc_type = data.characterizations[0].document_type
                explanation = data.characterizations[0].explanation
                print(f"   ✅ Clasificación: {doc_type}")
                print(f"   🧠 Explicación: {explanation[:200]}...\n")  # Muestra primeros 200 caracteres
            elif result.get("status") == "skipped":
                print(f"   ⚠️  Omitido: {result['reason']}\n")
            else:
                print(f"   ❌ Error inesperado: {result}\n")

        except Exception as e:
            print(f"   ❌ Error procesando {pdf_path.name}: {e}\n")


if __name__ == "__main__":
    main()
