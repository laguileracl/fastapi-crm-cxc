from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.users import current_active_superuser
from app.models.admin_log import AdminLog
import uuid as uuid_lib

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

# Promote user to superuser
@router.post("/promote_user/{user_id}")
async def promote_user(user_id: str, db: AsyncSession = Depends(get_db), superuser: User = Depends(current_active_superuser)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_superuser = True
    db.add(user)
    await db.commit()

    # Audit log
    log = AdminLog(
        id=str(uuid_lib.uuid4()),
        action="Promote User",
        performed_by=superuser.email,
        target_user_id=user.id
    )
    db.add(log)
    await db.commit()

    return {"detail": f"User {user.email} promoted to superuser."}

# Delete user
@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db), superuser: User = Depends(current_active_superuser)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    # Audit log
    log = AdminLog(
        id=str(uuid_lib.uuid4()),
        action="Delete User",
        performed_by=superuser.email,
        target_user_id=user.id
    )
    db.add(log)
    await db.commit()

    return {"detail": f"User {user.email} deleted."}

# Downgrade user (remove superuser)
@router.patch("/downgrade_user/{user_id}")
async def downgrade_user(user_id: str, db: AsyncSession = Depends(get_db), superuser: User = Depends(current_active_superuser)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_superuser = False
    db.add(user)
    await db.commit()

    # Audit log
    log = AdminLog(
        id=str(uuid_lib.uuid4()),
        action="Downgrade User",
        performed_by=superuser.email,
        target_user_id=user.id
    )
    db.add(log)
    await db.commit()

    return {"detail": f"User {user.email} downgraded to regular user."}

# Get user details by ID
@router.get("/get_user/{user_id}")
async def get_user(user_id: str, db: AsyncSession = Depends(get_db), superuser: User = Depends(current_active_superuser)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "is_verified": user.is_verified
    }

# List all users with pagination
@router.get("/list_users")
async def list_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), superuser: User = Depends(current_active_superuser)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()

    return [{
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "is_verified": user.is_verified
    } for user in users]

# List admin logs
@router.get("/list_admin_logs")
async def list_admin_logs(db: AsyncSession = Depends(get_db), superuser: User = Depends(current_active_superuser)):
    result = await db.execute(select(AdminLog).order_by(AdminLog.timestamp.desc()))
    logs = result.scalars().all()

    return [{
        "id": log.id,
        "action": log.action,
        "performed_by": log.performed_by,
        "target_user_id": log.target_user_id,
        "timestamp": log.timestamp.isoformat()
    } for log in logs]