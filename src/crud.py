from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from fastapi import HTTPException
import models, schemas

# ============================== Organization ==============================
def create_organization(db: Session, org: schemas.OrganizationCreate):
    db_org = models.Organization(name=org.name, password=org.password)
    db.add(db_org)
    
    try:
        db.commit()
        db.refresh(db_org)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Organization with this name already exists.")
    
    return db_org

# ============================== Locker ==============================
def create_locker(db: Session, locker: schemas.LockerCreate):
    db_locker = models.Locker(locker_id=locker.locker_id)
    db.add(db_locker)
    
    try:
        db.commit()
        db.refresh(db_locker)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Locker with this id already exists.")
    
    return db_locker

def delete_locker(db: Session, locker_id: int):
    db_locker = db.query(models.Locker).filter(models.Locker.locker_id == locker_id).first()

    if db_locker is None:
        # If the locker is not found, raise an HTTP exception
        raise HTTPException(status_code=404, detail="Locker not found.")

    try:
        db.delete(db_locker)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting locker: {e}")

    return {"detail": "Locker deleted successfully"}

# ============================== SR ==============================
def create_service_request(db: Session, service_request: schemas.ServiceRequestCreate):
    # Check if the organization exists
    organization = db.query(models.Organization).filter(models.Organization.name == service_request.organization_name).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Check if the organization password is correct
    if organization.password != service_request.organization_password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # Check if a service request already exists with the same request_id and organization_name
    existing_request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.request_id == service_request.request_id,
        models.ServiceRequest.organization_name == service_request.organization_name
    ).first()

    if existing_request:
        raise HTTPException(status_code=400, detail="Service request with this request_id and organization already exists")

    # List to track all the use dates
    use_dates = service_request.use_dates

    # Find an available locker for all use dates
    available_locker = None

    # Check all lockers to find one that is available for all requested use_dates
    lockers = db.query(models.Locker).all()

    for locker in lockers:
        # Check if the locker is available for all requested use_dates
        is_available = True
        for use_date in use_dates:
            conflicting_date = db.query(models.ServiceRequestDate).join(models.ServiceRequest).filter(
                models.ServiceRequest.locker_id == locker.locker_id,
                models.ServiceRequestDate.use_date == use_date
            ).first()

            if conflicting_date:
                is_available = False
                break  # No need to check further if one date conflicts

        if is_available:
            available_locker = locker
            break  # Found an available locker, break out of the loop

    # If no locker is available, raise an error
    if not available_locker:
        raise HTTPException(status_code=400, detail="No locker available for the requested dates")

    # If an available locker is found, create the new service request
    new_request = models.ServiceRequest(
        request_id=service_request.request_id,
        organization_name=service_request.organization_name,
        locker_id=available_locker.locker_id
    )

    db.add(new_request)
    db.flush()  # Flush to get the service_request_id for the new entry

    # Add the service request dates
    for use_date in use_dates:
        date_record = models.ServiceRequestDate(
            service_request_id=new_request.service_request_id, 
            use_date=use_date
        )
        db.add(date_record)
        db.flush()  

    db.commit()
    db.refresh(new_request)

    # Prepare the response with the assigned locker
    use_dates = [date.use_date for date in new_request.dates]

    return schemas.ServiceRequestResponse(
        service_request_id=new_request.service_request_id,
        request_id=new_request.request_id,
        organization_name=new_request.organization_name,
        locker_id=available_locker.locker_id,
        use_dates=use_dates,
    )


# ============================== Log ==============================
def create_log(db: Session, log: schemas.LogCreate):
    log_timestamp = log.timestamp if log.timestamp else datetime.now(timezone.utc)

    service_request = (
        db.query(models.ServiceRequest)
        .join(models.ServiceRequestDate, models.ServiceRequest.service_request_id == models.ServiceRequestDate.service_request_id)
        .filter(
            models.ServiceRequest.locker_id == log.locker_id,
            models.ServiceRequestDate.use_date == log_timestamp.date()
        )
        .first()
    )

    db_log = models.Log(
        locker_id=log.locker_id,
        actor=log.actor,
        action=log.action,
        timestamp=log_timestamp,  # Use the processed timestamp
        service_request_id=service_request.service_request_id if service_request else None
    )
    db.add(db_log)
    
    try:
        db.commit()
        db.refresh(db_log)
    except Exception as e:
        db.rollback()
        raise e

    # Create a LogResponse with all fields from the database object
    return schemas.LogResponse(
        log_id=db_log.log_id,
        locker_id=db_log.locker_id,
        actor=db_log.actor,
        action=db_log.action,
        timestamp=db_log.timestamp,
        service_request_id=db_log.service_request_id
    )