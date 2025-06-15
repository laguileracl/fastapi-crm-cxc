from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate

def get_clients(db: Session, skip: int = 0, limit: int = 100, include_inactive: bool = False):
    query = select(Client)
    if not include_inactive:
        query = query.where(Client.is_active == True)
    result = db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

def get_client(db: Session, id: int):
    result = db.execute(select(Client).where(Client.id == id))
    return result.scalars().first()

def get_client_by_card_code(db: Session, card_code: str):
    result = db.execute(select(Client).where(Client.card_code == card_code))
    return result.scalars().first()

def create_client(db: Session, client: ClientCreate):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, db_client: Client, client_update: ClientUpdate):
    update_data = client_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, db_client: Client):
    db_client.is_active = False
    db.add(db_client)
    db.commit()
