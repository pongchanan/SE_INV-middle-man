from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from database import get_db

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.post("/new", response_model=schemas.OrganizationResponse)
def create_organization(
    organization: schemas.OrganizationCreate,
    db: Session = Depends(database.get_db)
):
    try:
        new_organization = crud.create_organization(db, organization)
    except HTTPException as e:
        raise e
    return new_organization