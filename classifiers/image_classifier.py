from openai import OpenAI
from pathlib import Path
from models import Classification
from config import MODEL_IMAGE, BASE_URL, USE_LOCAL_MODEL
from prompts.base_prompts import PROMPT_IMAGE_CLASSIFICATION

client = OpenAI(base_url=BASE_URL)


def classify_image_document(pdf_path: Path, content_info: dict) -> dict:
    """
    Clasifica un documento PDF usando análisis visual o OCR local.

    Flujo:
    1. Si USE_LOCAL_MODEL y MODEL_IMAGE == "paddleocr-vl":
       - Extrae texto con PaddleOCR-VL
       - Clasifica el texto con LLM
    2. Si no:
       - Convierte PDF a imagen
       - Envía a OpenAI vision API
    """
    try:
        # 🔹 Flujo local: PaddleOCR-VL → texto → LLM
        if USE_LOCAL_MODEL and MODEL_IMAGE.lower() == "paddleocr-vl":
            from ocr.paddle_vl_wrapper import extract_text_with_paddlevl
            from classifiers.text_classifier import classify_text_document

            print(f"🧩 Ejecutando OCR local (PaddleOCR-VL) sobre {pdf_path.name}...")

            ocr_result = extract_text_with_paddlevl(pdf_path)

            if ocr_result["error"]:
                return {"status": "error", "reason": ocr_result["error"], "ocr_data": ocr_result}

            if not ocr_result["texto_extraido"].strip():
                return {"status": "error", "reason": "OCR no produjo texto.", "ocr_data": ocr_result}

            # Clasificar el texto extraído
            classification_result = classify_text_document(
                pdf_path=pdf_path,
                text=ocr_result["texto_extraido"],
                content_info=content_info
            )

            # Agregar métricas OCR al resultado
            if classification_result["status"] == "ok":
                classification_result["ocr_data"] = ocr_result

            return classification_result

        # 🔹 Flujo remoto: OpenAI vision
        from utils.pdf_utils import pdf_to_images
        from utils.encoding import encode_image_to_base64
        import tempfile
        import shutil

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            image_paths = pdf_to_images(pdf_path, output_folder=temp_dir_path)

            if not image_paths:
                return {"status": "error", "reason": "No se pudo convertir el PDF a imágenes."}

            first_image = image_paths[0]
            persistent_copy = Path("output") / "temp_images"
            persistent_copy.mkdir(parents=True, exist_ok=True)
            dst = persistent_copy / f"{pdf_path.stem}_page_1.jpeg"
            shutil.copy(first_image, dst)

        base64_image = encode_image_to_base64(dst)

        messages = [
            {
                "role": "system",
                "content": (
                    PROMPT_IMAGE_CLASSIFICATION
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Clasifica visualmente el documento y explica tu decisión."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            },
        ]

        completion = client.chat.completions.parse(
            model=MODEL_IMAGE,
            messages=messages,
            response_format=Classification,
        )

        classification = completion.choices[0].message

        if classification.refusal:
            return {"status": "refused", "reason": classification.refusal}

        parsed = classification.parsed
        parsed.characterizations[0].content_type = content_info["content_type"]

        return {"status": "ok", "data": parsed}

    except Exception as e:
        return {"status": "error", "reason": str(e)}