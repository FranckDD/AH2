from repositories.user_repo import UserRepository

class AuthController:
    def __init__(self):
        self.user_repo = UserRepository()
        self.current_user = None

    def authenticate(self, username: str, password: str):
        user = self.user_repo.get_user_by_username(username)
        if user and user.check_password(password) and user.is_active:
            self.current_user = user
            return user
        return None