from sqlalchemy.orm import Session, joinedload  # Ajoutez joinedload
from sqlalchemy import text
from models.user import User
from models.database import DatabaseManager

class UserRepository:
    def __init__(self):
        self.db = DatabaseManager("postgresql://postgres:Admin_2025@localhost/AH2")
        self.session = self.db.get_session()

    def get_user_by_username(self, username: str):
        try:
            user = self.session.query(User)\
                .options(joinedload(User.role))\
                .filter(User.username == username)\
                .first()
            
            if not user:
                print(f"Aucun utilisateur trouvé avec le username: {username}")
            return user
            
        except Exception as e:
            print(f"ERREUR lors de la récupération de l'utilisateur: {str(e)}")
            raise

    def get_user_permissions(self, role_id: int):
        query = text(
            "SELECT p.permission_name FROM role_permissions rp "
            "JOIN permissions p ON rp.permission_id = p.permission_id "
            "WHERE rp.role_id = :role_id"
        )
        return self.session.execute(query, {'role_id': role_id}).scalars().all()