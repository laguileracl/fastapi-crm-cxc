from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.users import current_active_superuser

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/")
async def list_users(db: AsyncSession = Depends(get_db), superuser: User = Depends(current_active_superuser)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
