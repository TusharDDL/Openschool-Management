# School Management System Backend

This is the backend service for the School Management System built with FastAPI.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configuration

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Project Structure
```
backend/
├── app/
│   ├── api/         # API routes
│   ├── core/        # Core utilities and middleware
│   ├── models/      # SQLAlchemy models
│   ├── services/    # Business logic
│   └── main.py      # FastAPI application entry point
├── tests/           # Test cases
├── requirements.txt # Python dependencies
└── Dockerfile      # Docker configuration
```

### Running Tests
```bash
pytest
```

### Docker Build
```bash
docker build -t school-management-backend .
docker run -p 8000:8000 school-management-backend
```