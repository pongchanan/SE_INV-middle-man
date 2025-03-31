from pydantic import BaseModel

class OrganizationBase(BaseModel):
    name: str
    password: str
    manager: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int

    class Config:
        from_attributes = True

class ServiceRequestBase(BaseModel):
    organization_id: int
    request_data: str

class ServiceRequestCreate(ServiceRequestBase):
    pass

class ServiceRequestResponse(ServiceRequestBase):
    id: int

    class Config:
        from_attributes = True
