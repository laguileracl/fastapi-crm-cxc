# app/users.py

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.manager import BaseUserManager
from fastapi_users.password import PasswordHelper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi import Depends

from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.database import get_db
from sqlalchemy.orm import Session

SECRET = "SUPERSECRET"  # cambia esto en producción

# Transport + JWT strategy
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Password helper
password_helper = PasswordHelper()

# User DB dependency
def get_user_db(db: Session = Depends(get_db)):
    yield SQLAlchemyUserDatabase(User, db)

# User Manager
class UserManager(BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request=None):
        print(f"User {user.id} has registered.")

# FastAPI Users instance
fastapi_users = FastAPIUsers[User, int](
    get_user_manager=lambda: UserManager(next(get_user_db())),  # Ojo: next() para obtener el yield
    auth_backends=[auth_backend],
)

# Current active user dependency
current_active_user = fastapi_users.current_user(active=True)
