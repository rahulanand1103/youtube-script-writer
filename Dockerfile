# Use official Python base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the necessary port for Streamlit UI
EXPOSE 8501

# Default command (to be overridden in docker-compose)
CMD ["python", "cli.py"]
