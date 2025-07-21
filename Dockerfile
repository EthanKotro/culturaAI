FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential curl && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app
COPY ./models ./models
COPY app.py .

# Expose internal port
EXPOSE 8001

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
