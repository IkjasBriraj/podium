# Multi-stage Dockerfile for Podium App (Frontend + Backend)

# Stage 1: Build Angular Frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source code
COPY frontend/ ./

# Build the Angular application for production
RUN npm run build

# Stage 2: Final image with both frontend and backend
FROM python:3.11-slim

# Install Node.js for serving frontend
RUN apt-get update && apt-get install -y \
    curl \
    supervisor \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from the builder stage
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Copy frontend package.json for serving (if needed)
COPY frontend/package*.json ./frontend/

# Create supervisord configuration
RUN mkdir -p /var/log/supervisor

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting Podium Application..."\n\
\n\
# Start backend\n\
echo "Starting FastAPI backend on port 8000..."\n\
cd /app && python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &\n\
BACKEND_PID=$!\n\
\n\
# Start frontend\n\
echo "Starting Angular frontend on port 4200..."\n\
cd /app/frontend/dist/frontend/browser && python -m http.server 4200 &\n\
FRONTEND_PID=$!\n\
\n\
# Wait for any process to exit\n\
wait -n\n\
\n\
# Exit with status of process that exited first\n\
exit $?\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose ports
EXPOSE 4200 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start both services
CMD ["/app/start.sh"]
