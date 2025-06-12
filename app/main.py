import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.database import init_models
from app.routers import client
from app.routers import users
from app.routers import admin

from app.users import fastapi_users, auth_backend
from app.schemas.user import UserRead, UserCreate, UserUpdate

# Crear instancia de la aplicación
app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de autenticación
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Rutas de cliente
app.include_router(client.router)
app.include_router(users.router)
app.include_router(admin.router)


# Evento asíncrono para inicializar tablas
@app.on_event("startup")
async def on_startup():
    await init_models()

# Ruta principal
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI CRM application!"}

# Configuración para Jinja2
templates = Jinja2Templates(directory="app/templates")

@app.get("/clients-ui", response_class=HTMLResponse)
async def clients_ui(request: Request):
    return templates.TemplateResponse("clients.html", {"request": request})
