from sqlalchemy import Column, String, DateTime, func
from app.database import Base

class AdminLog(Base):
    __tablename__ = "admin_logs"

    id = Column(String, primary_key=True)
    action = Column(String, nullable=False)
    performed_by = Column(String, nullable=False)
    target_user_id = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
