from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database.db import Base

class Home(Base):
    __tablename__ = "homes"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, nullable=False)
    ip_address = Column(String, nullable=False, unique=True)
    port = Column(String, nullable=False)

    # Relationship to the Device model
    devices = relationship("Device", back_populates="home", cascade="all, delete-orphan")
