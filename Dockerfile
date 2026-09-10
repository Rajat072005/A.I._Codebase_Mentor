FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (git is required for GitPython)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu torch==2.2.1+cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create the storage directories
RUN mkdir -p data metadata_cache

# Hugging Face Spaces requires the app to run on port 7860
EXPOSE 7860

# Start the Flask app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "--timeout", "120", "api:app"]

