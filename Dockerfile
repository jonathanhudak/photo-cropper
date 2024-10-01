FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Download YOLO weights and config
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg

# Expose port for VNC (if needed)
EXPOSE 5900

# Run the application
CMD ["python", "main.py"]