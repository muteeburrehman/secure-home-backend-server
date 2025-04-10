from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.home import HomeCreate, HomeOut
from app.models.home import Home
from app.database.db import get_db

router = APIRouter()

# Create a new home
@router.post("/homes/", response_model=HomeOut)
def create_home(home: HomeCreate, db: Session = Depends(get_db)):
    # Check if home already exists based on IP address (or other unique criteria)
    db_home = db.query(Home).filter(Home.ip_address == home.ip_address).first()
    if db_home:
        raise HTTPException(status_code=400, detail="Home with this IP address already exists")

    new_home = Home(**home.dict())  # Create a new Home object
    db.add(new_home)  # Add the new home to the database
    db.commit()  # Commit the transaction
    db.refresh(new_home)  # Refresh the object to get the newly created data

    return new_home

# List all homes
@router.get("/homes/", response_model=list[HomeOut])
def list_homes(db: Session = Depends(get_db)):
    homes = db.query(Home).all()  # Get all homes from the database
    return homes

