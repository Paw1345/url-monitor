FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app.py urls.json ./

RUN useradd --create-home appuser
USER appuser

CMD ["python", "app.py", "urls.json"]
