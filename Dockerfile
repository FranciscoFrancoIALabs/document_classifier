FROM ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddleocr-vl:latest

USER root

WORKDIR /workspace

COPY . /workspace

RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["python", "main.py"]