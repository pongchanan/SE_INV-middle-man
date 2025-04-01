from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

class QRCodeResponse(BaseModel):
    service_request_id: int
    organization_name: str
    locker_id: int
    use_date: date
    qr_code: str  # Base64 encoded QR code image or encrypted data
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    detail: str

# ============================== Organization ==============================
class OrganizationBase(BaseModel):
    name: str
    password: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    name: str

    class Config:
        from_attributes = True

# ============================== Locker ==============================
class LockerBase(BaseModel):
    locker_id: int

class LockerCreate(LockerBase):
    pass

class LockerResponse(LockerBase):
    class Config:
        from_attributes = True

# ============================== SR ==============================
class ServiceRequestBase(BaseModel):
    request_id: int
    organization_name: str

class ServiceRequestCreate(ServiceRequestBase):
    organization_password: str
    use_dates: List[date]

class ServiceRequestResponse(ServiceRequestBase):
    locker_id: int
    use_dates: List[date]

    class Config:
        from_attributes = True

class ServiceRequestDateBase(BaseModel):
    service_request_id: int
    use_date: date

# ============================== Log ==============================
class LogBase(BaseModel):
    locker_id: int
    timestamp: Optional[datetime] = None
    actor: str
    action: str

class LogCreate(LogBase):
    pass

class LogResponse(LogBase):
    log_id: int
    service_request_id: Optional[int] = None

    class Config:   
        from_attributes = True