from pydantic import BaseModel, Field
from typing import List, Optional

class Characterization(BaseModel):
    """
    Representa una caracterización individual de un documento:
    - Tipo de documento (ej: Resolución, Plano, etc.)
    - Tipo de contenido (texto, imagen, híbrido)
    - Explicación generada por el modelo
    """
    document_type: str = Field(..., description="Categoría principal del documento.")
    content_type: str = Field(..., description="Tipo de contenido analizado (text, image, hybrid).")
    explanation: str = Field(..., description="Razonamiento o justificación del modelo.")

class Classification(BaseModel):
    """
    Resultado estructurado devuelto por el modelo.
    Puede incluir varias caracterizaciones si el documento tiene múltiples secciones.
    """
    characterizations: List[Characterization] = Field(..., description="Lista de caracterizaciones detectadas.")
    ocr_quality: Optional[str] = Field(None, description="Calidad estimada del OCR o del texto reconocido (si aplica).")
