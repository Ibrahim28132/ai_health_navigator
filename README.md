# 🩺 AI Health Navigator

An intelligent health navigation system that provides medical advice, hospital locations, weather information, and health advisories using AI and external APIs.

## 🌟 Features

- **AI-Powered Medical Triage**: Get intelligent medical advice for symptoms
- **Hospital Locator**: Find nearby hospitals with ratings and addresses
- **Weather Integration**: Get current weather data and health impact analysis
- **Health Advisories**: Access public health information for specific locations
- **Multi-Modal AI**: Uses LangGraph for intelligent workflow orchestration
- **Docker Support**: Fully containerized for easy deployment

## 🏗️ Architecture

The system uses a **LangGraph-based workflow** with the following components:

1. **Extract Node**: Analyzes user queries to extract symptoms and location
2. **Planner Node**: Determines which services to call based on the query
3. **Execute Node**: Calls external APIs (Google Maps, OpenWeather, Tavily)
4. **Critic Node**: Compiles and formats the final response

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- API Keys for external services

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-health-navigator.git
cd ai-health-navigator

# Create .env file with your API keys
cp .env.example .env
# Edit .env with your actual API keys

# Build and run with Docker
docker-compose up --build

# Access the application
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
```

### Option 2: Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-health-navigator.git
cd ai-health-navigator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
# Edit .env with your actual API keys

# Run backend
cd backend
uvicorn main:app --reload

# Run frontend (in new terminal)
cd frontend
streamlit run app.py --server.port 8501
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI API Key (for GPT-4)
OPENAI_API_KEY=your_openai_api_key_here

# Google Maps API Key (for hospital locations)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Tavily API Key (for health advisories)
TAVILY_API_KEY=your_tavily_api_key_here

# OpenWeather API Key (for weather information)
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

## 📋 API Endpoints

### Backend API (FastAPI)

- `GET /` - Health check endpoint
- `POST /navigate` - Main health navigation endpoint

#### Example Request

```bash
curl -X POST "http://localhost:8000/navigate" \
     -H "Content-Type: application/json" \
     -d '{"query": "I have fever and headache in Kisumu"}'
```

#### Example Response

```json
{
  "response": "**Medical Advice for Fever and Headache in Kisumu**\n\n**Symptoms**: fever and headache\n**Location**: Kisumu, Kenya\n\n**Medical Triage**: [AI-generated medical advice]\n\n**Nearby Hospitals**:\n- Hospital A (Rating: 4.5)\n- Hospital B (Rating: 4.2)\n\n**Weather**: 24°C, light rain\n**Health Advisories**: [Location-specific health information]\n\n**Disclaimer**: This is not medical advice. Consult a healthcare professional."
}
```

## 🐳 Docker Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d
```

## 🏥 Supported Services

- **Medical Triage**: OpenAI GPT-4 powered symptom analysis
- **Hospital Search**: Google Maps Places API integration
- **Weather Data**: OpenWeather API for location-specific weather
- **Health Advisories**: Tavily search for public health information

## 🛠️ Technology Stack

- **Backend**: FastAPI, LangGraph, LangChain
- **Frontend**: Streamlit
- **AI**: OpenAI GPT-4, LangGraph workflow orchestration
- **APIs**: Google Maps, OpenWeather, Tavily
- **Containerization**: Docker, Docker Compose
- **Language**: Python 3.11+

## 📁 Project Structure

```
ai-health-navigator/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── agent.py         # LangGraph agent implementation
│   └── __init__.py
├── frontend/
│   └── app.py           # Streamlit frontend
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Multi-service orchestration
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Development

### Adding New Features

1. **New API Integration**: Add new functions in `agent.py`
2. **New Workflow Steps**: Extend the LangGraph workflow
3. **Frontend Updates**: Modify `frontend/app.py`

### Testing

```bash
# Test the agent directly
cd backend
python -c "from agent import app; print('Agent loaded successfully')"

# Test the API
curl http://localhost:8000/
```

## 📚 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This application is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.**

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/yourusername/ai-health-navigator/issues) page
2. Ensure all API keys are properly configured
3. Check Docker logs: `docker-compose logs -f`
4. Verify the backend is healthy: `curl http://localhost:8000/`

## 🌟 Acknowledgments

- OpenAI for GPT-4 API
- Google Maps for location services
- OpenWeather for weather data
- Tavily for search capabilities
- LangChain and LangGraph communities

---

**Made with ❤️ for better health navigation**
