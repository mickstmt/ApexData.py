from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import seasons, drivers, constructors, races

# Import all models to ensure they are registered with SQLAlchemy
from app.db import base  # noqa: F401

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="F1 Data API powered by FastF1",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(seasons.router, prefix=f"{settings.API_V1_PREFIX}/seasons", tags=["seasons"])
app.include_router(drivers.router, prefix=f"{settings.API_V1_PREFIX}/drivers", tags=["drivers"])
app.include_router(constructors.router, prefix=f"{settings.API_V1_PREFIX}/constructors", tags=["constructors"])
app.include_router(races.router, prefix=f"{settings.API_V1_PREFIX}/races", tags=["races"])


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "ApexData API - FastF1 Powered",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
