from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate

# Helper para calcular credit_line_available
def calculate_credit_line_available(client_data: dict) -> float:
    credit_line_amount = client_data.get("credit_line_amount", 0.0) or 0.0
    account_balance = client_data.get("current_outstanding_balance", 0.0) or 0.0
    open_orders_balance = client_data.get("open_orders_balance", 0.0) or 0.0
    open_deliveries_balance = client_data.get("open_deliveries_balance", 0.0) or 0.0
    used_credit = account_balance + open_orders_balance + open_deliveries_balance
    available_credit = credit_line_amount - used_credit
    return max(available_credit, 0.0)  # nunca negativo

# Get cliente por id
def get_client(db: Session, id: int):
    return db.query(Client).filter(Client.id == id).first()

# Get cliente por código SN
def get_client_by_card_code(db: Session, card_code: str):
    return db.query(Client).filter(Client.card_code == card_code).first()

# Get cliente por RUT
def get_client_by_RUT(db: Session, RUT: str):
    return db.query(Client).filter(Client.rut == RUT).first()

# Get listado clientes
def get_clients(db: Session, skip: int = 0, limit: int = 100, include_inactive: bool = False):
    query = db.query(Client)
    if not include_inactive:
        query = query.filter(Client.is_active == True)
    return query.offset(skip).limit(limit).all()

# Crear cliente
def create_client(db: Session, client_create: ClientCreate):
    client_data = client_create.dict()
    client_data["credit_line_available"] = calculate_credit_line_available(client_data)

    db_client = Client(**client_data)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Update cliente (update inteligente)
def update_client(db: Session, db_client: Client, client_update: ClientUpdate):
    update_data = client_update.dict(exclude_unset=True)

    # recalculamos credit_line_available si alguno de estos campos cambia:
    credit_related_fields = [
        "credit_line_amount",
        "current_outstanding_balance",
        "open_orders_balance",
        "open_deliveries_balance"
    ]

    needs_credit_recalc = any(field in update_data for field in credit_related_fields)

    for key, value in update_data.items():
        setattr(db_client, key, value)

    if needs_credit_recalc:
        # recalculamos con el estado actual del objeto
        client_data = {
            "credit_line_amount": db_client.credit_line_amount,
            "current_outstanding_balance": db_client.current_outstanding_balance,
            "open_orders_balance": db_client.open_orders_balance,
            "open_deliveries_balance": db_client.open_deliveries_balance
        }
        db_client.credit_line_available = calculate_credit_line_available(client_data)

    db.commit()
    db.refresh(db_client)
    return db_client

# Eliminar cliente (soft delete → marcar is_active = False)
def delete_client(db: Session, db_client: Client):
    db_client.is_active = False
    db.commit()
    db.refresh(db_client)
    return db_client
