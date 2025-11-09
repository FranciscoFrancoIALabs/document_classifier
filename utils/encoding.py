import base64
from pathlib import Path

def encode_image_to_base64(image_path: Path) -> str:
    """
    Convierte una imagen a una cadena base64 para enviar al modelo multimodal.

    Args:
        image_path (Path): ruta a la imagen (JPG, PNG, etc.)

    Returns:
        str: cadena base64 codificada
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded
    except Exception as e:
        print(f"❌ Error al codificar imagen '{image_path.name}': {e}")
        return ""
