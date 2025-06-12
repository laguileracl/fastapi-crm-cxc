from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.client_comment import ClientCommentCreate, ClientCommentResponse
from app.models.client_comment import ClientComment
from app.models.client import Client
from app.database import get_db
from app.users import current_active_user
from app.models.user import User

import logging

logger = logging.getLogger("crm_logger")
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/client-comments", tags=["client-comments"])

# GET comentarios de un cliente → sin protección (abierto)
@router.get("/{client_id}", response_model=List[ClientCommentResponse])
def read_client_comments(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    comments = db.query(ClientComment).filter(ClientComment.client_id == client_id).order_by(ClientComment.created_at.desc()).all()
    return comments

# POST agregar comentario → protegido con JWT
@router.post("/", response_model=ClientCommentResponse, status_code=status.HTTP_201_CREATED)
def create_client_comment(
    comment_create: ClientCommentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(current_active_user)
):
    db_client = db.query(Client).filter(Client.id == comment_create.client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    db_comment = ClientComment(
        client_id=comment_create.client_id,
        comment_text=comment_create.comment_text,
        created_by=user.email  # siempre registrar el email del user autenticado
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    logger.info(f"[USER {user.email}] Added comment for Client ID {comment_create.client_id}: {comment_create.comment_text}")

    return db_comment

# DELETE comentario → protegido con JWT
@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(current_active_user)
):
    db_comment = db.query(ClientComment).filter(ClientComment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    db.delete(db_comment)
    db.commit()

    logger.info(f"[USER {user.email}] Deleted comment ID {comment_id}")
