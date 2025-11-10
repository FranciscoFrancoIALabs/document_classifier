
---

# 🧠 Document Classifier v3 — Clasificación Multimodal de Documentos PDF

Este proyecto permite **clasificar automáticamente documentos PDF** según su tipo (Resolución, Plano, Escritura, etc.) utilizando **modelos de lenguaje y visión**.
Admite tanto **procesamiento textual** como **procesamiento visual (OCR)**, con soporte para **modelos locales (vLLM, PaddleOCR-VL)** o **OpenAI API**.

---

## 🚀 Características principales

* 🔍 **Detección automática** del tipo de contenido (texto, imagen o híbrido).
* 🧾 **Clasificación textual** mediante LLM local (GPT-OSS-20B) o remoto.
* 🖼️ **Clasificación visual / OCR** con **PaddleOCR-VL** (visión + lenguaje).
* 📊 **Reporter CSV** con métricas y marcas de tiempo locales.
* ⚙️ **Arquitectura modular**: detectores, clasificadores, OCR, prompts y utilidades independientes.
* 🔄 **Soporte local o cloud**: OpenAI API o modelos locales.
* 🧩 **Modo de ejecución configurable**: `"text"`, `"image"` o `"auto"` (en desarrollo).

---

## 📁 Estructura del proyecto

```
document_classifier_v3/
│
├── Dockerfile                    # Imagen base con PaddleOCR-VL y timezone -05
├── main.py                       # Orquestador principal
├── config.py                     # Configuración general
├── models.py                     # Esquemas de salida estructurada (Pydantic)
├── requirements.txt              # Dependencias Python
│
├── detectors/
│   └── content_detector.py        # Detección del tipo de contenido
│
├── classifiers/
│   ├── text_classifier.py         # Clasificador textual con LLM
│   ├── image_classifier.py        # Clasificador visual / OCR
│   └── __init__.py
│
├── ocr/
│   └── paddle_vl_wrapper.py       # Wrapper para PaddleOCR-VL
│
├── prompts/
│   └── base_prompts.py            # Prompts centralizados para clasificación
│
├── utils/
│   ├── pdf_utils.py               # Conversión PDF → imagen
│   ├── encoding.py                # Codificación Base64
│   ├── reporting.py               # Generación de reportes CSV
│   └── __init__.py
│
├── Muestras de Expedientes/       # Carpeta con PDFs de ejemplo
│
└── output/                        # Carpeta para resultados OCR y reportes
```

---

## 🧭 Ver estructura del proyecto (Windows PowerShell)

Ejecuta este comando desde la raíz del proyecto:

```powershell
gci -r -fo . | ? { $_.FullName -notmatch '\\\.venv(\\|$)|\\\.idea(\\|$)|\\\.git(\\|$)|\\\.gitignore$|\\__pycache__(\\|$)' } | sort FullName | % {
    $r=$_.FullName.Substring((pwd).Path.Length).TrimStart('\')
    $p=if($r -eq ''){@()}else{$r -split '\\'}
    $d=$p.Count-1
    $i='|'+'   '*$d
    if ($_.PSIsContainer) {
        "$i+---$($_.Name)"
    } else {
        "$i   $($_.Name)"
    }
}
```

---

## 🐳 Construir la imagen Docker

```powershell
docker build -t document_classifier_v3 .
```

> La imagen ya configura automáticamente la zona horaria `America/Bogota` (UTC−05).

---

## 🚀 Ejecutar el contenedor (GPU activada y carpeta externa montada)

```powershell
docker run -it --gpus all `
  -v "${PWD}:/workspace" `
  -v "C:\Users\Administrator\Documents\FF\ANT\Expedientes\Expedientes Muestra:/data/expedientes" `
  -v paddleocr_cache:/root/.paddleocr `
  --network host `
  --name document_classifier_v3 `
  document_classifier_v3 `
  bash
```

> Esto monta tu carpeta real de expedientes (`C:\Users\Administrator\Documents\FF\ANT\Expedientes\Expedientes Muestra`) dentro del contenedor en `/data/expedientes`.

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

* Analiza los PDFs de `Muestras de Expedientes/` o de la ruta configurada.
* Ejecuta OCR o clasificación textual según `MODE` en `config.py`.
* Guarda los resultados en `output/reporte_procesamiento.csv`.
* Incluye timestamp local (-05) en cada registro.

---

## ⚙️ Configuración (`config.py`)

```python
from pathlib import Path

# Carpeta montada desde el host
PDF_FOLDER = Path("/data/expedientes")

MODE = "image"  # "text", "image" o "auto"

USE_LOCAL_MODEL = True
MODEL_TEXT = "openai/gpt-oss-20b"
MODEL_IMAGE = "paddleocr-vl"
BASE_URL = "http://localhost:8001/v1"
```

> **Nota:** El modo `"auto"` será implementado próximamente.

---

## 🧠 Flujo de ejecución

1. `main.py` recorre los documentos PDF (en una carpeta o subcarpetas futuras).
2. `content_detector.py` determina si son texto, imagen o híbrido.
3. Si `MODE = "image"` → usa **PaddleOCR-VL** → extrae texto → clasifica con LLM.
4. Si `MODE = "text"` → extrae texto embebido → clasifica con LLM.
5. Se genera un CSV con métricas, tiempos y categoría detectada.

---

## 🧾 Ejemplo de salida

```
📄 Resolucion_con_coordenadas.pdf
🧩 Tipo: IMAGE
✅ OCR completado (62.3s) → 15,234 caracteres
✅ Clasificación: Resolucion
🧠 Explicación: El documento contiene la palabra “RESOLUCIÓN” y estructura legal numerada.
🕒 Timestamp: 2025-11-09 18:07:15 (-05)
```

---

## 🧩 Próximos pasos

1. Implementar modo `"auto"` que seleccione automáticamente el flujo óptimo.
2. Añadir soporte para carpetas anidadas (procesamiento por subdirectorios).
3. Mejorar métricas OCR (CER/WER).
4. Exportar resultados en formatos adicionales (JSON, Excel).

---