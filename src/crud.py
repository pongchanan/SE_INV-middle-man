from sqlalchemy.orm import Session
import models, schemas

def create_organization(db: Session, org: schemas.OrganizationCreate):
    db_org = models.Organization(name=org.name, password=org.password, manager=org.manager)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def get_organization(db: Session, org_id: int):
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()

def create_service_request(db: Session, request: schemas.ServiceRequestCreate):
    db_request = models.ServiceRequest(organization_id=request.organization_id, request_data=request.request_data)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request
