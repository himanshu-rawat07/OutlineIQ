# ---- Base Image ----
FROM --platform=linux/amd64 python:3.10-slim AS base

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# ---- System Dependencies ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    poppler-utils \
 && rm -rf /var/lib/apt/lists/*

# ---- Python Dependencies ----
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ---- Copy Project Files ----
COPY . .

# ---- Default (Batch Mode) ----
# Runs main.py and processes PDFs in input/ → output/
CMD ["python", "main.py"]

# ---- UI Mode (Optional) ----
# To run Streamlit UI, override CMD when starting the container:
# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

EXPOSE 8501
