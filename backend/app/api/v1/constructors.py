from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.models.constructor import Constructor
from app.schemas.constructor import ConstructorResponse, ConstructorCreate, ConstructorUpdate

router = APIRouter()


@router.get("/", response_model=List[ConstructorResponse])
def get_constructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all constructors.
    """
    constructors = db.query(Constructor).order_by(Constructor.name).offset(skip).limit(limit).all()
    return constructors


@router.get("/{constructor_id}", response_model=ConstructorResponse)
def get_constructor(constructor_id: str, db: Session = Depends(get_db)):
    """
    Get a specific constructor by constructor_id.
    """
    constructor = db.query(Constructor).filter(Constructor.constructor_id == constructor_id).first()
    if not constructor:
        raise HTTPException(status_code=404, detail=f"Constructor {constructor_id} not found")
    return constructor


@router.post("/", response_model=ConstructorResponse, status_code=201)
def create_constructor(constructor_data: ConstructorCreate, db: Session = Depends(get_db)):
    """
    Create a new constructor.
    """
    # Check if constructor already exists
    existing = db.query(Constructor).filter(Constructor.constructor_id == constructor_data.constructor_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Constructor {constructor_data.constructor_id} already exists")

    constructor = Constructor(**constructor_data.model_dump())
    db.add(constructor)
    db.commit()
    db.refresh(constructor)
    return constructor


@router.put("/{constructor_id}", response_model=ConstructorResponse)
def update_constructor(constructor_id: str, constructor_data: ConstructorUpdate, db: Session = Depends(get_db)):
    """
    Update a constructor.
    """
    constructor = db.query(Constructor).filter(Constructor.constructor_id == constructor_id).first()
    if not constructor:
        raise HTTPException(status_code=404, detail=f"Constructor {constructor_id} not found")

    update_data = constructor_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(constructor, key, value)

    db.commit()
    db.refresh(constructor)
    return constructor


@router.delete("/{constructor_id}", status_code=204)
def delete_constructor(constructor_id: str, db: Session = Depends(get_db)):
    """
    Delete a constructor.
    """
    constructor = db.query(Constructor).filter(Constructor.constructor_id == constructor_id).first()
    if not constructor:
        raise HTTPException(status_code=404, detail=f"Constructor {constructor_id} not found")

    db.delete(constructor)
    db.commit()
    return None
