from openai import OpenAI
from pathlib import Path
import shutil
import tempfile
from utils.pdf_utils import pdf_to_images
from utils.encoding import encode_image_to_base64
from models import Classification
from config import MODEL_IMAGE, BASE_URL


client = OpenAI(base_url=BASE_URL)


def classify_image_document(pdf_path: Path, content_info: dict) -> dict:
    """
    Clasifica un documento PDF usando análisis visual (imagen).
    Convierte el PDF a imágenes y procesa la primera página.
    """
    try:
        # 1️⃣ Convertir PDF → imágenes persistentes
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            image_paths = pdf_to_images(pdf_path, output_folder=temp_dir_path)

            if not image_paths:
                return {"status": "error", "reason": "No se pudo convertir el PDF a imágenes."}

            # Copiar la primera imagen a un lugar persistente para depuración
            first_image = image_paths[0]
            persistent_copy = Path("output_images")
            persistent_copy.mkdir(exist_ok=True)
            dst = persistent_copy / Path(pdf_path.stem + "_page_1.jpeg")
            shutil.copy(first_image, dst)

        # 2️⃣ Codificar la imagen a base64
        try:
            base64_image = encode_image_to_base64(dst)
        except Exception as e:
            print(f"❌ Error al codificar imagen '{dst.name}': {e}")
            return {"status": "error", "reason": f"Error al codificar imagen: {e}"}

        # 3️⃣ Preparar prompt y mensajes
        messages = [
            {
                "role": "system",
                "content": (
                    "Eres un asistente experto en clasificación documental. "
                    "Analiza visualmente la imagen del documento y clasifícala en UNA de las siguientes categorías: "
                    "Resolucion, Plano, Escritura, Croquis, Documento de Apoyo u Otros. "
                    "Basate en texto visible, diagramas, sellos, estructuras y elementos visuales. "
                    "Si no hay suficiente información visual, indica 'Otros'."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Clasifica visualmente el documento y explica tu decisión."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ]

        # 4️⃣ Ejecutar modelo
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
