from pydantic import BaseModel
from typing import List

class ScheduleBase(BaseModel):
    time: str
    operation: bool
    days: List[int]

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleOut(ScheduleBase):
    id: int

    class Config:
        from_attributes = True  # Fixed typo here (was from_attribute)

class DeviceScheduleOut(BaseModel):
    device_id: int
    schedules: List[ScheduleOut]

    class Config:
        from_attributes = True  # Fixed typo here (was from_attribute)