# Sambhar Backend

FastAPI backend for the Sambhar data profiling application.

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Unix/macOS
.\venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- `/docs` for Swagger documentation
- `/redoc` for ReDoc documentation 