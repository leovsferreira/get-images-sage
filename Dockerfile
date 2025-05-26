FROM python:3.11

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN echo "Build timestamp: $(date)" && \
    pip3 install --no-cache-dir -r requirements.txt

ENV YOLO_CONFIG_DIR=/tmp

COPY . .

CMD ["python3", "main.py"]