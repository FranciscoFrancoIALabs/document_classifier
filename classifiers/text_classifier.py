from openai import OpenAI
import pdfplumber
import time
from pathlib import Path
from prompts.base_prompts import PROMPT_TEXT_CLASSIFICATION as PROMPT_BASE
from config import MODEL_TEXT, BASE_URL, TEXT_TRUNCATE_LIMIT
from models import Classification

client = OpenAI(base_url=BASE_URL)

def classify_text_document(pdf_path: Path, text: str = None, content_info: dict = None) -> dict:
    """
    Clasifica un documento por su texto y devuelve un resultado plano compatible con el pipeline.
    """
    start = time.time()

    try:
        # 1️⃣ Obtener texto
        if text is None:
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        if not text.strip():
            return {"status": "error", "reason": "Texto vacío"}

        # 2️⃣ Truncar texto si es muy largo
        text_truncated = text[:TEXT_TRUNCATE_LIMIT]

        # 3️⃣ Llamar al modelo con estructura pydantic
        messages = [
            {"role": "system", "content": "Eres un experto en clasificación documental."},
            {
                "role": "user",
                "content": f"{PROMPT_BASE}\n\nContenido:\n{text_truncated}",
            },
        ]

        completion = client.chat.completions.parse(
            model=MODEL_TEXT,
            messages=messages,
            response_format=Classification,
        )

        elapsed = time.time() - start
        msg = completion.choices[0].message

        # 4️⃣ Manejar rechazo
        if msg.refusal:
            return {"status": "refused", "reason": msg.refusal}

        parsed = msg.parsed
        # Si hay una sola caracterización (lo normal)
        char = parsed.characterizations[0] if parsed.characterizations else None

        # 5️⃣ Devolver el mismo formato esperado por el pipeline
        return {
            "status": "ok",
            "data": {
                "document_type": char.document_type if char else "Otros",
                "explanation": char.explanation if char else "Sin explicación generada.",
                "llm_time_s": round(elapsed, 2),
            },
        }

    except Exception as e:
        return {"status": "error", "reason": str(e)}
