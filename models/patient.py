from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Patient(Base):
    __tablename__ = 'patients'
    
    patient_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    birth_date = Column(Date)
    gender = Column(String(10))
    national_id = Column(String(20))
    contact_phone = Column(String(20))
    assurance = Column(String(20))
    residence = Column(String)