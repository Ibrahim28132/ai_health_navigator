@echo off
echo 🐳 Building and running AI Health Navigator with Docker...

REM Build the images
echo 📦 Building Docker images...
docker-compose build

REM Start the services
echo 🚀 Starting services...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check service status
echo 📊 Service status:
docker-compose ps

echo.
echo ✅ AI Health Navigator is running!
echo 🌐 Backend API: http://localhost:8000
echo 🌐 Frontend App: http://localhost:8501
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo To stop services: docker-compose down
echo To view logs: docker-compose logs -f
pause
