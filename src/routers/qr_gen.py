from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import requests
from datetime import date
from typing import Optional
import json
import schemas, crud, database, models
from database import get_db

router = APIRouter(prefix="/qr", tags=["QR Code"])

HARDWARE_API_URL = "PLEASEHELPME"

@router.get("/request/{service_request_id}/{use_date}", response_model=schemas.QRCodeResponse)
def request_qr_code(
    service_request_id: int,
    use_date: date,
    db: Session = Depends(database.get_db)
):
    service_request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.service_request_id == service_request_id
    ).first()
    
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    date_record = db.query(models.ServiceRequestDate).filter(
        models.ServiceRequestDate.service_request_id == service_request_id,
        models.ServiceRequestDate.use_date == use_date
    ).first()
    
    if not date_record:
        raise HTTPException(status_code=404, detail="Date not associated with this service request")
    
    organization = db.query(models.Organization).filter(
        models.Organization.name == service_request.organization_name
    ).first()
    
    hardware_request_data = {
        "start_date": str(use_date),
        "end_date": str(use_date),
        "username": organization.name,
        "locker_id": service_request.locker_id,
        "request_id": str(service_request.request_id)
    }
    
    try:
        response = requests.post(
            HARDWARE_API_URL,
            data=hardware_request_data
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to generate QR code from hardware service: {response.text}"
            )

        qr_data = response.json().get("qr_code") if response.headers.get("content-type") == "application/json" else response.text
        
        log_data = schemas.LogCreate(
            locker_id=service_request.locker_id,
            actor=f"System-{organization.name}",
            action="QR_CODE_GENERATED"
        )
        crud.create_log(db, log_data)
        
        return schemas.QRCodeResponse(
            service_request_id=service_request_id,
            organization_name=service_request.organization_name,
            locker_id=service_request.locker_id,
            use_date=use_date,
            qr_code=qr_data
        )
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error connecting to hardware service: {str(e)}"
        )