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