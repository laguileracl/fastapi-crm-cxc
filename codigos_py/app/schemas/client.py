from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ClientBase(BaseModel):
    card_code: str  # Código SN
    name: str
    rut: str
    credit_line_amount: Optional[float] = 0.0
    current_outstanding_balance: Optional[float] = 0.0
    account_manager: Optional[str] = None
    alias_name: Optional[str] = None
    client_segment: Optional[str] = None
    payment_terms_days: Optional[int] = None
    client_group: Optional[str] = None
    open_orders_balance: Optional[float] = 0.0
    open_deliveries_balance: Optional[float] = 0.0
    sanction_tool_risk_level: Optional[str] = None
    sanction_tool_date: Optional[str] = None  # lo puedes luego convertir a date
    telephone_2: Optional[str] = None
    telephone_1: Optional[str] = None
    mobile_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    contact_person: Optional[str] = None
    is_active: Optional[bool] = True

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    rut: Optional[str] = None
    credit_line_amount: Optional[float] = None
    current_outstanding_balance: Optional[float] = None
    account_manager: Optional[str] = None
    alias_name: Optional[str] = None
    client_segment: Optional[str] = None
    payment_terms_days: Optional[int] = None
    client_group: Optional[str] = None
    open_orders_balance: Optional[float] = None
    open_deliveries_balance: Optional[float] = None
    sanction_tool_risk_level: Optional[str] = None
    sanction_tool_date: Optional[str] = None
    telephone_2: Optional[str] = None
    telephone_1: Optional[str] = None
    mobile_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    contact_person: Optional[str] = None
    is_active: Optional[bool] = None

class ClientResponse(ClientBase):
    id: int
    credit_line_available: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # reemplazo de orm_mode en Pydantic v2
