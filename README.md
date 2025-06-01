# Sambhar - Data Profiling and Analysis Tool

A full-stack application for data profiling and analysis with FastAPI backend and React/TypeScript frontend.

## Features

- File Upload: Support for CSV, Excel, Parquet, and JSON files
- Auto Profiling: Automatic data type detection and statistical analysis
- Smart Visualizations: Auto-generated charts and plots
- Descriptive Summaries: Natural language insights about your data
- Interactive Analysis: Filter, zoom, and explore your data

## Project Structure

```
sambhar/
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   └── tests/       # Backend tests
└── frontend/        # React frontend
    ├── src/         # Source code
    └── public/      # Static assets
```

## Backend Deployment (Railway)

1. Create a Railway account at https://railway.app
2. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```
3. Login to Railway:
   ```bash
   railway login
   ```
4. Create a new project:
   ```bash
   railway init
   ```
5. Deploy:
   ```bash
   railway up
   ```

## Frontend Deployment (Vercel)

1. Create a Vercel account at https://vercel.com
2. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```
3. Login to Vercel:
   ```bash
   vercel login
   ```
4. Deploy:
   ```bash
   vercel
   ```

## Environment Variables

### Backend
- `PORT`: Port number (default: 8000)
- `FRONTEND_URL`: URL of the frontend application
- `ENVIRONMENT`: development/production

### Frontend
- `VITE_API_URL`: URL of the backend API

## Local Development

1. Backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. Frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Development

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## License

MIT 