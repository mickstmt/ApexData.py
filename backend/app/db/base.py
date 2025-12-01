# Import all models here for Alembic to detect them
from app.db.database import Base
from app.models.season import Season
from app.models.driver import Driver
from app.models.constructor import Constructor
from app.models.race import Race
from app.models.result import RaceResult
from app.models.qualifying import Qualifying
