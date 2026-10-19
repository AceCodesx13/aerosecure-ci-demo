FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /app/
ENV SM_CHANNEL_TRAIN=/opt/ml/input/data/train \
    SM_CHANNEL_VALIDATION=/opt/ml/input/data/validation \
    SM_MODEL_DIR=/opt/ml/model \
    SM_OUTPUT_DATA_DIR=/opt/ml/output/data
ENTRYPOINT ["python", "/app/train.py"]
