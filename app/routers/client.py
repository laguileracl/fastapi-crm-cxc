from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import pandas as pd

from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
import app.crud.client as crud_client
from app.database import get_db
from app.users import current_active_user
from app.models.user import User
from app.utils.rut import validar_rut_chileno  # <--- Nuevo import

import logging

logger = logging.getLogger("crm_logger")
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/clients", tags=["clients"])

# ... otros endpoints arriba si los tienes ...

@router.post("/upload-excel")
def upload_clients_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(current_active_user)
):
    df = pd.read_excel(file.file)
    df.columns = df.columns.str.strip()

    required_columns = {
        'Código SN', 'Nombre cliente', 'VAT Code', 'Linea de Crédito',
        'Account Balance', 'Ejecutivo Cuenta', 'Nombre Corto', 'Segmento',
        'Payment Terms Code', 'Nacional / Extranjero', 'Negocios en Proceso',
        'Guías Despacho No Facturadas', 'Nivel de Riesgo', 'Fecha Informe Riesgo',
        'Teléfono 2', 'Teléfono 1', 'Móvil', 'E-Mail', 'Contacto', 'Active',
        'Tipo socio negocio'
    }
    if not required_columns.issubset(set(df.columns)):
        raise HTTPException(status_code=400, detail=f"Excel must contain columns: {required_columns}")

    processed_clients = 0
    for idx, row in df.iterrows():
        card_code = str(row['Código SN']).strip()
        if not card_code:
            continue

        client_type = row.get('Tipo socio negocio', '').strip()
        rut = str(row['VAT Code']).strip()

        # Validar RUT chileno SOLO para nacionales
        if client_type.lower() == 'nacional':
            if not validar_rut_chileno(rut):
                raise HTTPException(
                    status_code=400,
                    detail=f"Fila {idx+2}: El RUT '{rut}' de {row['Nombre cliente']} no es válido para un cliente nacional."
                )

        client_data = {
            "card_code": card_code,
            "name": row['Nombre cliente'],
            "rut": rut,
            "credit_line_amount": row.get('Linea de Crédito', 0),
            "current_outstanding_balance": row.get('Account Balance', 0),
            "account_manager": row.get('Ejecutivo Cuenta', ''),
            "alias_name": row.get('Nombre Corto', ''),
            "client_segment": row.get('Segmento', ''),
            "payment_terms_days": row.get('Payment Terms Code', 0),
            "client_group": row.get('Nacional / Extranjero', ''),
            "open_orders_balance": row.get('Negocios en Proceso', 0),
            "open_deliveries_balance": row.get('Guías Despacho No Facturadas', 0),
            "sanction_tool_risk_level": row.get('Nivel de Riesgo', ''),
            "sanction_tool_date": str(row.get('Fecha Informe Riesgo', '')),
            "telephone_2": row.get('Teléfono 2', ''),
            "telephone_1": row.get('Teléfono 1', ''),
            "mobile_phone": row.get('Móvil', ''),
            "email": row.get('E-Mail', ''),
            "contact_person": row.get('Contacto', ''),
            "is_active": True if str(row.get('Active', '')).strip().lower() == 'yes' else False,
            "client_type": client_type
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
