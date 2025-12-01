from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.models.season import Season
from app.schemas.season import SeasonResponse, SeasonCreate, SeasonUpdate

router = APIRouter()


@router.get("/", response_model=List[SeasonResponse])
def get_seasons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all seasons.
    """
    seasons = db.query(Season).order_by(Season.year.desc()).offset(skip).limit(limit).all()
    return seasons


@router.get("/{year}", response_model=SeasonResponse)
def get_season(year: int, db: Session = Depends(get_db)):
    """
    Get a specific season by year.
    """
    season = db.query(Season).filter(Season.year == year).first()
    if not season:
        raise HTTPException(status_code=404, detail=f"Season {year} not found")
    return season


@router.post("/", response_model=SeasonResponse, status_code=201)
def create_season(season_data: SeasonCreate, db: Session = Depends(get_db)):
    """
    Create a new season.
    """
    # Check if season already exists
    existing = db.query(Season).filter(Season.year == season_data.year).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Season {season_data.year} already exists")

    season = Season(**season_data.model_dump())
    db.add(season)
    db.commit()
    db.refresh(season)
    return season


@router.put("/{year}", response_model=SeasonResponse)
def update_season(year: int, season_data: SeasonUpdate, db: Session = Depends(get_db)):
    """
    Update a season.
    """
    season = db.query(Season).filter(Season.year == year).first()
    if not season:
        raise HTTPException(status_code=404, detail=f"Season {year} not found")

    update_data = season_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(season, key, value)

    db.commit()
    db.refresh(season)
    return season


@router.delete("/{year}", status_code=204)
def delete_season(year: int, db: Session = Depends(get_db)):
    """
    Delete a season.
    """
    season = db.query(Season).filter(Season.year == year).first()
    if not season:
        raise HTTPException(status_code=404, detail=f"Season {year} not found")

    db.delete(season)
    db.commit()
    return None
