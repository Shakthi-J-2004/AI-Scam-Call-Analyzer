FROM python:3.11-slim

# Install ffmpeg which is required by OpenAI Whisper
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the dependency list first (Docker caches this layer)
COPY requirements.txt .

# We pre-install an older setuptools so Whisper's isolated build succeeds
# We use --no-build-isolation to rely on the installed packages instead of isolated pip environs
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "setuptools<70.0.0" wheel && \
    pip install --no-cache-dir --no-build-isolation -r requirements.txt

# Copy the rest of the code into the container
COPY . .

# Streamlit runs on 8501 by default
EXPOSE 8501

# Healthcheck for Cloud Run
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Start Streamlit bound to 0.0.0.0 
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
