from passlib.context import CryptContext
from ..models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db_session):
        self.session = db_session
    
    def authenticate(self, username: str, password: str) -> User:
        user = self.session.query(User).filter_by(username=username).first()
        if not user or not pwd_context.verify(password, user.password_hash):
            return None
        return user