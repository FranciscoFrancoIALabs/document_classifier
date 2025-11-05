# Imagen base oficial de PaddleOCR-VL (incluye PaddleOCR + CUDA)
FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddleocr-vl:latest

# Usa root para instalar paquetes del sistema
USER root

# Define el directorio de trabajo
WORKDIR /workspace

# Copia el proyecto completo al contenedor
COPY . /workspace

# ===============================
# 🧩 Instalación de dependencias
# ===============================
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 🔧 Actualiza pip e instala dependencias del proyecto
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# ===============================
# 🔐 Variables de entorno opcionales
# ===============================
# Puedes pasar la API key al construir la imagen o al crear el contenedor.
# Ejemplo (build): docker build --build-arg OPENAI_API_KEY=%OPENAI_API_KEY% -t document_classifier_v2 .
# Ejemplo (run):   docker run -e OPENAI_API_KEY=%OPENAI_API_KEY% ...
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# ===============================
# 🔧 Comando por defecto
# ===============================
CMD ["python", "main.py"]
