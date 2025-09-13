# Docker Setup for Bugsy

This project includes a complete Docker setup for easy deployment and development.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

## Quick Start

1. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your actual API keys
   ```

2. **Build and run the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Open your browser and go to `http://localhost:5000`

## Docker Files Overview

### Dockerfile
- Uses Python 3.12 slim image for optimal size
- Installs all required dependencies (Flask, OpenAI, python-dotenv, etc.)
- Sets up proper environment variables
- Includes health checks
- Exposes port 5000

### docker-compose.yml
- Defines the Flask application service
- Maps port 5000 to host
- Mounts volumes for persistent data
- Includes health checks and restart policies
- Sets up isolated network

### .dockerignore
- Excludes unnecessary files from build context
- Reduces build time and image size
- Excludes development files, logs, and OS-specific files

## Available Commands

```bash
# Build and start services
docker-compose up --build

# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild only
docker-compose build

# Remove everything (containers, networks, volumes)
docker-compose down -v --remove-orphans
```

## Environment Variables

Required environment variables in `.env`:
- `OPENAI_API_KEY`: Your OpenAI API key
- `TESTSPRITE_API_KEY`: Your TestSprite API key

## Volume Mounts

- `./get_test_stripe_plan:/app/get_test_stripe_plan` - Persistent data storage
- `./templates:/app/templates` - Template files

## Health Checks

The container includes health checks that verify the Flask app is responding on port 5000.

## Troubleshooting

1. **Port already in use:**
   ```bash
   # Change the port mapping in docker-compose.yml
   ports:
     - "8000:5000"  # Use port 8000 instead
   ```

2. **Permission issues:**
   ```bash
   # Ensure Docker has proper permissions
   sudo docker-compose up --build
   ```

3. **Build failures:**
   ```bash
   # Clean build
   docker-compose down -v
   docker system prune -f
   docker-compose up --build
   ```