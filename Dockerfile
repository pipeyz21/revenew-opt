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
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]