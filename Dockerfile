FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear un usuario no privilegiado para ejecutar la aplicación
RUN useradd -m appuser
USER appuser

# Exponer puerto
EXPOSE 5000

# Ejecutar la aplicación
CMD ["python", "app.py"] 