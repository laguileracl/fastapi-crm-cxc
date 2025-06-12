# 📊 FastAPI CRM CXC (Cuentas por Cobrar)

Proyecto en desarrollo: **Sistema CRM + ERP** para la gestión de cuentas por cobrar de clientes.

---

## 🚀 Objetivo

Construir un sistema interno tipo *ERP / CRM* con:

👉 Gestión de clientes
👉 Importación inteligente de planilla de *Master de Clientes* (controlada por SAP)
👉 Visualización de cartera de clientes en forma dinámica
👉 Gestión de comentarios históricos por cliente
👉 Control de líneas de crédito, riesgos y pagos
👉 Preparado para extender a integración con **facturas**, **pagos**, **gestión de cobranzas**

---

## 🗂️ Estructura actual del proyecto

```
/app
    /models          # Definición ORM (Client, ClientComment)
    /schemas         # Schemas Pydantic
    /crud            # Operaciones CRUD (Client, ClientComment)
    /routers         # Rutas API REST
    /templates       # Frontend simple (clients.html)
    /static          # Archivos estáticos (CSS/JS futuros)
    main.py          # Configuración principal de FastAPI
    database.py      # Configuración de DB (sqlite por ahora)
/docs
    CLIENT_MASTER_DATABASE.md    # Documentación base de datos clientes
    PROJECT_LOGIC.md             # Lógica de negocio del proyecto
    VSCode_SETUP.md              # Configuración recomendada para VSCode
README.md                        # Este documento
.gitignore                       # Exclusión de carpetas temporales
```

---

## 🛠️ Stack Tecnológico

- ⚡ FastAPI
- 🗄️ SQLAlchemy + SQLite
- 🔡 Bootstrap + DataTables (en frontend simple)
- Python 3.13
- 🖋️ VSCode + OhMyZSH + iTerm2 (entorno recomendado)

---

## ⚙️ Features actuales

👉 CRUD completo de clientes
👉 Importación incremental de planilla `BusinessPartners.xlsx`
👉 Control de *clientes activos / inactivos*
👉 Cálculo automático de línea de crédito disponible
👉 Sistema de comentarios histórico con autor + timestamp
👉 API REST moderna (listo para futura integración a frontend más avanzado)

---

## ✈️ Roadmap

🔺 Optimizar carga incremental de planilla (parsing optimizado)
🔺 Mejorar interfaz de comentarios (mostrar timeline bonito)
🔺 Agregar módulo Facturas
🔺 Agregar módulo Pagos
🔺 Reportes de cartera / aging de cuentas
🔺 Autenticación y control de permisos (login con RSM, Admin, etc.)
🔺 Exportación de reportes en Excel / PDF
🔺 Despliegue en servidor interno (dockerización)

---

## 🚧 En desarrollo

Este proyecto es parte de una iniciativa interna para modernizar la gestión de cuentas por cobrar en la empresa.

---

## 📝 Notas adicionales

La estructura de la planilla `BusinessPartners.xlsx` y su lógica están documentadas en:

- [docs/CLIENT\_MASTER\_DATABASE.md](docs/CLIENT_MASTER_DATABASE.md)
- [docs/PROJECT\_LOGIC.md](docs/PROJECT_LOGIC.md)

👉 **Si vas a colaborar en el proyecto, lee esos documentos primero.**

---

## 🤝 Autor

Luis A. - 2025
Proyecto privado / uso interno

---
