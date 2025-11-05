from openai import OpenAI
import pdfplumber
from pathlib import Path
from models import Classification
from config import MODEL_TEXT, BASE_URL

client = OpenAI(base_url=BASE_URL)

# 🧠 Prompt base (idéntico al del modelo de imagen para coherencia conceptual)
PROMPT_BASE = (
    "CLASIFICA este documento en UNA de estas categorías específicas:\n\n"
    "CATEGORÍAS VÁLIDAS (usa EXACTAMENTE estos nombres):\n"
    "- 'Resolucion' (para documentos legales, resoluciones administrativas)\n"
    "- 'Plano' (para planos prediales, cartográficos, topográficos)\n"
    "- 'Escritura' (para documentos notariales, contratos, títulos de propiedad)\n"
    "- 'Croquis' (para dibujos simples, bosquejos, diagramas)\n"
    "- 'Documento de Apoyo' (para tablas, listados, bases de datos, informes)\n"
    "- 'Otros' (para cualquier otro tipo no cubierto)\n\n"
    "PALABRAS CLAVE Y SEÑALES PARA CADA CATEGORÍA:\n"
    "Resolucion - Busca: 'RESOLUCIÓN', 'DECRETO', 'ACUERDO', 'ACTA', 'ARTÍCULO', 'RESUELVE'\n"
    "Plano - Busca: 'PLANO', 'COORDENADAS', 'ESCALA', 'LEVANTAMIENTO', 'LINDEROS', 'ÁREA'\n"
    "Escritura - Busca: 'ESCRITURA', 'NOTARÍA', 'CONTRATO', 'PROPIEDAD', 'DOMINIO'\n"
    "Croquis - Busca: 'CROQUIS', 'BOSQUEJO', 'ESQUEMA', 'DIBUJO', 'MAQUETA'\n"
    "Documento de Apoyo - Busca: 'TABLA', 'LISTADO', 'INFORME', 'BASE DE DATOS', 'REGISTRO'\n\n"
    "REGLAS:\n"
    "1️⃣ Prioriza coincidencias exactas de palabras clave.\n"
    "2️⃣ Si tiene estructura legal (artículos, considerandos) → Resolucion.\n"
    "3️⃣ Si hay coordenadas o escalas → Plano.\n"
    "4️⃣ Si parece acta notarial o escritura → Escritura.\n"
    "5️⃣ Si tiene tablas o datos numéricos → Documento de Apoyo.\n\n"
    "ANALIZA AHORA ESTE DOCUMENTO:"
)


def classify_text_document(pdf_path: Path, content_info: dict) -> dict:
    """
    Clasifica un documento basado en su contenido textual embebido.
    Solo procesa documentos de tipo 'text' o 'hybrid'.
    """
    try:
        # ⚠️ Solo texto o híbrido
        if content_info["content_type"] not in ("text", "hybrid"):
            return {
                "status": "skipped",
                "reason": f"Documento '{pdf_path.name}' omitido (no contiene texto o es solo imagen)."
            }

        # 1️⃣ Extraer texto embebido
        with pdfplumber.open(pdf_path) as pdf:
            full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        if not full_text.strip():
            return {
                "status": "skipped",
                "reason": f"Documento '{pdf_path.name}' sin texto legible."
            }

        # 2️⃣ Preparar mensajes para el modelo
        messages = [
            {
                "role": "system",
                "content": (
                    "Eres un experto en análisis documental. "
                    "Clasifica documentos administrativos, catastrales y notariales "
                    "basándote SOLO en el texto embebido, sin aplicar OCR ni suposiciones visuales."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT_BASE},
                    {"type": "text", "text": f"Tipo de contenido detectado: {content_info['content_type']}"},
                    {"type": "text", "text": f"CONTENIDO DEL DOCUMENTO:\n\n{full_text}"},
                ],
            },
        ]

        # 3️⃣ Llamada al modelo
        completion = client.chat.completions.parse(
            model=MODEL_TEXT,
            messages=messages,
            response_format=Classification,
        )

        classification = completion.choices[0].message

        # 4️⃣ Manejar respuesta
        if classification.refusal:
            return {"status": "refused", "reason": classification.refusal}

        parsed = classification.parsed
        parsed.characterizations[0].content_type = content_info["content_type"]

        return {"status": "ok", "data": parsed}

    except Exception as e:
        return {"status": "error", "reason": str(e)}
