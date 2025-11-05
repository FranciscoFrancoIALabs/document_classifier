from pathlib import Path

# ==============================
# 🔧 CONFIGURACIÓN GLOBAL
# ==============================

# 📂 Carpeta donde están los PDFs a analizar
PDF_FOLDER = Path("Muestras de Expedientes")

# ⚙️ Modo de ejecución
# - "text": usa el texto embebido del PDF
# - "image": procesa el documento como imagen (OCR o visión multimodal)
# - "auto": decide según el tipo de contenido detectado
MODE = "text"  # cambia a "text", "image" o "auto" según lo que quieras probar


# ==============================
# 🤖 CONFIGURACIÓN DE MODELOS
# ==============================

# Si usas un modelo local (por ejemplo, vLLM, Ollama, LM Studio)
USE_LOCAL_MODEL = True

# Modelo a usar
# - Para OpenAI: "gpt-4o-mini", "gpt-4.1", "gpt-5-nano"
# - Para LLM local: el nombre del modelo compatible (por ejemplo, "openai/gpt-oss-20b")
MODEL_TEXT = "openai/gpt-oss-20b"
MODEL_IMAGE = "gpt-5-nano"

# Base URL de la API (por defecto: OpenAI)
# Cambia si usas un servidor local (por ejemplo: http://localhost:8001/v1)
if USE_LOCAL_MODEL:
    BASE_URL = "http://localhost:8001/v1"
else:
    BASE_URL = "https://api.openai.com/v1"


# ==============================
# ⚙️ PARÁMETROS ADICIONALES
# ==============================

# Límite de caracteres del texto a enviar al modelo (para ahorrar tokens)
TEXT_TRUNCATE_LIMIT = 15000

# Carpeta temporal para imágenes generadas desde PDFs
TEMP_IMAGE_FOLDER = Path("temp_images")
TEMP_IMAGE_FOLDER.mkdir(exist_ok=True)
