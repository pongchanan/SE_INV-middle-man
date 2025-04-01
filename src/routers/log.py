from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from database import get_db

router = APIRouter(prefix="/log", tags=["Logs"])

@router.post("/new", response_model=schemas.LogResponse)
def create_log(
    log: schemas.LogCreate,
    db: Session = Depends(database.get_db)
):
    try:
        now_log = crud.create_log(db, log)
    except HTTPException as e:
        raise e
    return now_log

@router.delete("/delete/{log_id}", response_model=schemas.MessageResponse)
def delete_log_endpoint(log_id: int, db: Session = Depends(get_db)):
    return crud.delete_log(db, log_id)