from pydantic import BaseModel
from typing import Optional

class InspectorCreate(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    position: str
    department: str
    phone_number: str
    appointment_date: str
    training_date: str

class InspectorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    phone_number: Optional[str] = None
    appointment_date: Optional[str] = None
    training_date: Optional[str] = None

class InspectorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    position: str
    department: str
    phone_number: str
    appointment_date: str
    training_date: str

    class Config:
        from_attributes = True
