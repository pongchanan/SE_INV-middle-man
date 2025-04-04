from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# import schemas, crud, database
from .. import schemas, crud, database
from ..database import get_db
from .. import models

router = APIRouter(prefix="/service_requests", tags=["Service Requests"])

@router.post("/new", response_model=schemas.ServiceRequestResponse)
def create_service_request(
    service_request: schemas.ServiceRequestCreate, 
    db: Session = Depends(database.get_db)
):
    try:
        new_request = crud.create_service_request(db, service_request)
        return new_request
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{service_request_id}", response_model=schemas.MessageResponse)
def delete_service_request_endpoint(service_request_id: str, db: Session = Depends(get_db)):
    return crud.delete_service_request(db, service_request_id)

@router.post("/add_date", response_model=schemas.MessageResponse)
def add_date_endpoint(request: schemas.ServiceRequestDateBase, db: Session = Depends(get_db)):
    return crud.add_date(db, request.service_request_id, request.use_date)

@router.delete("/remove_date", response_model=schemas.MessageResponse)
def remove_date_endpoint(request: schemas.ServiceRequestDateBase, db: Session = Depends(get_db)):
    return crud.remove_date(db, request.service_request_id, request.use_date)

@router.get("/get/{request_id}/{organization_name}")
def get_service_request_endpoint(request_id: str, organization_name: str, db: Session = Depends(get_db)):
    services = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.request_id == request_id,
        models.ServiceRequest.organization_name == organization_name
    ).all()
    if not services:
        raise HTTPException(status_code=404, detail="Service Request not found")
    return services