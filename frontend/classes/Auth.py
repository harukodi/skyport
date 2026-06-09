from nicegui import ui, app
import bcrypt
import hmac
from os import environ

class Auth:
    _username: str = ""
    _password_hash: bytes = b""

    @classmethod
    def init(cls) -> None:
        try:
            username = environ.pop("SKYPORT_USERNAME")
            password = environ.pop("SKYPORT_PASSWORD")
        except KeyError:
            raise RuntimeError("USERNAME OR PASSWORD ENV IS NOT SET!")
        
        if len(password) < 16:
            raise ValueError("Password must be at least 5 characters long")
        
        cls._username = username
        cls._password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        del password
    

    @staticmethod
    def is_authenticated() -> bool:
        return app.storage.user.get("authenticated", False)

    @staticmethod
    def require_auth(redirect_to: str = "/") -> bool:
        if not Auth.is_authenticated():
            ui.navigate.to(redirect_to)
            return False
        return True

    @staticmethod
    def redirect_if_authenticated(redirect_to: str = "/dashboard") -> bool:
        if Auth.is_authenticated():
            ui.navigate.to(redirect_to)
            return True
        return False

    @staticmethod
    def login(redirect_to: str = "/dashboard") -> None:
        app.storage.user["authenticated"] = True
        ui.navigate.to(redirect_to)

    @staticmethod
    def logout(redirect_to: str = "/") -> None:
        app.storage.user["authenticated"] = False
        ui.navigate.to(redirect_to)

    @staticmethod
    def verify_login(username: str, password: str) -> bool:
        username_match = hmac.compare_digest(username, Auth._username)
        if not username_match:
            return False
        return bcrypt.checkpw(password.encode(), Auth._password_hash)