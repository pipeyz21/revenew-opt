FROM python:3.10-slim
WORKDIR /app

# Copiar solo requirements.txt primero para aprovechar el cache
COPY requirements.txt .

# Instalar dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear carpeta de logs dentro de /app
RUN mkdir -p logs

EXPOSE 8000
CMD ["gunicorn", "revenew.wsgi:application", "--bind", "0.0.0.0:8000"]
