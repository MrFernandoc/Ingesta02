# Usa una imagen oficial de Python como base
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de tu script Python al contenedor
COPY . /app

# Actualiza pip y instala las dependencias necesarias
RUN pip install --upgrade pip \
    && pip install mysql-connector-python boto3 colorama

# Comando para ejecutar tu script
CMD ["python", "ingesta.py"]
