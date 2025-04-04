from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import requests
from datetime import date
from typing import Optional
import json
# import schemas, crud, database, models
from .. import schemas, crud, database
from ..database import get_db
from .. import models

import base64
from cryptography.fernet import Fernet
import json
import hashlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

router = APIRouter(prefix="/qr", tags=["QR Code"])

HARDWARE_API_URL = "PLEASEHELPME"

@router.get("/request/{service_request_id}/{use_date}/{actor}")
def request_qr_code(
    service_request_id: int,
    use_date: date,
    actor: Optional[str] = "Admin",
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
    
    load_dotenv()
    key = os.getenv("SECRET_KEY")
    if not key:
        raise HTTPException(status_code=500, detail="SECRET_KEY not found in environment variables")
    # Hash the key to ensure it's exactly 32 bytes
    hashed_key = hashlib.sha256(key.encode("utf-8")).digest()[:32]  # No need for .encode()

    # Encode to URL-safe base64
    encoded_key = base64.urlsafe_b64encode(hashed_key)

    cipher = Fernet(encoded_key)
    
    hardware_request_data = {
        "start_date": str(use_date),
        "end_date": str(use_date),
        "actor": actor,
        "locker_id": service_request.locker_id,
        "request_id": service_request.request_id
    }
    
    json_data = json.dumps(hardware_request_data).encode()
    encrypted_data = cipher.encrypt(json_data)
    
    return encrypted_data
        
@router.get("/obtain_qr_str")
def obtain_qr_str(
    user: str,
    request_id: str,
    organization_name: str,
    db: Session = Depends(database.get_db)
):  
    request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.request_id == request_id,
        models.ServiceRequest.organization_name == organization_name
    ).first()
    
    if request is None:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    locker_id = request.locker.locker_id

    load_dotenv()
    key = os.getenv("SECRET_KEY")
    if not key:
        raise HTTPException(status_code=500, detail="SECRET_KEY not found in environment variables")
    # Hash the key to ensure it's exactly 32 bytes
    hashed_key = hashlib.sha256(key.encode("utf-8")).digest()[:32]  # No need for .encode()

    # Encode to URL-safe base64
    encoded_key = base64.urlsafe_b64encode(hashed_key)

    cipher = Fernet(encoded_key)
    
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    data = {
        "start_date": str(today),
        "end_date": str(tomorrow),
        "actor": user,
        "request_id": request_id,
        "locker_id": locker_id,
    }
    
    json_data = json.dumps(data).encode()
    encrypted_data = cipher.encrypt(json_data)
    
    return encrypted_data