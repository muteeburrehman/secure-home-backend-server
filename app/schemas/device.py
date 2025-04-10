from pydantic import BaseModel

class DeviceCreate(BaseModel):
    name: str
    status: bool = False

class DeviceStatusUpdate(BaseModel):
    status: bool

class DeviceOut(BaseModel):
    id: int
    name: str
    status: bool
    home_id: int

    class Config:
        from_attributes = True