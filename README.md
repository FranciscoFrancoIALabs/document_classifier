
---

# 🧠 Document Classifier v3 — Clasificación Multimodal de Documentos PDF

Este proyecto permite **clasificar automáticamente documentos PDF** según su tipo (Resolución, Plano, Escritura, etc.) utilizando **modelos de lenguaje y visión**.
Admite tanto **procesamiento textual** como **procesamiento visual (OCR)**, con soporte para **modelos locales (vLLM, PaddleOCR-VL)** o **OpenAI API**.

---

## 🚀 Características principales

* 🔍 **Detección automática** del tipo de contenido (texto, imagen o híbrido).
* 🧾 **Clasificación textual** mediante LLM local (GPT-OSS-20B) o remoto.
* 🖼️ **Clasificación visual / OCR** con **PaddleOCR-VL** (visión + lenguaje).
* 📊 **Reporter CSV** con métricas detalladas por documento.
* ⚙️ **Arquitectura modular**: detectores, clasificadores, OCR y utilidades independientes.
* 🔄 **Soporte local o cloud**: OpenAI API o modelos locales.
* 🧩 **Modo de ejecución configurable**: `"text"`, `"image"`, o `"auto"`.

---

## 📁 Estructura del proyecto

```
document_classifier_v3/
│
├── Dockerfile                    # Imagen base con PaddleOCR-VL
├── main.py                       # Orquestador principal
├── config.py                     # Configuración general
├── models.py                     # Esquemas de salida estructurada
├── requirements.txt              # Dependencias Python
│
├── detectors/
│   └── content_detector.py        # Detección de tipo de contenido
│
├── classifiers/
│   ├── text_classifier.py         # Clasificador por texto embebido
│   ├── image_classifier.py        # Clasificador por visión / OCR
│   └── __init__.py
│
├── ocr/
│   └── paddle_vl_wrapper.py       # Wrapper PaddleOCR-VL
│
├── utils/
│   ├── pdf_utils.py               # Conversión PDF → imagen
│   ├── encoding.py                # Funciones de codificación Base64
│   ├── reporting.py               # Generación de reportes CSV
│   └── __init__.py
│
├── Muestras de Expedientes/       # Carpeta de PDFs de ejemplo
│
└── output/                        # Carpeta para resultados y reportes
```

---

## 🐳 Construir la imagen Docker

```powershell
docker build -t document_classifier_v3 .
```

---

## 🚀 Crear y ejecutar el contenedor (GPU activada)

```powershell
docker run -it --gpus all `
  -v "${PWD}:/workspace" `
  -v paddleocr_cache:/root/.paddleocr `
  --network host `
  --name document_classifier_v3 `
  document_classifier_v3 `
  bash
```

---

## 🔁 Reingresar al contenedor existente

```powershell
docker exec -it document_classifier_v3 bash
```

---

## ▶️ Ejecutar el clasificador

```bash
python main.py
```

Por defecto:

* Analiza los PDFs de `Muestras de Expedientes/`
* Ejecuta OCR o clasificación textual según `MODE` en `config.py`
* Guarda los resultados en `output/reporte_procesamiento.csv`

---

## ⚙️ Configuración (`config.py`)

```python
from pathlib import Path

PDF_FOLDER = Path("Muestras de Expedientes")
MODE = "auto"  # "text", "image", "auto"

USE_LOCAL_MODEL = True
MODEL_TEXT = "openai/gpt-oss-20b"
MODEL_IMAGE = "paddleocr-vl"
BASE_URL = "http://localhost:8001/v1"
OPENAI_API_KEY = "sk-your-key-if-needed"
```

---

## 🧠 Flujo de ejecución

1. `main.py` recorre los documentos PDF.
2. `content_detector.py` determina si son texto, imagen o híbrido.
3. Si el documento es imagen → usa **PaddleOCR-VL** → texto → LLM.
4. Si tiene texto → usa el **LLM textual** directamente.
5. El resultado estructurado se guarda en `output/reporte_procesamiento.csv`.

---

## 🧾 Ejemplo de salida

```
📄 Resolucion_con_coordenadas.pdf
🧩 Tipo: IMAGE
✅ OCR completado (62.3s)
✅ Clasificación: Resolución
🧠 Explicación: El documento contiene la palabra "RESOLUCIÓN" y estructura legal numerada.
⏱️ Tiempo total: 75.9s
```

---