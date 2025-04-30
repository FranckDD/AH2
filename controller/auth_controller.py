from repositories.user_repo import UserRepository
from models.user import pwd_context  # Import du contexte de cryptage centralisé

class AuthController:
    def __init__(self):
        self.user_repo = UserRepository()
        self.current_user = None

    def authenticate(self, username: str, password: str):
        try:
            user = self.user_repo.get_user_by_username(username)
            if not user:
                print(f"Utilisateur {username} non trouvé")
                return None
                
            if not user.is_active:
                print(f"Compte {username} désactivé")
                return None
                
            # Vérification directe avec pwd_context pour un meilleur contrôle
            if not pwd_context.verify(password, user.password_hash):
                print(f"Échec de vérification du mot de passe pour {username}")
                return None
                
            self.current_user = user
            return user
            
        except Exception as e:
            print(f"Erreur d'authentification pour {username}: {str(e)}")
            # Loguer l'erreur complète pour le débogage
            import traceback
            traceback.print_exc()
            return None