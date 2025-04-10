from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    home_id = Column(Integer, ForeignKey("homes.id"), nullable=False)  # Foreign key to Home

    # Relationship to the Home model
    home = relationship("Home", back_populates="devices")

    # Relationship to the Schedule model
    schedules = relationship("Schedule", back_populates="device", cascade="all, delete")

    # Relationship to DeviceSchedule (one-to-one)
    device_schedule = relationship("DeviceSchedule", back_populates="device", uselist=False, cascade="all, delete")
