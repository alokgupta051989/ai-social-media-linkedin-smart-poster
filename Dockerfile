FROM python:3.11-slim

WORKDIR /app

# Copy backend files
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Install dependencies
RUN pip install -r backend/requirements.txt

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]