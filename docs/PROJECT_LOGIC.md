# PROJECT LOGIC - CRM CxC

## Objetivo del sistema

Construir un **mini ERP / CRM** para la gestión de clientes con foco en:

✅ Control de línea de crédito
✅ Seguimiento de cartera y riesgo
✅ Historial de contactos / gestiones
✅ Visualización fácil de toda la información por cliente
✅ Capacidad de cargar planillas actualizadas
✅ Agregar / editar / eliminar clientes manualmente
✅ Mantener base siempre limpia y actualizada

---

## Módulos actuales

- **Clients**:

  - Vista de tabla con DataTables
  - CRUD de clientes manual
  - Carga de Excel de BusinessPartners
  - Sincronización incremental
  - Control de crédito disponible
  - Estado de actividad
- **Client Comments**:

  - Comentarios por cliente
  - Trazabilidad con `created_by` y fecha
  - Eliminación segura

---

## Flujo de uso esperado

1️⃣ Usuario carga la planilla de clientes actualizada
2️⃣ El sistema revisa cambios, actualiza lo necesario
3️⃣ Los usuarios pueden buscar clientes, filtrar, exportar
4️⃣ Los RSM pueden agregar comentarios por cliente
5️⃣ Los analistas pueden visualizar cartera, riesgo, límites

---

## Futuras integraciones

✅ Dashboard resumen
✅ Panel de KPIs financieros
✅ Integración con sistema de facturación
✅ Gestión documental (contratos, certificados)
✅ Control de cambios en línea de crédito
✅ Workflow de aprobación de excepciones

---

## Arquitectura técnica

- **Backend**: FastAPI + SQLAlchemy + SQLite (para prototipo)
- **Frontend**: HTML + Bootstrap + DataTables + Vanilla JS
- **ORM**: SQLAlchemy
- **Base datos**: SQLite (migrable a Postgres en futuro)

---

## Setup recomendado

- iTerm2 + Zsh + Starship → desarrollo ágil
- VSCode + JetBrainsMono Nerd Font
- Plugins útiles: Python, Pylance, Black, isort, GitLens, DataTables extension

---

Este documento sirve como base para explicar la lógica de negocio y el roadmap del proyecto.
