from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    inspector_id = Column(Integer, ForeignKey('inspectors.id'))
    public_inspector_report = Column(String)
    checks_count = Column(Integer)
    violations_count = Column(Integer)
    report_date = Column(String)

    inspector = relationship("Inspector", back_populates="reports")
