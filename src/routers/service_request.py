from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from database import get_db

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
def delete_service_request_endpoint(service_request_id: int, db: Session = Depends(get_db)):
    return crud.delete_service_request(db, service_request_id)

@router.post("/add_date", response_model=schemas.MessageResponse)
def add_date_endpoint(request: schemas.ServiceRequestDateBase, db: Session = Depends(get_db)):
    return crud.add_date(db, request.service_request_id, request.use_date)

@router.delete("/remove_date", response_model=schemas.MessageResponse)
def remove_date_endpoint(request: schemas.ServiceRequestDateBase, db: Session = Depends(get_db)):
    return crud.remove_date(db, request.service_request_id, request.use_date)