FROM python:3.10-slim

# Copar código
WORKDIR /app
COPY . /app

# Instalar dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Exponer puerto
EXPOSE 8000

# Ejecutar comandos
CMD ["gunicorn", "revenew.wsgi:application", "--bind", "0.0.0.0:8000"]