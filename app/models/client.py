from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func, UniqueConstraint
from app.database import Base
from sqlalchemy.orm import validates
import re

def validar_rut_chileno(rut):
    rut = rut.upper().replace("-", "").replace(".", "")
    if not re.match(r"^\d{7,8}[0-9K]$", rut):
        return False
    cuerpo = rut[:-1]
    dv = rut[-1]
    suma = 0
    multiplo = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = 9 if multiplo == 2 else multiplo - 1
    dv_calc = 11 - (suma % 11)
    dv_calc = "K" if dv_calc == 10 else "0" if dv_calc == 11 else str(dv_calc)
    return dv == dv_calc

class Client(Base):
    __tablename__ = "clients"
    __table_args__ = (
        UniqueConstraint("rut", name="uq_clients_rut"),
        UniqueConstraint("email", name="uq_clients_email"),
        UniqueConstraint("card_code", name="uq_clients_card_code"),
    )

    id = Column(Integer, primary_key=True, index=True)
    card_code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    rut = Column(String, unique=True, nullable=False, index=True)
    credit_line_amount = Column(Float)
    current_outstanding_balance = Column(Float)
    account_manager = Column(String)
    alias_name = Column(String)
    client_segment = Column(String)
    payment_terms_days = Column(Integer)
    client_group = Column(String)
    open_orders_balance = Column(Float)
    open_deliveries_balance = Column(Float)
    sanction_tool_risk_level = Column(String)
    sanction_tool_date = Column(String)
    telephone_2 = Column(String)
    telephone_1 = Column(String)
    mobile_phone = Column(String)
    email = Column(String, unique=True, index=True)
    contact_person = Column(String)
    is_active = Column(Boolean, default=True)
    client_type = Column(String)  # Nuevo: mapea 'Tipo socio negocio'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @property
    def credit_line_available(self):
        return (self.credit_line_amount or 0) - (
            (self.current_outstanding_balance or 0)
            + (self.open_orders_balance or 0)
            + (self.open_deliveries_balance or 0)
        )

    @validates("email")
    def validate_email(self, key, address):
        if address and "@" not in address:
            raise ValueError("Invalid email address")
        return address

    @validates("rut")
    def validate_rut(self, key, rut):
        tipo = (self.client_type or "").strip().lower()
        if tipo == "nacional" and rut:
            if not validar_rut_chileno(rut):
                raise ValueError("RUT chileno inválido para cliente nacional")
        return rut
