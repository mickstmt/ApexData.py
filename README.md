# ApexData.py 🏎️

ApexData is a Formula 1 data API powered by FastF1, built with FastAPI (Python) backend and designed for Next.js frontend integration.

## Features

- ✅ Complete F1 data API (Seasons, Drivers, Constructors, Races, Results, Qualifying)
- ✅ FastF1 integration for telemetry data
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Alembic migrations
- ✅ Auto-generated API documentation (Swagger/ReDoc)
- ✅ CORS enabled for frontend integration
- 🚧 Telemetry endpoints (coming soon)
- 🚧 Live timing data (coming soon)

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **Alembic** - Database migrations
- **FastF1** - F1 data and telemetry library
- **PostgreSQL** - Primary database
- **Pydantic** - Data validation

### Database
- **PostgreSQL 15+** - Main database
- **Redis** - Caching (optional, for future use)

## Project Structure

```
ApexData/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/        # API endpoints
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── db/           # Database config
│   │   ├── utils/        # Utilities
│   │   ├── config.py     # Settings
│   │   └── main.py       # FastAPI app
│   ├── alembic/          # Database migrations
│   ├── scripts/          # Seed scripts
│   ├── tests/            # Tests
│   ├── requirements.txt  # Python dependencies
│   └── .env             # Environment variables (not in git)
├── frontend/             # Next.js app (coming soon)
└── README.md

```

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/mickstmt/ApexData.py.git
cd ApexData.py
```

### 2. Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE apexdata_db;
```

### 3. Backend Setup

#### Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=apexdata_db

# Redis Configuration (optional for now)
REDIS_URL=redis://localhost:6379

# FastF1 Configuration
FASTF1_CACHE_DIR=./fastf1_cache

# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=ApexData API
VERSION=1.0.0

# CORS Origins (comma separated)
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

#### Run Database Migrations

```bash
alembic upgrade head
```

#### Start the Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs (Swagger): http://localhost:8000/docs
- Alternative Docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Base URLs
- Root: `http://localhost:8000/`
- API v1: `http://localhost:8000/api/v1/`
- Health: `http://localhost:8000/health`

### Available Endpoints

#### Seasons
- `GET /api/v1/seasons/` - Get all seasons
- `GET /api/v1/seasons/{year}` - Get season by year
- `POST /api/v1/seasons/` - Create new season
- `PUT /api/v1/seasons/{year}` - Update season
- `DELETE /api/v1/seasons/{year}` - Delete season

#### Drivers
- `GET /api/v1/drivers/` - Get all drivers
- `GET /api/v1/drivers/{driver_id}` - Get driver by ID
- `POST /api/v1/drivers/` - Create new driver
- `PUT /api/v1/drivers/{driver_id}` - Update driver
- `DELETE /api/v1/drivers/{driver_id}` - Delete driver

#### Constructors
- `GET /api/v1/constructors/` - Get all constructors
- `GET /api/v1/constructors/{constructor_id}` - Get constructor by ID
- `POST /api/v1/constructors/` - Create new constructor
- `PUT /api/v1/constructors/{constructor_id}` - Update constructor
- `DELETE /api/v1/constructors/{constructor_id}` - Delete constructor

#### Races
- `GET /api/v1/races/` - Get all races
- `GET /api/v1/races/{race_id}` - Get race by ID
- `GET /api/v1/races/season/{year}` - Get races by season
- `POST /api/v1/races/` - Create new race
- `PUT /api/v1/races/{race_id}` - Update race
- `DELETE /api/v1/races/{race_id}` - Delete race

## Database Models

### Core Models
- **Season**: F1 seasons (year, wikipedia_url)
- **Driver**: F1 drivers (driver_id, code, name, nationality, etc.)
- **Constructor**: F1 teams (constructor_id, name, nationality)
- **Race**: Grand Prix events (race_name, circuit, date, etc.)
- **RaceResult**: Race results (position, points, times, etc.)
- **Qualifying**: Qualifying results (Q1, Q2, Q3 times)

### Telemetry Models (Coming Soon)
- **LapData**: Lap-by-lap data
- **TelemetryPoint**: Detailed telemetry points

## Development

### Running Tests

```bash
cd backend
pytest
```

### Creating a New Migration

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Seeding Data

Seed scripts will be available in `backend/scripts/` for populating the database with F1 data.

## Next Steps

- [ ] Create seed scripts for historical F1 data
- [ ] Implement telemetry endpoints
- [ ] Add FastF1 live timing integration
- [ ] Create Next.js frontend
- [ ] Add Redis caching
- [ ] Implement Celery for background tasks
- [ ] Add authentication & authorization
- [ ] Deploy to production

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Acknowledgments

- [FastF1](https://github.com/theOehrly/Fast-F1) - F1 data library
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Ergast API](http://ergast.com/mrd/) - Historical F1 data

---

Built with ❤️ for F1 fans
