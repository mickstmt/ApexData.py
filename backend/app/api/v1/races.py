from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.models.race import Race
from app.schemas.race import RaceResponse, RaceCreate, RaceUpdate

router = APIRouter()


@router.get("/", response_model=List[RaceResponse])
def get_races(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all races.
    """
    races = db.query(Race).order_by(Race.date.desc()).offset(skip).limit(limit).all()
    return races


@router.get("/{race_id}", response_model=RaceResponse)
def get_race(race_id: str, db: Session = Depends(get_db)):
    """
    Get a specific race by ID.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail=f"Race {race_id} not found")
    return race


@router.get("/season/{year}", response_model=List[RaceResponse])
def get_races_by_season(year: int, db: Session = Depends(get_db)):
    """
    Get all races for a specific season.
    """
    from app.models.season import Season

    season = db.query(Season).filter(Season.year == year).first()
    if not season:
        raise HTTPException(status_code=404, detail=f"Season {year} not found")

    races = db.query(Race).filter(Race.season_id == season.id).order_by(Race.round).all()
    return races


@router.post("/", response_model=RaceResponse, status_code=201)
def create_race(race_data: RaceCreate, db: Session = Depends(get_db)):
    """
    Create a new race.
    """
    race = Race(**race_data.model_dump())
    db.add(race)
    db.commit()
    db.refresh(race)
    return race


@router.put("/{race_id}", response_model=RaceResponse)
def update_race(race_id: str, race_data: RaceUpdate, db: Session = Depends(get_db)):
    """
    Update a race.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail=f"Race {race_id} not found")

    update_data = race_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(race, key, value)

    db.commit()
    db.refresh(race)
    return race


@router.delete("/{race_id}", status_code=204)
def delete_race(race_id: str, db: Session = Depends(get_db)):
    """
    Delete a race.
    """
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise HTTPException(status_code=404, detail=f"Race {race_id} not found")

    db.delete(race)
    db.commit()
    return None
