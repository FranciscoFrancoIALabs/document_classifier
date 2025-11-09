import pdfplumber
from pathlib import Path


def detect_content_type(pdf_path: Path) -> dict:
    """
    Analiza un PDF y determina su tipo de contenido:
    - 'text'   → si todas las páginas tienen texto embebido.
    - 'image'  → si todas las páginas son imágenes sin texto.
    - 'hybrid' → si mezcla texto e imágenes.

    Retorna un diccionario con:
        {
            "file": str,
            "content_type": str,
            "text_pages": list[int],
            "image_pages": list[int],
            "total_pages": int
        }
    """
    text_pages = []
    image_pages = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)

            for i, page in enumerate(pdf.pages, start=1):
                has_text = bool(page.extract_text() and page.extract_text().strip())
                has_image = len(page.images) > 0

                if has_text:
                    text_pages.append(i)
                if has_image:
                    image_pages.append(i)

        # Determinar tipo
        if len(text_pages) == total_pages:
            content_type = "text"
        elif len(text_pages) == 0:
            content_type = "image"  # Sin texto → asumimos imagen (aunque no haya images detectadas)
        else:
            content_type = "hybrid"

        return {
            "file": pdf_path.name,
            "content_type": content_type,
            "text_pages": text_pages,
            "image_pages": image_pages,
            "total_pages": total_pages
        }

    except Exception as e:
        return {
            "file": pdf_path.name,
            "content_type": "error",
            "error": str(e),
            "text_pages": [],
            "image_pages": [],
            "total_pages": 0
        }