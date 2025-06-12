import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from app.database import get_user_db
from app.models.user import User

# Secret para JWT (debería estar en un archivo .env para producción)
SECRET = "SECRET_KEY"

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} registered.")

# Dependency para FastAPI Users
def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

# Autenticación JWT
bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

# Dependency para usuario activo actual
current_active_user = fastapi_users.current_user(active=True)

# Dependency para superuser activo actual (esto es lo que faltaba)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
