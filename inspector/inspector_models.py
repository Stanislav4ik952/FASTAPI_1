from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Inspector(Base):
    __tablename__ = "inspectors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    patronymic = Column(String)
    position = Column(String)
    department = Column(String)
    phone_number = Column(String)
    appointment_date = Column(String)
    training_date = Column(String)

    # Связь с отчетами
    reports = relationship("Report", back_populates="inspector")
