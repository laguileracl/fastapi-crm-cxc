from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd

from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
import app.crud.client as crud_client
from app.database import get_db
from app.users import current_active_user
from app.models.user import User

import logging

logger = logging.getLogger("crm_logger")
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/clients", tags=["clients"])

# GET listado clientes → sin protección (abierto)
@router.get("/", response_model=List[ClientResponse])
def read_clients(skip: int = 0, limit: int = 100, all: bool = False, db: Session = Depends(get_db)):
    return crud_client.get_clients(db, skip=skip, limit=limit, include_inactive=all)

# GET cliente por id → sin protección (abierto)
@router.get("/{id}", response_model=ClientResponse)
def read_client(id: int, db: Session = Depends(get_db)):
    db_client = crud_client.get_client(db, id=id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

# POST crear cliente → protegido con JWT
@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    user: User = Depends(current_active_user)
):
    db_client = crud_client.get_client_by_card_code(db, card_code=client.card_code)
    if db_client:
        raise HTTPException(status_code=400, detail="CardCode already registered")
    
    new_client = crud_client.create_client(db, client)

    logger.info(f"[USER {user.email}] Created new Client ID {new_client.id} with CardCode {new_client.card_code} and Name '{new_client.name}'")

    return new_client

# PUT actualizar cliente → puedes dejar abierto o proteger si quieres (aquí lo dejo abierto como ejemplo)
@router.put("/{id}", response_model=ClientResponse)
def update_client(id: int, client_update: ClientUpdate, db: Session = Depends(get_db)):
    db_client = crud_client.get_client(db, id=id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return crud_client.update_client(db, db_client, client_update)

# DELETE cliente (soft delete) → protegido con JWT
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(current_active_user)
):
    db_client = crud_client.get_client(db, id=id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    crud_client.delete_client(db, db_client)

    logger.info(f"[USER {user.email}] Soft deleted Client ID {db_client.id} (CardCode {db_client.card_code})")

# POST upload Excel → protegido con JWT
@router.post("/upload-excel")
def upload_clients_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(current_active_user)
):
    df = pd.read_excel(file.file)
    df.columns = df.columns.str.strip()

    required_columns = {
        'Código SN', 'Nombre de socio de negocios', 'RUT', 'Linea de Credito',
        'Account Balance', 'Sales Employee Code', 'Alias Name', 'SEGMENTO',
        'Payment Terms Code', 'Group Code', 'Open Orders Balance',
        'Open Deliveries/GRPO Balance', 'Sanction Tool Risk Level',
        'SanctionTool DATE', 'Telephone 2', 'Telephone 1', 'Mobile Phone',
        'E-Mail', 'Contact Person', 'Active'
    }

    if not required_columns.issubset(set(df.columns)):
        raise HTTPException(status_code=400, detail=f"Excel must contain columns: {required_columns}")

    processed_clients = 0
    for _, row in df.iterrows():
        card_code = str(row['Código SN']).strip()

        if not card_code.startswith("C"):
            continue

        client_data = {
            "card_code": card_code,
            "name": row['Nombre de socio de negocios'],
            "rut": str(row['RUT']).strip(),
            "credit_line_amount": row.get('Linea de Credito', 0),
            "current_outstanding_balance": row.get('Account Balance', 0),
            "account_manager": row.get('Sales Employee Code', ''),
            "alias_name": row.get('Alias Name', ''),
            "client_segment": row.get('SEGMENTO', ''),
            "payment_terms_days": row.get('Payment Terms Code', 0),
            "client_group": row.get('Group Code', ''),
            "open_orders_balance": row.get('Open Orders Balance', 0),
            "open_deliveries_balance": row.get('Open Deliveries/GRPO Balance', 0),
            "sanction_tool_risk_level": row.get('Sanction Tool Risk Level', ''),
            "sanction_tool_date": str(row.get('SanctionTool DATE', '')),
            "telephone_2": row.get('Telephone 2', ''),
            "telephone_1": row.get('Telephone 1', ''),
            "mobile_phone": row.get('Mobile Phone', ''),
            "email": row.get('E-Mail', ''),
            "contact_person": row.get('Contact Person', ''),
            "is_active": True if str(row.get('Active', '')).strip().lower() == 'yes' else False
        }

        existing_client = crud_client.get_client_by_card_code(db, card_code=card_code)

        if existing_client:
            update_schema = ClientUpdate(**client_data)
            crud_client.update_client(db, existing_client, update_schema)
        else:
            create_schema = ClientCreate(**client_data)
            crud_client.create_client(db, create_schema)

        processed_clients += 1

    logger.info(f"[USER {user.email}] Upload Excel processed {processed_clients} clients")

    return {"detail": f"{processed_clients} clients processed successfully"}
