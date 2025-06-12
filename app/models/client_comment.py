from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class ClientComment(Base):
    __tablename__ = "clients_comments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False, index=True)  # FK a Client.id (después puedes agregar FK real si quieres)
    comment_text = Column(String, nullable=False)
    created_by = Column(String, nullable=False, default="system")  # lo dejamos preparado para login real después
    created_at = Column(DateTime(timezone=True), server_default=func.now())
