from pydantic import BaseModel
from typing import Optional

class ReportCreate(BaseModel):
    inspector_id: int
    public_inspector_report: str
    checks_count: int
    violations_count: int
    report_date: str

class ReportUpdate(BaseModel):
    inspector_id: Optional[int] = None
    public_inspector_report: Optional[str] = None
    checks_count: Optional[int] = None
    violations_count: Optional[int] = None
    report_date: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    inspector_id: int
    public_inspector_report: str
    checks_count: int
    violations_count: int
    report_date: str

    class Config:
        from_attributes = True
