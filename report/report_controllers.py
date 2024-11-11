from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from report.report_models import Report
from report.report_schemas import ReportCreate, ReportUpdate, ReportResponse
from typing import List
from fastapi.security import HTTPBearer

# Создаем HTTPBearer схему для проверки токена
oauth2_scheme = HTTPBearer()

router = APIRouter()

# Создание отчета
@router.post("/", response_model=ReportResponse, dependencies=[Depends(oauth2_scheme)])
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    new_report = Report(**report.model_dump())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

# Чтение всех отчетов
@router.get("/", response_model=List[ReportResponse], dependencies=[Depends(oauth2_scheme)])
def read_reports(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Report).offset(skip).limit(limit).all()

# Чтение отчета по ID
@router.get("/{report_id}", response_model=ReportResponse, dependencies=[Depends(oauth2_scheme)])
def read_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

# Обновление отчета
@router.put("/{report_id}", response_model=ReportResponse, dependencies=[Depends(oauth2_scheme)])
def update_report(report_id: int, report_update: ReportUpdate, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in report_update.model_dump(exclude_unset=True).items():
        setattr(db_report, key, value)

    db.commit()
    db.refresh(db_report)
    return db_report

# Удаление отчета
@router.delete("/{report_id}", dependencies=[Depends(oauth2_scheme)])
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()
    return {"detail": "Report deleted"}
