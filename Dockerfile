# Imagen base oficial de Python
FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Puerto expuesto
EXPOSE 5000

# Comando para iniciar la app
CMD ["python", "app.py"]

