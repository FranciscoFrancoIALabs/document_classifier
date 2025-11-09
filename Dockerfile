FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddleocr-vl:latest

USER root
WORKDIR /workspace

COPY . /workspace

RUN apt-get update && apt-get install -y \
    poppler-utils \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# 🔧 Zona horaria del contenedor
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["python", "main.py"]