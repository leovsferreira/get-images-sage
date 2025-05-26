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

RUN pip3 install --no-cache-dir \
    opencv-python-headless==4.8.1.78 \
    ultralytics \
    pywaggle

RUN mkdir -p /root/.cache/ultralytics
ENV YOLO_CONFIG_DIR=/root/.cache/ultralytics

RUN python3 -c "import os; os.environ['YOLO_CONFIG_DIR'] = '/root/.cache/ultralytics'; from ultralytics import YOLO; print('Downloading YOLO model...'); model = YOLO('yolov8n.pt'); print('YOLO model downloaded successfully!')"

RUN ls -la /root/.cache/ultralytics/ || echo "Cache directory not found"
RUN find /root -name "*.pt" -type f || echo "No .pt files found"

COPY . .

CMD ["python3", "main.py"]