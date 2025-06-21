FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential supervisor

# Install Python packages
COPY requirements.txt pytorch-cpu.txt ./
RUN pip install --no-cache-dir -r  pytorch-cpu.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Expose both FastAPI and Streamlit ports
EXPOSE 8000 8501

# Start both services using Supervisor
CMD ["tail", "-f", "/dev/null"]
