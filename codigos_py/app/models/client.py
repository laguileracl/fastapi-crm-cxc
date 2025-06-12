from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func
from app.database import Base
from sqlalchemy.orm import validates

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    card_code = Column(String, unique=True, nullable=False, index=True)  # Código SN
    name = Column(String, nullable=False)                                # Nombre cliente
    rut = Column(String, unique=True, nullable=False, index=True)        # RUT
    credit_line_amount = Column(Float)                                   # Monto línea crédito otorgada
    current_outstanding_balance = Column(Float)                          # Account Balance
    account_manager = Column(String)                                     # Ejecutivo cuentas (RSM)
    alias_name = Column(String)                                          # Nombre corto empresa
    client_segment = Column(String)                                      # Segmento
    payment_terms_days = Column(Integer)                                 # Plazo de pago en días
    client_group = Column(String)                                        # Nacional / Extranjero
    open_orders_balance = Column(Float)                                  # Negocios en proceso
    open_deliveries_balance = Column(Float)                              # Guías de despacho no facturadas
    sanction_tool_risk_level = Column(String)                            # Nivel de riesgo Sanction Tool
    sanction_tool_date = Column(String)                                  # Fecha análisis Sanction Tool (como string, luego puedes parsear a date)
    telephone_2 = Column(String)                                         # Teléfono 2
    telephone_1 = Column(String)                                         # Teléfono 1
    mobile_phone = Column(String)                                        # Móvil
    email = Column(String)                                               # Email
    contact_person = Column(String)                                      # Contacto
    is_active = Column(Boolean, default=True)                            # Activo / No activo (por columna "Active")
    credit_line_available = Column(Float)                                # Calculado: credit_line_amount - sum(account_balance + open_orders + open_deliveries)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @validates("email")
    def validate_email(self, key, address):
        if address and "@" not in address:
            raise ValueError("Invalid email address")
        return address
