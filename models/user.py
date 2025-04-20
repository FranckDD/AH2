from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import bcrypt


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)  # BCrypt hash
    full_name = Column(String(100), nullable=False)
    postgres_role = Column(String(20))
    is_active = Column(Boolean, default=True)
    specialty_id = Column(Integer, ForeignKey('medical_specialties.specialty_id'))
    role_id = Column(Integer, ForeignKey('application_roles.role_id'))

    from models.application_role import ApplicationRole
    role = relationship("ApplicationRole", back_populates="users")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))