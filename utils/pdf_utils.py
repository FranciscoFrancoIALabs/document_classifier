import tempfile
from pdf2image import convert_from_path
from pathlib import Path


def pdf_to_images(pdf_path: Path, output_folder: Path = None) -> list[Path]:
    """
    Convierte cada página de un PDF en imágenes JPEG.
    Devuelve una lista de rutas a las imágenes generadas.
    """
    if output_folder is None:
        output_folder = Path(tempfile.mkdtemp())

    images = convert_from_path(pdf_path)
    image_paths = []

    for i, page in enumerate(images, start=1):
        image_path = output_folder / f"{pdf_path.stem}_page_{i}.jpeg"
        page.save(image_path, "JPEG")
        image_paths.append(image_path)

    return image_paths