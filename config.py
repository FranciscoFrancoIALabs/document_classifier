from pathlib import Path

# ==============================
# 🔧 CONFIGURACIÓN GLOBAL
# ==============================

# 📂 Carpeta donde están los PDFs a analizar
PDF_FOLDER = Path("Muestras de Expedientes")

# ⚙️ Modo de ejecución:
MODE = "image"  # "text", "image" o "auto"

# ==============================
# 🤖 CONFIGURACIÓN DE MODELOS
# ==============================

USE_LOCAL_MODEL = True

if USE_LOCAL_MODEL:
    MODEL_TEXT = "openai/gpt-oss-20b"
    MODEL_IMAGE = "paddleocr-vl"
    BASE_URL = "http://localhost:8001/v1"
else:
    MODEL_TEXT = "gpt-4o-mini"
    MODEL_IMAGE = "gpt-4o-mini"
    BASE_URL = "https://api.openai.com/v1"


# ==============================
# ⚙️ PARÁMETROS ADICIONALES
# ==============================

TEXT_TRUNCATE_LIMIT = 15000
TEMP_IMAGE_FOLDER = Path("temp_images")
TEMP_IMAGE_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER = Path("output")
OUTPUT_FOLDER.mkdir(exist_ok=True)


# ==============================
# 🧩 DEPURACIÓN OPCIONAL
# ==============================
if __name__ == "__main__":
    print("🔧 CONFIGURACIÓN ACTUAL:")
    print(f"   USE_LOCAL_MODEL = {USE_LOCAL_MODEL}")
    print(f"   MODEL_TEXT      = {MODEL_TEXT}")
    print(f"   MODEL_IMAGE     = {MODEL_IMAGE}")
    print(f"   BASE_URL        = {BASE_URL}")
    print(f"   MODE            = {MODE}")