# CLIENT MASTER DATABASE

## Objetivo

Este documento describe la estructura y lógica del **Maestro de Clientes** en el sistema CRM CxC.

La base de datos de clientes se mantiene sincronizada con la planilla **BusinessPartners.xlsx** proveniente del ERP.  
El sistema permite carga incremental e inteligente, evitando reescritura completa.

---

## Tabla: `clients`

| Campo en DB | Fuente en Excel | Descripción | Cálculo / Observación |
|-------------|-----------------|-------------|----------------------|
| `card_code` | Código SN | Código único del cliente |
| `name` | Nombre cliente | Nombre completo del cliente |
| `rut` | VAT Code | RUT chileno o VAT internacional |
| `credit_line_amount` | Linea de Crédito | Monto autorizado de línea de crédito |
| `current_outstanding_balance` | Account Balance | Saldo actual pendiente de pago |
| `account_manager` | Ejecutivo Cuenta | Ejecutivo asignado (RSM) |
| `alias_name` | Nombre Corto | Nombre corto o comercial |
| `client_segment` | Segmento | Segmento de negocio |
| `payment_terms_days` | Payment Terms Code | Plazo de pago en días |
| `client_group` | Nacional / Extranjero | Grupo del cliente |
| `open_orders_balance` | Negocios en Proceso | Monto de pedidos en proceso |
| `open_deliveries_balance` | Guías Despacho No Facturadas | Monto de guías no facturadas |
| `sanction_tool_risk_level` | Nivel de Riesgo | Nivel de riesgo según Sanction Tool |
| `sanction_tool_date` | Fecha Informe Riesgo | Fecha de análisis |
| `telephone_2` | Teléfono 2 | Teléfono alternativo |
| `telephone_1` | Teléfono 1 | Teléfono principal |
| `mobile_phone` | Móvil | Número de celular |
| `email` | E-Mail | Email de contacto |
| `contact_person` | Contacto | Nombre del contacto financiero |
| `is_active` | Active | Estado del cliente (Yes / No) |
| `credit_line_available` | Calculado | credit_line_amount - (Account Balance + Negocios en Proceso + Guías No Facturadas) |

---

## Lógica de actualización

- Los clientes cuyo `card_code` comienza con `C` son considerados válidos.
- Al importar Excel:
  - Se actualizan los registros cuyo `card_code` ya existe.
  - Se agregan nuevos clientes si no existen.
  - Los campos que cambian se actualizan individualmente.
- Si `Active = No`, el cliente queda marcado como `is_active = False`, pero no se elimina.

---

## Comentarios asociados

Los comentarios de gestión quedan asociados a cada cliente:

Tabla `client_comments`:
- `id`
- `client_id` → FK a `clients.id`
- `text`
- `created_by` (para futura integración con login)
- `created_at`

---

## Futuras extensiones

✅ Agregar control de versión de histórico de clientes eliminados o inactivos  
✅ Dashboard de cartera / indicadores  
✅ Visualización detallada de facturas y pagos  
✅ Buscador avanzado con filtros customizables  
✅ Permitir exportar en Excel la base completa o parcial  
