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
