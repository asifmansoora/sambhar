from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import json
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go
import logging
import os
from app.utils.data_profiler import DataProfiler
from app.utils.file_handler import FileHandler
from app.schemas.responses import ProfileResponse, VisualizationResponse

# Get environment variables with defaults
PORT = int(os.getenv("PORT", 8000))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://sambhar-frontend.vercel.app")  # Default to production URL

# Configure logging to show more details
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log environment details
logger.info(f"Starting server with PORT={PORT}, ENVIRONMENT={ENVIRONMENT}")
logger.info(f"FRONTEND_URL={FRONTEND_URL}")

app = FastAPI(
    title="Sambhar API",
    description="Data Profiling and Analysis API",
    version="1.0.0"
)

# Configure CORS
origins = [
    FRONTEND_URL,  # Production frontend URL
    "http://localhost:5173",  # Development frontend URL
    "https://sambhar-88lre93rr-asif-mansoors-projects.vercel.app",
    "https://sambhar-frontend.vercel.app",
    "https://sambhar-frontend-git-main.vercel.app",
    "https://sambhar-frontend-*.vercel.app",
    "https://*.vercel.app"
]

# Remove any empty strings and duplicates from origins
origins = list(set([origin for origin in origins if origin]))
logger.info(f"Configured CORS origins: {origins}")

# Add CORS middleware with more detailed logging
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Request headers: {request.headers}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all origins for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to Sambhar API"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Received file: {file.filename}")
        file_handler = FileHandler()
        df = await file_handler.process_file(file)
        
        # Generate profile
        profiler = DataProfiler(df)
        profile = profiler.generate_profile()
        
        return JSONResponse(content=profiler._convert_to_serializable(profile))
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/profile")
async def profile_data(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing file for profiling: {file.filename}")
        file_handler = FileHandler()
        df = await file_handler.process_file(file)
        
        logger.info("Generating profile...")
        profiler = DataProfiler(df)
        profile = profiler.generate_profile()
        
        logger.info("Generating visualizations...")
        visualizations = profiler.generate_visualizations()
        
        logger.info("Generating summary...")
        summary = profiler.generate_summary()
        
        response = profiler._convert_to_serializable({
            "profile": profile,
            "visualizations": visualizations,
            "summary": summary
        })
        
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Error in profile_data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/visualize/{viz_type}")
async def generate_visualization(
    viz_type: str,
    file: UploadFile = File(...),
    columns: List[str] = None
):
    try:
        logger.info(f"Generating visualization of type {viz_type}")
        file_handler = FileHandler()
        df = await file_handler.process_file(file)
        
        profiler = DataProfiler(df)
        viz = profiler.generate_specific_visualization(viz_type, columns)
        
        return JSONResponse(content=profiler._convert_to_serializable({
            "plot_data": viz,
            "viz_type": viz_type
        }))
    except Exception as e:
        logger.error(f"Error generating visualization: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting uvicorn server on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT) 