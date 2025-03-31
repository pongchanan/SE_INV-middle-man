from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from database import get_db

router = APIRouter(prefix="/lockers", tags=["Lockers"])

@router.post("/new", response_model=schemas.LockerCreate)
def create_locker(
    locker: schemas.LockerCreate,
    db: Session = Depends(database.get_db)
):
    try:
        new_locker = crud.create_locker(db, locker)
    except HTTPException as e:
        raise e
    return new_locker

@router.delete("/delete/{locker_id}", response_model=schemas.MessageResponse)
def delete_locker(
    locker_id: int,
    db: Session = Depends(database.get_db)
):
    try:
        result = crud.delete_locker(db, locker_id)
    except HTTPException as e:
        raise e
    return result