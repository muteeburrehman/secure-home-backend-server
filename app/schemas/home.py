from pydantic import BaseModel

# For creating a new home
class HomeCreate(BaseModel):
    owner: str
    ip_address: str
    port: str

# For returning home data from DB
class HomeOut(HomeCreate):
    id: int

    class Config:
        from_attributes = True