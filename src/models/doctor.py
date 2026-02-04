from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from src.database import Base


class Doctor(Base):
    __tablename__ = "dheeraj_doctors"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
