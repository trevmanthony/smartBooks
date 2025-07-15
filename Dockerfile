FROM python:3.11-slim
WORKDIR /app

# Install libraries required for headless Chrome used in Selenium tests
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libasound2 libxss1 libxtst6 libdrm2 \
    libxcb-dri3-0 libxshmfence1 fonts-liberation curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
