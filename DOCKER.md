# Podium Docker Setup

This directory contains Docker configuration files for running the Podium application.

## Files

- **Dockerfile**: Multi-stage build that creates a single container running both frontend and backend
- **docker-compose.yml**: Orchestration file for easy container management
- **.dockerignore**: Excludes unnecessary files from Docker build context

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. Make sure your `.env` file is configured with your AWS and MongoDB credentials
2. Build and run the container:
   ```bash
   docker-compose up --build
   ```
3. Access the application:
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Using Docker directly

1. Build the image:
   ```bash
   docker build -t podium-app .
   ```

2. Run the container:
   ```bash
   docker run -d \
     --name podium-app \
     -p 4200:4200 \
     -p 8000:8000 \
     --env-file .env \
     podium-app
   ```

## Architecture

The Dockerfile uses a multi-stage build:

1. **Stage 1 (frontend-builder)**: Builds the Angular frontend using Node.js
2. **Stage 2 (final)**: Creates the final image with Python, copies the built frontend, and sets up both services

Both services run in the same container:
- **Backend**: FastAPI/Uvicorn on port 8000
- **Frontend**: Static files served via Python HTTP server on port 4200

## Environment Variables

Required environment variables (set in `.env`):
- `MONGODB_URL`: MongoDB connection string (default: `mongodb://host.docker.internal:27017`)
- `DB_NAME`: Database name (default: `podium_db`)
- `AWS_ACCESS_KEY_ID`: AWS access key for S3
- `AWS_SECRET_ACCESS_KEY`: AWS secret key for S3
- `AWS_REGION`: AWS region (default: `us-east-1`)
- `S3_BUCKET_NAME`: S3 bucket name for media storage (default: `podium-media`)

## Running MongoDB Locally

If you're running MongoDB on your host machine, the container can access it via `host.docker.internal:27017`.

Alternatively, uncomment the MongoDB service in `docker-compose.yml` to run MongoDB in a separate container.

## Stopping the Application

Using Docker Compose:
```bash
docker-compose down
```

Using Docker directly:
```bash
docker stop podium-app
docker rm podium-app
```

## Logs

View logs in real-time:
```bash
docker-compose logs -f
```

Or for direct Docker:
```bash
docker logs -f podium-app
```

## Development Notes

- The Dockerfile builds the Angular frontend in production mode for optimal performance
- Both services start automatically when the container starts
- The container exposes both ports 4200 (frontend) and 8000 (backend)
- The startup script ensures both services run concurrently

## Troubleshooting

1. **MongoDB connection issues**: Ensure MongoDB is running and accessible at the URL specified in `.env`
2. **Port conflicts**: Make sure ports 4200 and 8000 are not already in use on your host machine
3. **Build failures**: Check that all dependencies are correctly specified in `requirements.txt` and `package.json`
