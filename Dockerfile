FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .

# Instala as dependências (incluindo fastapi e uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

EXPOSE 8000

# Use python -m uvicorn em vez de chamar apenas 'uvicorn'
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
