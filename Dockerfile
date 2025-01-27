FROM python:latest

WORKDIR /usr/src/warehouse_data_analyzer

COPY requirements.txt .

ENV TZ="Europe/Kiev" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN python3 -m venv .venv
RUN bash -c "source .venv/bin/activate && \
    python3 -m pip install --no-cache-dir -U pip setuptools -r requirements.txt"

COPY . .

CMD [ "bash", "-c", "sleep 10 && source .venv/bin/activate && \
    uvicorn app:create_app --reload --host=0.0.0.0 --port=8000" ]
