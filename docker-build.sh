#!/bin/bash

echo "🐳 Building and running AI Health Navigator with Docker..."

# Build the images
echo "📦 Building Docker images..."
docker-compose build

# Start the services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service status:"
docker-compose ps

echo ""
echo "✅ AI Health Navigator is running!"
echo "🌐 Backend API: http://localhost:8000"
echo "🌐 Frontend App: http://localhost:8501"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"
