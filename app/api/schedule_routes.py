# app/api/schedule_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.schedule import ScheduleCreate, DeviceScheduleOut, ScheduleOut
from app.models.device import Device
from app.models.home import Home
from app.models.schedule import Schedule as ScheduleModel, DeviceSchedule as DeviceScheduleModel

router = APIRouter()


# Create a schedule for a device
@router.post("/homes/{home_id}/devices/{device_id}/schedule", response_model=dict)
def create_schedule(home_id: int, device_id: int, schedule: ScheduleCreate, db: Session = Depends(get_db)):
    # Validate home and device existence
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    device = db.query(Device).filter(Device.id == device_id, Device.home_id == home_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Check if a DeviceSchedule exists
    device_schedule = db.query(DeviceScheduleModel).filter_by(device_id=device_id).first()
    if not device_schedule:
        device_schedule = DeviceScheduleModel(device_id=device_id)
        db.add(device_schedule)
        db.commit()
        db.refresh(device_schedule)

    # Create new schedule with both device_id and device_schedule_id
    new_schedule = ScheduleModel(
        time=schedule.time,
        operation=schedule.operation,
        days=",".join(map(str, schedule.days)),
        device_id=device_id,  # Make sure to set this
        device_schedule_id=device_schedule.id
    )
    db.add(new_schedule)
    db.commit()

    return {"message": "Schedule created successfully"}


# Get schedules for a device
@router.get("/homes/{home_id}/devices/{device_id}/schedule", response_model=DeviceScheduleOut)
def get_device_schedule(home_id: int, device_id: int, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    device = db.query(Device).filter(Device.id == device_id, Device.home_id == home_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    device_schedule = db.query(DeviceScheduleModel).filter_by(device_id=device_id).first()
    if not device_schedule:
        return {"device_id": device_id, "schedules": []}

    # Convert schedule days from string to list of integers when returning
    schedules_out = []
    for schedule in device_schedule.schedules:
        schedule_dict = {
            "id": schedule.id,
            "time": schedule.time,
            "operation": schedule.operation,
            "days": [int(day) for day in schedule.days.split(",") if day]
        }
        schedules_out.append(schedule_dict)

    return {"device_id": device_id, "schedules": schedules_out}


# Delete a schedule
@router.delete("/homes/{home_id}/devices/{device_id}/schedule/{schedule_id}", response_model=dict)
def delete_schedule(home_id: int, device_id: int, schedule_id: int, db: Session = Depends(get_db)):
    # Validate home and device existence
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    device = db.query(Device).filter(Device.id == device_id, Device.home_id == home_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Find and delete the schedule
    schedule = db.query(ScheduleModel).filter(
        ScheduleModel.id == schedule_id,
        ScheduleModel.device_id == device_id
    ).first()

    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    db.delete(schedule)
    db.commit()

    return {"message": "Schedule deleted successfully"}