from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, func, UniqueConstraint
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    pass

class Organization(Base):
    __tablename__ = "organizations"

    name = mapped_column(String, primary_key=True, index=True, unique=True)
    password = mapped_column(String)

class Locker(Base):
    __tablename__ = "lockers"

    locker_id = mapped_column(Integer, primary_key=True, index=True, unique=True, autoincrement=False)

    service_requests = relationship("ServiceRequest", back_populates="locker", cascade="all, delete")

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    service_request_id = mapped_column(Integer, primary_key=True, index=True)
    locker_id = mapped_column(Integer, ForeignKey("lockers.locker_id"))
    request_id = mapped_column(Integer)
    organization_name = mapped_column(String, ForeignKey("organizations.name"))

    organization = relationship("Organization")
    locker = relationship("Locker", back_populates="service_requests")  
    dates = relationship("ServiceRequestDate", back_populates="service_request", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="service_request", cascade="all, delete-orphan")

    # same request id from the same organization is not allowed: enforced in crud


class ServiceRequestDate(Base):
    __tablename__ = "service_request_dates"

    service_request_date_id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    use_date = mapped_column(Date)
    service_request_id = mapped_column(Integer, ForeignKey("service_requests.service_request_id"))

    service_request = relationship("ServiceRequest", back_populates="dates")

    # same use date on the same locker is not allowed: enforced in crud



class Log(Base):
    __tablename__ = "logs"

    log_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    locker_id = mapped_column(Integer)
    timestamp = mapped_column(DateTime, default=func.now())
    actor = mapped_column(String)
    action = mapped_column(String)
    service_request_id = mapped_column(Integer, ForeignKey("service_requests.service_request_id", ondelete="CASCADE"))

    service_request = relationship("ServiceRequest", back_populates="logs")