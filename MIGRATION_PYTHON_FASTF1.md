# Migración a Python Backend con FastF1

## Resumen Ejecutivo

Este documento describe la arquitectura y pasos necesarios para replicar ApexData utilizando un backend Python que aproveche las capacidades completas del paquete FastF1, manteniendo una experiencia de usuario moderna con Next.js en el frontend.

---

## Stack Tecnológico Propuesto

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Lenguaje**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: React Server Components + TanStack Query
- **Charts**: Recharts o Plotly.js (para telemetría)
- **Fuente**: Orbitron (mantener identidad visual)

### Backend
- **Framework**: FastAPI
- **Lenguaje**: Python 3.11+
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Data Processing**: Pandas (viene con FastF1)
- **Caching**: Redis
- **Task Queue**: Celery (para procesamiento async)
- **Validation**: Pydantic V2

### Datos y APIs
- **Telemetría**: FastF1
- **Datos Históricos**: Jolpica F1 API (backup)
- **Real-time**: FastF1 Live Timing

### Base de Datos
- **Primary DB**: PostgreSQL 15+
- **Cache Layer**: Redis
- **Time-series (opcional)**: TimescaleDB (extensión de PostgreSQL para telemetría)

### Infraestructura
- **Containerización**: Docker + Docker Compose
- **API Documentation**: FastAPI Auto-generated (Swagger/ReDoc)
- **Testing**: pytest (backend), Vitest (frontend)

---

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                       FRONTEND (Next.js)                    │
│  ┌────────────┬────────────┬────────────┬────────────┐     │
│  │  Seasons   │  Drivers   │  Results   │ Telemetry  │     │
│  │   Page     │   Page     │   Page     │   Page     │     │
│  └────────────┴────────────┴────────────┴────────────┘     │
│         │              │              │              │      │
│         └──────────────┴──────────────┴──────────────┘      │
│                        │                                     │
│                  TanStack Query                              │
│                        │                                     │
└────────────────────────┼─────────────────────────────────────┘
                         │
                    HTTP/REST
                         │
┌────────────────────────┼─────────────────────────────────────┐
│                  BACKEND (FastAPI)                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              API Layer (FastAPI)                    │    │
│  │  /api/v1/seasons  /api/v1/drivers  /api/v1/races   │    │
│  │  /api/v1/telemetry  /api/v1/live                   │    │
│  └─────────────────────────────────────────────────────┘    │
│         │                        │                           │
│  ┌──────┴────────┐      ┌───────┴──────────┐               │
│  │  FastF1       │      │  Service Layer   │               │
│  │  Integration  │      │  (Business Logic)│               │
│  └───────────────┘      └──────────────────┘               │
│         │                        │                           │
│  ┌──────┴────────────────────────┴──────────┐               │
│  │         SQLAlchemy ORM                   │               │
│  └──────────────────────────────────────────┘               │
└────────────────────────┼─────────────────────────────────────┘
                         │
                    PostgreSQL
                         │
┌────────────────────────┼─────────────────────────────────────┐
│                   DATABASE LAYER                             │
│  ┌─────────┬─────────┬──────────┬──────────┬─────────────┐  │
│  │ Seasons │ Drivers │  Races   │ Results  │ Qualifying  │  │
│  ├─────────┼─────────┼──────────┼──────────┼─────────────┤  │
│  │ Telemetry│ LapData│ Weather  │ Positions│ TireStints  │  │
│  └─────────┴─────────┴──────────┴──────────┴─────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Estructura del Proyecto

```
apexdata-python/
│
├── frontend/                    # Next.js App
│   ├── src/
│   │   ├── app/
│   │   │   ├── (dashboard)/
│   │   │   │   ├── seasons/
│   │   │   │   ├── drivers/
│   │   │   │   ├── constructors/
│   │   │   │   ├── results/
│   │   │   │   └── telemetry/      # NUEVO: Visualizaciones de telemetría
│   │   │   ├── api/                 # API routes (proxy si es necesario)
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   ├── lib/
│   │   │   ├── api-client.ts       # Axios/Fetch wrapper para FastAPI
│   │   │   └── types.ts            # TypeScript types
│   │   └── hooks/
│   ├── package.json
│   ├── tailwind.config.ts
│   └── next.config.js
│
├── backend/                     # FastAPI App
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Settings (Pydantic Settings)
│   │   │
│   │   ├── api/                 # API Endpoints
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── seasons.py
│   │   │   │   ├── drivers.py
│   │   │   │   ├── constructors.py
│   │   │   │   ├── races.py
│   │   │   │   ├── results.py
│   │   │   │   ├── qualifying.py
│   │   │   │   ├── telemetry.py    # NUEVO: Endpoints de telemetría
│   │   │   │   └── live.py         # NUEVO: Live timing
│   │   │   └── deps.py          # Dependencies (DB session, etc)
│   │   │
│   │   ├── models/              # SQLAlchemy Models
│   │   │   ├── __init__.py
│   │   │   ├── season.py
│   │   │   ├── driver.py
│   │   │   ├── constructor.py
│   │   │   ├── race.py
│   │   │   ├── result.py
│   │   │   ├── qualifying.py
│   │   │   ├── telemetry.py     # NUEVO
│   │   │   ├── lap_data.py      # NUEVO
│   │   │   └── tire_stint.py    # NUEVO
│   │   │
│   │   ├── schemas/             # Pydantic Schemas (Request/Response)
│   │   │   ├── __init__.py
│   │   │   ├── season.py
│   │   │   ├── driver.py
│   │   │   ├── race.py
│   │   │   └── telemetry.py     # NUEVO
│   │   │
│   │   ├── services/            # Business Logic
│   │   │   ├── __init__.py
│   │   │   ├── fastf1_service.py   # NUEVO: FastF1 integration
│   │   │   ├── season_service.py
│   │   │   ├── driver_service.py
│   │   │   └── telemetry_service.py # NUEVO
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py      # Database connection
│   │   │   └── base.py          # Base model
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── cache.py         # Redis caching utilities
│   │
│   ├── alembic/                 # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── scripts/                 # Seed scripts
│   │   ├── seed_seasons.py
│   │   ├── seed_drivers.py
│   │   ├── seed_races.py
│   │   ├── seed_results.py
│   │   ├── seed_qualifying.py
│   │   └── seed_telemetry.py    # NUEVO: Import FastF1 data
│   │
│   ├── tests/
│   │   ├── test_api/
│   │   └── test_services/
│   │
│   ├── requirements.txt
│   └── pyproject.toml
│
├── docker-compose.yml           # Orchestration
├── .env.example
└── README.md
```

---

## Paso a Paso: Implementación

### Fase 1: Setup Inicial (Día 1-2)

#### 1.1 Crear estructura del proyecto

```bash
mkdir apexdata-python
cd apexdata-python
mkdir -p backend/app/{api,models,schemas,services,db,utils}
mkdir -p backend/alembic/versions
mkdir -p backend/scripts
mkdir -p frontend
```

#### 1.2 Setup Backend (FastAPI)

**requirements.txt**:
```txt
# FastAPI
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9

# FastF1 and Data Processing
fastf1==3.3.3
pandas==2.1.4
numpy==1.26.3

# Caching and Task Queue
redis==5.0.1
celery==5.3.6

# HTTP Client
httpx==0.26.0
aiohttp==3.9.1

# Utilities
python-dotenv==1.0.0
python-multipart==0.0.6
```

**backend/app/main.py**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import seasons, drivers, constructors, races, results, qualifying, telemetry
from app.db.database import engine
from app.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ApexData API",
    description="F1 Data API powered by FastF1",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(seasons.router, prefix="/api/v1/seasons", tags=["seasons"])
app.include_router(drivers.router, prefix="/api/v1/drivers", tags=["drivers"])
app.include_router(constructors.router, prefix="/api/v1/constructors", tags=["constructors"])
app.include_router(races.router, prefix="/api/v1/races", tags=["races"])
app.include_router(results.router, prefix="/api/v1/results", tags=["results"])
app.include_router(qualifying.router, prefix="/api/v1/qualifying", tags=["qualifying"])
app.include_router(telemetry.router, prefix="/api/v1/telemetry", tags=["telemetry"])

@app.get("/")
def root():
    return {"message": "ApexData API - FastF1 Powered"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

**backend/app/config.py**:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/apexdata"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # FastF1
    FASTF1_CACHE_DIR: str = "./fastf1_cache"

    # API
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()
```

**backend/app/db/database.py**:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 1.3 Setup Frontend (Next.js)

```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --app --src-dir
```

**frontend/src/lib/api-client.ts**:
```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default apiClient;

// Type-safe API functions
export const seasonsApi = {
  getAll: () => apiClient.get('/seasons'),
  getById: (year: number) => apiClient.get(`/seasons/${year}`),
};

export const driversApi = {
  getAll: () => apiClient.get('/drivers'),
  getById: (id: string) => apiClient.get(`/drivers/${id}`),
};

export const telemetryApi = {
  getLapTelemetry: (year: number, round: number, driver: string, lap: number) =>
    apiClient.get(`/telemetry/${year}/${round}/${driver}/${lap}`),
  getSessionTelemetry: (year: number, round: number, session: string) =>
    apiClient.get(`/telemetry/${year}/${round}/${session}`),
};
```

---

### Fase 2: Modelos de Base de Datos (Día 3-4)

#### 2.1 Modelos SQLAlchemy (replicar Prisma schema)

**backend/app/models/season.py**:
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Season(Base):
    __tablename__ = "seasons"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    year = Column(Integer, unique=True, nullable=False, index=True)
    wikipedia_url = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    races = relationship("Race", back_populates="season", cascade="all, delete-orphan")
```

**backend/app/models/driver.py**:
```python
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
import uuid

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    driver_id = Column(String, unique=True, nullable=False, index=True)
    permanent_number = Column(Integer, nullable=True)
    code = Column(String(3), nullable=True)
    given_name = Column(String, nullable=False)
    family_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    nationality = Column(String, nullable=False)
    url = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    results = relationship("Result", back_populates="driver")
    qualifying = relationship("Qualifying", back_populates="driver")
    lap_data = relationship("LapData", back_populates="driver")  # NEW
```

**backend/app/models/telemetry.py** (NUEVO):
```python
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
import uuid

class LapData(Base):
    """Stores lap-by-lap data from FastF1"""
    __tablename__ = "lap_data"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Keys
    race_id = Column(String, ForeignKey("races.id", ondelete="CASCADE"), nullable=False)
    driver_id = Column(String, ForeignKey("drivers.id", ondelete="RESTRICT"), nullable=False)

    # Lap Info
    session_type = Column(String, nullable=False)  # 'R', 'Q', 'FP1', 'FP2', 'FP3'
    lap_number = Column(Integer, nullable=False)

    # Timing
    lap_time = Column(Float, nullable=True)  # in seconds
    sector_1_time = Column(Float, nullable=True)
    sector_2_time = Column(Float, nullable=True)
    sector_3_time = Column(Float, nullable=True)

    # Speed
    speed_i1 = Column(Float, nullable=True)  # Speed trap 1
    speed_i2 = Column(Float, nullable=True)  # Speed trap 2
    speed_fl = Column(Float, nullable=True)  # Speed at finish line
    speed_st = Column(Float, nullable=True)  # Speed trap

    # Tire Info
    compound = Column(String, nullable=True)  # SOFT, MEDIUM, HARD, etc.
    tire_life = Column(Integer, nullable=True)  # laps on this tire

    # Flags
    is_personal_best = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    race = relationship("Race", back_populates="lap_data")
    driver = relationship("Driver", back_populates="lap_data")
    telemetry_points = relationship("TelemetryPoint", back_populates="lap", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_lap_data_race_driver', 'race_id', 'driver_id'),
        Index('idx_lap_data_session', 'race_id', 'session_type'),
    )


class TelemetryPoint(Base):
    """Stores detailed telemetry data points (high frequency)"""
    __tablename__ = "telemetry_points"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Key
    lap_id = Column(String, ForeignKey("lap_data.id", ondelete="CASCADE"), nullable=False)

    # Position
    distance = Column(Float, nullable=False)  # Distance along track (meters)

    # Telemetry
    speed = Column(Float, nullable=True)  # km/h
    throttle = Column(Float, nullable=True)  # 0-100%
    brake = Column(Float, nullable=True)  # 0-100%
    gear = Column(Integer, nullable=True)  # Current gear
    rpm = Column(Float, nullable=True)  # Engine RPM
    drs = Column(Integer, nullable=True)  # DRS status (0=off, 1=on)

    # Relationships
    lap = relationship("LapData", back_populates="telemetry_points")

    # Indexes
    __table_args__ = (
        Index('idx_telemetry_lap', 'lap_id'),
    )
```

#### 2.2 Crear Migraciones

```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

### Fase 3: Integración FastF1 (Día 5-7)

#### 3.1 Servicio FastF1

**backend/app/services/fastf1_service.py**:
```python
import fastf1
import pandas as pd
from pathlib import Path
from app.config import settings
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class FastF1Service:
    def __init__(self):
        # Enable FastF1 cache
        cache_dir = Path(settings.FASTF1_CACHE_DIR)
        cache_dir.mkdir(exist_ok=True)
        fastf1.Cache.enable_cache(str(cache_dir))

    def get_session(self, year: int, round: int, session_type: str):
        """
        Load a F1 session

        Args:
            year: Season year
            round: Race round number
            session_type: 'FP1', 'FP2', 'FP3', 'Q', 'S', 'R'

        Returns:
            FastF1 Session object
        """
        try:
            session = fastf1.get_session(year, round, session_type)
            session.load()
            return session
        except Exception as e:
            logger.error(f"Error loading session {year}/{round}/{session_type}: {e}")
            return None

    def get_lap_telemetry(
        self,
        year: int,
        round: int,
        driver: str,
        lap_number: int,
        session_type: str = 'R'
    ) -> Optional[pd.DataFrame]:
        """
        Get telemetry data for a specific lap

        Returns DataFrame with columns: Distance, Speed, Throttle, Brake, Gear, RPM, DRS
        """
        try:
            session = self.get_session(year, round, session_type)
            if not session:
                return None

            driver_laps = session.laps.pick_driver(driver)
            lap = driver_laps.pick_lap(lap_number)

            if lap is None:
                return None

            telemetry = lap.get_telemetry()
            return telemetry

        except Exception as e:
            logger.error(f"Error getting telemetry: {e}")
            return None

    def get_all_laps(self, year: int, round: int, session_type: str = 'R') -> pd.DataFrame:
        """
        Get all laps from a session

        Returns DataFrame with lap times, sectors, speeds, compounds, etc.
        """
        try:
            session = self.get_session(year, round, session_type)
            if not session:
                return pd.DataFrame()

            return session.laps

        except Exception as e:
            logger.error(f"Error getting laps: {e}")
            return pd.DataFrame()

    def get_fastest_lap(self, year: int, round: int, session_type: str = 'R'):
        """Get the fastest lap of the session"""
        try:
            session = self.get_session(year, round, session_type)
            if not session:
                return None

            fastest_lap = session.laps.pick_fastest()
            return fastest_lap

        except Exception as e:
            logger.error(f"Error getting fastest lap: {e}")
            return None

    def get_driver_laps(self, year: int, round: int, driver: str, session_type: str = 'R'):
        """Get all laps for a specific driver"""
        try:
            session = self.get_session(year, round, session_type)
            if not session:
                return pd.DataFrame()

            driver_laps = session.laps.pick_driver(driver)
            return driver_laps

        except Exception as e:
            logger.error(f"Error getting driver laps: {e}")
            return pd.DataFrame()

    def compare_drivers_fastest_lap(
        self,
        year: int,
        round: int,
        drivers: List[str],
        session_type: str = 'Q'
    ):
        """
        Compare telemetry from fastest laps of multiple drivers

        Returns dict with driver codes as keys and telemetry DataFrames as values
        """
        try:
            session = self.get_session(year, round, session_type)
            if not session:
                return {}

            comparison = {}
            for driver in drivers:
                driver_laps = session.laps.pick_driver(driver)
                fastest_lap = driver_laps.pick_fastest()

                if fastest_lap is not None:
                    telemetry = fastest_lap.get_telemetry()
                    comparison[driver] = telemetry

            return comparison

        except Exception as e:
            logger.error(f"Error comparing drivers: {e}")
            return {}

# Singleton instance
fastf1_service = FastF1Service()
```

#### 3.2 API Endpoints para Telemetría

**backend/app/api/v1/telemetry.py**:
```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db
from app.services.fastf1_service import fastf1_service
from app.schemas.telemetry import LapTelemetryResponse, LapComparisonResponse
import pandas as pd

router = APIRouter()

@router.get("/{year}/{round}/{session}/laps")
def get_session_laps(
    year: int,
    round: int,
    session: str = Query(..., regex="^(FP1|FP2|FP3|Q|S|R)$"),
    driver: Optional[str] = None
):
    """
    Get all laps from a session, optionally filtered by driver
    """
    try:
        if driver:
            laps = fastf1_service.get_driver_laps(year, round, driver, session)
        else:
            laps = fastf1_service.get_all_laps(year, round, session)

        if laps.empty:
            raise HTTPException(status_code=404, detail="No lap data found")

        # Convert to JSON-friendly format
        laps_data = laps[[
            'LapNumber', 'Time', 'Driver', 'LapTime',
            'Sector1Time', 'Sector2Time', 'Sector3Time',
            'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST',
            'Compound', 'TyreLife', 'IsPersonalBest'
        ]].to_dict(orient='records')

        return {
            "year": year,
            "round": round,
            "session": session,
            "laps": laps_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{year}/{round}/{session}/telemetry/{driver}/{lap}")
def get_lap_telemetry(
    year: int,
    round: int,
    session: str,
    driver: str,
    lap: int
):
    """
    Get detailed telemetry for a specific lap
    """
    try:
        telemetry = fastf1_service.get_lap_telemetry(year, round, driver, lap, session)

        if telemetry is None or telemetry.empty:
            raise HTTPException(status_code=404, detail="Telemetry not found")

        # Sample telemetry to reduce size (every 10th point)
        telemetry_sampled = telemetry[::10]

        telemetry_data = telemetry_sampled[[
            'Distance', 'Speed', 'Throttle', 'Brake',
            'Gear', 'RPM', 'DRS'
        ]].to_dict(orient='records')

        return {
            "year": year,
            "round": round,
            "session": session,
            "driver": driver,
            "lap": lap,
            "telemetry": telemetry_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{year}/{round}/{session}/compare")
def compare_drivers(
    year: int,
    round: int,
    session: str,
    drivers: str = Query(..., description="Comma-separated driver codes (e.g., VER,HAM,LEC)")
):
    """
    Compare fastest laps of multiple drivers
    """
    try:
        driver_list = drivers.split(',')

        if len(driver_list) > 5:
            raise HTTPException(
                status_code=400,
                detail="Maximum 5 drivers for comparison"
            )

        comparison = fastf1_service.compare_drivers_fastest_lap(
            year, round, driver_list, session
        )

        if not comparison:
            raise HTTPException(status_code=404, detail="No data found for comparison")

        # Format for frontend
        result = {}
        for driver, telemetry in comparison.items():
            # Sample to reduce payload
            telemetry_sampled = telemetry[::10]

            result[driver] = {
                "telemetry": telemetry_sampled[[
                    'Distance', 'Speed', 'Throttle', 'Brake'
                ]].to_dict(orient='records')
            }

        return {
            "year": year,
            "round": round,
            "session": session,
            "comparison": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### Fase 4: Frontend - Páginas de Telemetría (Día 8-10)

#### 4.1 Página de Telemetría

**frontend/src/app/telemetry/[year]/[round]/page.tsx**:
```typescript
import TelemetryClient from './TelemetryClient';

interface TelemetryPageProps {
  params: Promise<{
    year: string;
    round: string;
  }>;
}

export default async function TelemetryPage({ params }: TelemetryPageProps) {
  const { year, round } = await params;

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">
        Telemetry - {year} Round {round}
      </h1>
      <TelemetryClient year={parseInt(year)} round={parseInt(round)} />
    </div>
  );
}
```

**frontend/src/app/telemetry/[year]/[round]/TelemetryClient.tsx**:
```typescript
'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { telemetryApi } from '@/lib/api-client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

interface TelemetryClientProps {
  year: number;
  round: number;
}

export default function TelemetryClient({ year, round }: TelemetryClientProps) {
  const [session, setSession] = useState('Q');
  const [driver, setDriver] = useState('VER');
  const [lap, setLap] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ['telemetry', year, round, session, driver, lap],
    queryFn: () => telemetryApi.getLapTelemetry(year, round, driver, lap),
  });

  if (isLoading) return <div>Loading telemetry...</div>;

  const telemetryData = data?.data?.telemetry || [];

  return (
    <div className="space-y-8">
      {/* Controls */}
      <div className="flex gap-4">
        <select
          value={session}
          onChange={(e) => setSession(e.target.value)}
          className="px-4 py-2 border rounded"
        >
          <option value="FP1">Free Practice 1</option>
          <option value="FP2">Free Practice 2</option>
          <option value="FP3">Free Practice 3</option>
          <option value="Q">Qualifying</option>
          <option value="R">Race</option>
        </select>

        <input
          type="text"
          placeholder="Driver (e.g., VER)"
          value={driver}
          onChange={(e) => setDriver(e.target.value)}
          className="px-4 py-2 border rounded"
        />

        <input
          type="number"
          placeholder="Lap"
          value={lap}
          onChange={(e) => setLap(parseInt(e.target.value))}
          className="px-4 py-2 border rounded"
        />
      </div>

      {/* Speed Chart */}
      <div className="rounded-lg border bg-card p-6">
        <h2 className="text-2xl font-bold mb-4">Speed</h2>
        <LineChart width={1000} height={400} data={telemetryData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Distance" label={{ value: 'Distance (m)', position: 'insideBottom', offset: -5 }} />
          <YAxis label={{ value: 'Speed (km/h)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Speed" stroke="#8884d8" dot={false} />
        </LineChart>
      </div>

      {/* Throttle & Brake */}
      <div className="rounded-lg border bg-card p-6">
        <h2 className="text-2xl font-bold mb-4">Throttle & Brake</h2>
        <LineChart width={1000} height={400} data={telemetryData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Distance" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Throttle" stroke="#82ca9d" dot={false} />
          <Line type="monotone" dataKey="Brake" stroke="#ff7300" dot={false} />
        </LineChart>
      </div>

      {/* Gear */}
      <div className="rounded-lg border bg-card p-6">
        <h2 className="text-2xl font-bold mb-4">Gear</h2>
        <LineChart width={1000} height={300} data={telemetryData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Distance" />
          <YAxis domain={[0, 8]} />
          <Tooltip />
          <Legend />
          <Line type="stepAfter" dataKey="Gear" stroke="#ffc658" dot={false} />
        </LineChart>
      </div>
    </div>
  );
}
```

---

### Fase 5: Scripts de Seed con FastF1 (Día 11-12)

**backend/scripts/seed_telemetry.py**:
```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.database import SessionLocal
from app.models.lap_data import LapData, TelemetryPoint
from app.services.fastf1_service import fastf1_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_telemetry_for_race(year: int, round: int, session_type: str = 'R'):
    """
    Seed telemetry data for a specific race/session using FastF1
    """
    db = SessionLocal()

    try:
        logger.info(f"Fetching data from FastF1: {year} Round {round} {session_type}")

        # Get all laps
        laps = fastf1_service.get_all_laps(year, round, session_type)

        if laps.empty:
            logger.warning(f"No laps found for {year}/{round}/{session_type}")
            return

        # Get race from DB
        race = db.query(Race).filter(
            Race.year == year,
            Race.round == round
        ).first()

        if not race:
            logger.error(f"Race not found: {year}/{round}")
            return

        lap_count = 0

        # Process each lap
        for idx, lap_row in laps.iterrows():
            try:
                # Get driver
                driver_code = lap_row['Driver']
                driver = db.query(Driver).filter(Driver.code == driver_code).first()

                if not driver:
                    continue

                # Create lap data entry
                lap_data = LapData(
                    race_id=race.id,
                    driver_id=driver.id,
                    session_type=session_type,
                    lap_number=int(lap_row['LapNumber']),
                    lap_time=lap_row['LapTime'].total_seconds() if pd.notna(lap_row['LapTime']) else None,
                    sector_1_time=lap_row['Sector1Time'].total_seconds() if pd.notna(lap_row['Sector1Time']) else None,
                    sector_2_time=lap_row['Sector2Time'].total_seconds() if pd.notna(lap_row['Sector2Time']) else None,
                    sector_3_time=lap_row['Sector3Time'].total_seconds() if pd.notna(lap_row['Sector3Time']) else None,
                    speed_i1=float(lap_row['SpeedI1']) if pd.notna(lap_row['SpeedI1']) else None,
                    speed_i2=float(lap_row['SpeedI2']) if pd.notna(lap_row['SpeedI2']) else None,
                    speed_fl=float(lap_row['SpeedFL']) if pd.notna(lap_row['SpeedFL']) else None,
                    speed_st=float(lap_row['SpeedST']) if pd.notna(lap_row['SpeedST']) else None,
                    compound=str(lap_row['Compound']) if pd.notna(lap_row['Compound']) else None,
                    tire_life=int(lap_row['TyreLife']) if pd.notna(lap_row['TyreLife']) else None,
                    is_personal_best=bool(lap_row['IsPersonalBest']) if pd.notna(lap_row['IsPersonalBest']) else False,
                )

                db.add(lap_data)
                db.flush()  # Get the lap_data.id

                # OPTIONAL: Store detailed telemetry (WARNING: Very large data!)
                # Uncomment if you want full telemetry storage
                # telemetry = fastf1_service.get_lap_telemetry(
                #     year, round, driver_code, int(lap_row['LapNumber']), session_type
                # )
                #
                # if telemetry is not None and not telemetry.empty:
                #     # Sample every 10th point to reduce size
                #     telemetry_sampled = telemetry[::10]
                #
                #     for _, tel_row in telemetry_sampled.iterrows():
                #         tel_point = TelemetryPoint(
                #             lap_id=lap_data.id,
                #             distance=float(tel_row['Distance']),
                #             speed=float(tel_row['Speed']) if pd.notna(tel_row['Speed']) else None,
                #             throttle=float(tel_row['Throttle']) if pd.notna(tel_row['Throttle']) else None,
                #             brake=float(tel_row['Brake']) if pd.notna(tel_row['Brake']) else None,
                #             gear=int(tel_row['nGear']) if pd.notna(tel_row['nGear']) else None,
                #             rpm=float(tel_row['RPM']) if pd.notna(tel_row['RPM']) else None,
                #             drs=int(tel_row['DRS']) if pd.notna(tel_row['DRS']) else None,
                #         )
                #         db.add(tel_point)

                lap_count += 1

                if lap_count % 50 == 0:
                    db.commit()
                    logger.info(f"Processed {lap_count} laps...")

            except Exception as e:
                logger.error(f"Error processing lap: {e}")
                continue

        db.commit()
        logger.info(f"✅ Successfully seeded {lap_count} laps for {year}/{round}/{session_type}")

    except Exception as e:
        logger.error(f"Error seeding telemetry: {e}")
        db.rollback()

    finally:
        db.close()

if __name__ == "__main__":
    # Example: Seed 2024 Bahrain Grand Prix
    seed_telemetry_for_race(2024, 1, 'R')
    seed_telemetry_for_race(2024, 1, 'Q')
```

---

### Fase 6: Docker Setup (Día 13)

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: apexdata-postgres
    environment:
      POSTGRES_USER: apexuser
      POSTGRES_PASSWORD: apexpass
      POSTGRES_DB: apexdata
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U apexuser"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: apexdata-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # FastAPI Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: apexdata-backend
    environment:
      DATABASE_URL: postgresql://apexuser:apexpass@postgres:5432/apexdata
      REDIS_URL: redis://redis:6379
      FASTF1_CACHE_DIR: /app/cache
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - fastf1_cache:/app/cache
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Next.js Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: apexdata-frontend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000/api/v1
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    command: npm run dev

volumes:
  postgres_data:
  redis_data:
  fastf1_cache:
```

**backend/Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**frontend/Dockerfile**:
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

---

## Comparación: Proyecto Actual vs Nuevo Proyecto

| Aspecto | Proyecto Actual (Node.js) | Nuevo Proyecto (Python) |
|---------|---------------------------|-------------------------|
| **Backend** | Next.js API Routes | FastAPI (Python) |
| **ORM** | Prisma | SQLAlchemy |
| **Datos** | Jolpica API | FastF1 + Jolpica |
| **Telemetría** | ❌ No disponible | ✅ Completa (FastF1) |
| **Live Timing** | ❌ No | ✅ Sí (FastF1) |
| **Performance** | Buena | Excelente (pandas) |
| **Tipo de Datos** | Resultados básicos | Telemetría detallada |
| **Caching** | File-based | Redis |
| **Task Queue** | ❌ No | ✅ Celery |
| **API Docs** | Manual | Auto-generada |

---

## Funcionalidades Adicionales con FastF1

### 1. Visualizaciones de Telemetría
- Comparación de vueltas entre pilotos
- Gráficos de velocidad, throttle, brake
- Track maps con posiciones
- Análisis de sectores

### 2. Análisis de Neumáticos
- Degradación de neumáticos por stint
- Estrategias de pit stops
- Comparación de compuestos

### 3. Weather Data
- Temperatura de pista
- Temperatura ambiente
- Condiciones de lluvia
- Viento

### 4. Live Timing (FastF1)
- Posiciones en tiempo real
- Gaps entre pilotos
- Timing de sectores live
- Pit stop timing

### 5. Análisis Avanzados
- Heatmaps de rendimiento
- Comparación de racecraft
- Análisis de overtakes
- Fuel load estimation

---

## Timeline Estimado

| Fase | Duración | Tareas |
|------|----------|--------|
| **Fase 1** | 2 días | Setup inicial, estructura, Docker |
| **Fase 2** | 2 días | Modelos DB, migraciones |
| **Fase 3** | 3 días | Integración FastF1, servicios |
| **Fase 4** | 3 días | Frontend páginas telemetría |
| **Fase 5** | 2 días | Scripts de seed |
| **Fase 6** | 1 día | Docker, deployment |
| **Fase 7** | 2 días | Testing, optimización |
| **TOTAL** | **15 días** | Proyecto funcional completo |

---

## Comandos de Inicio Rápido

```bash
# 1. Clone y setup
git clone <repo>
cd apexdata-python

# 2. Start services
docker-compose up -d

# 3. Run migrations
docker-compose exec backend alembic upgrade head

# 4. Seed database
docker-compose exec backend python scripts/seed_seasons.py
docker-compose exec backend python scripts/seed_drivers.py
docker-compose exec backend python scripts/seed_races.py
docker-compose exec backend python scripts/seed_results.py
docker-compose exec backend python scripts/seed_qualifying.py
docker-compose exec backend python scripts/seed_telemetry.py

# 5. Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## Próximos Pasos Recomendados

1. **Priorizar Features**: Decidir qué visualizaciones de telemetría implementar primero
2. **Caching Strategy**: Implementar Redis para consultas frecuentes
3. **Background Jobs**: Usar Celery para procesamiento pesado de FastF1
4. **Monitoring**: Agregar Sentry para error tracking
5. **Performance**: Optimizar queries con indexes apropiados
6. **UI/UX**: Diseñar componentes reutilizables para gráficos

---

## Recursos Adicionales

- **FastF1 Docs**: https://docs.fastf1.dev/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Recharts**: https://recharts.org/

---

**¿Listo para comenzar?** 🏎️💨

Este stack te permitirá crear una aplicación de F1 mucho más poderosa con capacidades de análisis de telemetría que ninguna otra plataforma pública ofrece gratuitamente.
