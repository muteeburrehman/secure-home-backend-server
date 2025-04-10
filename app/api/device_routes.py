from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.device import DeviceCreate, DeviceOut, DeviceStatusUpdate
from app.database.db import get_db
from app.models.device import Device
from app.models.home import Home

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Create a new device for a given home
@router.post("/homes/{home_id}/devices/", response_model=DeviceOut, status_code=201)
def create_device(home_id: int, device_data: DeviceCreate, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    device_count = db.query(Device).filter(Device.home_id == home_id).count()
    if device_count >= 23:
        raise HTTPException(status_code=400, detail="Cannot add more than 23 devices per home")

    device = Device(name=device_data.name, status=device_data.status, home_id=home_id)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


# Get all devices for a home
@router.get("/homes/{home_id}/devices/", response_model=list[DeviceOut])
def list_devices(home_id: int, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    return db.query(Device).filter(Device.home_id == home_id).all()


# Update device status with HTML response
@router.put("/homes/{home_id}/devices/{device_id}/status", response_class=HTMLResponse)
def update_device_status(
        home_id: int,
        device_id: int,
        status_update: DeviceStatusUpdate,
        request: Request,
        db: Session = Depends(get_db)
):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    device = db.query(Device).filter(Device.id == device_id, Device.home_id == home_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    device.status = status_update.status
    db.commit()

    return templates.TemplateResponse(
        "device_status.html",
        {
            "request": request,
            "device_name": device.name,
            "home_name": home.owner,
            "status": device.status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
