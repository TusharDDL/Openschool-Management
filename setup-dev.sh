#!/bin/bash

# Exit on error
set -e

echo "Setting up development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

# Start development services
echo "Starting development services..."
docker-compose -f docker-compose.local.yml up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Run database migrations
echo "Running database migrations..."
docker-compose -f docker-compose.local.yml exec backend alembic upgrade head

echo "Development environment setup complete!"
echo "You can now run:"
echo "  npm run dev        # Start frontend development server"
echo "  npm run dev:logs   # View service logs"
echo "  npm run dev:stop   # Stop development services"