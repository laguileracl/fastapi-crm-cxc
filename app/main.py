from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.database import Base, engine
from app.routers import client

from app.users import fastapi_users, current_active_user, auth_backend
from app.models.user import User
from app.schemas.user import UserRead, UserCreate

# Crea la app FastAPI
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers de auth
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

# Router de clients
app.include_router(client.router)

# Crear tablas al iniciar
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Endpoint raíz
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI CRM application!"}

# Configuración Jinja2
templates = Jinja2Templates(directory="app/templates")

# Endpoint para la UI
@app.get("/clients-ui", response_class=HTMLResponse)
async def clients_ui(request: Request):
    return templates.TemplateResponse("clients.html", {"request": request})
