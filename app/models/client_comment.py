from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.database import Base

class ClientComment(Base):
    __tablename__ = "clients_comments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    comment_text = Column(String, nullable=False)
    created_by = Column(String, nullable=False, default="system")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
