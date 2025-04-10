from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base


class DeviceSchedule(Base):
    __tablename__ = "device_schedules"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), unique=True)

    # Relationship to the Device model
    device = relationship("Device", back_populates="device_schedule")

    # Relationship to schedules
    schedules = relationship("Schedule", back_populates="device_schedule")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(String, nullable=False)
    operation = Column(Boolean, nullable=False)
    days = Column(String, default="0,1,2,3,4,5,6")  # Comma-separated (days of the week)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)  # Foreign key to devices table
    device_schedule_id = Column(Integer, ForeignKey("device_schedules.id"))  # Foreign key to device_schedules table

    # Relationship to Device
    device = relationship("Device", back_populates="schedules")

    # Relationship to DeviceSchedule
    device_schedule = relationship("DeviceSchedule", back_populates="schedules")