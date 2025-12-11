# Imagem base leve com Python 3.11
FROM python:3.11-slim

# Evita criação de bytecode e melhora logs
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
  git \
  && rm -rf /var/lib/apt/lists/*

# Copia somente requirements primeiro para aproveitar cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto (goal/, classes/, main.py, etc.)
COPY . .

# Comando padrão pode ser sobrescrito em tempo de execução
CMD ["python", "main.py"]

