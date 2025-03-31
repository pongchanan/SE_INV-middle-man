from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud, database
from database import get_db  # Ensure this is correctly defined

router = APIRouter(prefix="/service_requests", tags=["Service Requests"])

@router.post("/", response_model=schemas.ServiceRequestResponse)
def create_service_request(
    request: schemas.ServiceRequestCreate, 
    db: Session = Depends(database.get_db)
):
    org = db.query(models.Organization).filter(models.Organization.id == request.organization_id).first()
    if not org:
        raise HTTPException(status_code=400, detail="Invalid organization_id")

    new_request = models.ServiceRequest(**request.model_dump())  # Use model_dump() for Pydantic v2
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request
