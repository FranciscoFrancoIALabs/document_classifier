from openai import OpenAI
import pdfplumber
import time
from pathlib import Path
from models import Classification
from config import MODEL_TEXT, BASE_URL, TEXT_TRUNCATE_LIMIT

client = OpenAI(base_url=BASE_URL)

PROMPT_BASE = (
    "CLASIFICA este documento en una de las siguientes categorías:\n"
    "Resolucion, Plano, Escritura, Croquis, Documento de Apoyo u Otros.\n"
    "Explica brevemente las razones de tu decisión."
)


def classify_text_document(pdf_path: Path, text: str = None, content_info: dict = None) -> dict:
    """
    Clasifica un documento por su texto.

    Args:
        pdf_path: Ruta al PDF
        text: Texto extraído (puede venir de OCR o ser None para extraerlo del PDF)
        content_info: Info adicional del documento

    Returns:
        dict con status, data (document_type, explanation, llm_time_s)
    """
    start = time.time()

    try:
        # 1️⃣ Obtener texto
        if text is None:
            # Extraer de PDF embebido
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        if not text.strip():
            return {"status": "error", "reason": "Texto vacío"}

        # 2️⃣ Truncar texto si es muy largo
        text_truncated = text[:TEXT_TRUNCATE_LIMIT]

        # 3️⃣ Llamar al LLM
        messages = [
            {"role": "system", "content": "Eres un experto en clasificación documental."},
            {
                "role": "user",
                "content": f"{PROMPT_BASE}\n\nContenido:\n{text_truncated}",
            },
        ]

        completion = client.chat.completions.create(
            model=MODEL_TEXT,
            messages=messages,
        )

        elapsed = time.time() - start

        # 4️⃣ Parsear respuesta
        msg = completion.choices[0].message
        full_text = msg.content.strip()

        # Detectar categoría en el texto
        categorias = ["Resolucion", "Plano", "Escritura", "Croquis", "Documento de Apoyo", "Otros"]
        detected = next((c for c in categorias if c.lower() in full_text.lower()), "Otros")

        return {
            "status": "ok",
            "data": {
                "document_type": detected,
                "explanation": full_text,
                "llm_time_s": round(elapsed, 2),
            },
        }

    except Exception as e:
        return {"status": "error", "reason": str(e)}