from pathlib import Path
from paddleocr import PaddleOCRVL
import time
import pdfplumber


def extract_text_with_paddlevl(pdf_path: Path, expediente_name: str = "default") -> dict:
    """
    Ejecuta PaddleOCR-VL sobre un PDF y devuelve texto + metadatos.

    Los resultados se guardan en:
        output/{expediente_name}/{pdf_stem}_ocr.md
        output/{expediente_name}/imgs/...
    """
    # 📁 Carpeta específica del expediente
    output_folder = Path("output") / expediente_name
    output_folder.mkdir(parents=True, exist_ok=True)

    start_time = time.time()

    result = {
        "texto_extraido": "",
        "ocr_tiempo_s": 0.0,
        "ocr_calidad": "Desconocida",
        "num_paginas": 0,
        "error": ""
    }

    try:
        # 1️⃣ Contar páginas
        with pdfplumber.open(pdf_path) as pdf:
            result["num_paginas"] = len(pdf.pages)

        # 2️⃣ Ejecutar OCR (el pipeline usa su propia lógica interna de paths)
        pipeline = PaddleOCRVL()
        output = pipeline.predict(input=str(pdf_path))

        # 3️⃣ Procesar resultados
        markdown_list = []
        markdown_images = []

        for res in output:
            md_info = res.markdown
            markdown_list.append(md_info)
            markdown_images.append(md_info.get("markdown_images", {}))

        # 4️⃣ Concatenar texto
        markdown_text = pipeline.concatenate_markdown_pages(markdown_list)

        # 5️⃣ Guardar markdown en la carpeta correcta del expediente
        mkd_file_path = output_folder / f"{pdf_path.stem}_ocr.md"
        mkd_file_path.write_text(markdown_text, encoding="utf-8")

        # 6️⃣ Guardar imágenes OCR en la carpeta correcta
        for item in markdown_images:
            if item:
                for rel_path, image in item.items():
                    print(f"🔍 DEBUG rel_path original: {rel_path}")
                    print(f"🔍 DEBUG output_folder: {output_folder}")

                    # Guardar en output/{expediente_name}/{rel_path}
                    file_path = output_folder / rel_path
                    print(f"🔍 DEBUG file_path final: {file_path}")

                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    image.save(file_path)

        # 7️⃣ Calcular métricas
        elapsed = time.time() - start_time
        result["texto_extraido"] = markdown_text
        result["ocr_tiempo_s"] = round(elapsed, 2)
        result["ocr_calidad"] = "Buena" if len(markdown_text) > 500 else "Baja"

        print(f"✅ OCR completado ({elapsed:.2f}s) → {len(markdown_text)} chars")
        print(f"📄 Guardado en: {mkd_file_path}")

    except Exception as e:
        result["error"] = str(e)
        print(f"❌ Error OCR en {pdf_path.name}: {e}")

    return result