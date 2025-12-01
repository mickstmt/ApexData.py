from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.models.driver import Driver
from app.schemas.driver import DriverResponse, DriverCreate, DriverUpdate

router = APIRouter()


@router.get("/", response_model=List[DriverResponse])
def get_drivers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all drivers.
    """
    drivers = db.query(Driver).order_by(Driver.family_name).offset(skip).limit(limit).all()
    return drivers


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: str, db: Session = Depends(get_db)):
    """
    Get a specific driver by driver_id.
    """
    driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail=f"Driver {driver_id} not found")
    return driver


@router.post("/", response_model=DriverResponse, status_code=201)
def create_driver(driver_data: DriverCreate, db: Session = Depends(get_db)):
    """
    Create a new driver.
    """
    # Check if driver already exists
    existing = db.query(Driver).filter(Driver.driver_id == driver_data.driver_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Driver {driver_data.driver_id} already exists")

    driver = Driver(**driver_data.model_dump())
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: str, driver_data: DriverUpdate, db: Session = Depends(get_db)):
    """
    Update a driver.
    """
    driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail=f"Driver {driver_id} not found")

    update_data = driver_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(driver, key, value)

    db.commit()
    db.refresh(driver)
    return driver


@router.delete("/{driver_id}", status_code=204)
def delete_driver(driver_id: str, db: Session = Depends(get_db)):
    """
    Delete a driver.
    """
    driver = db.query(Driver).filter(Driver.driver_id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail=f"Driver {driver_id} not found")

    db.delete(driver)
    db.commit()
    return None
