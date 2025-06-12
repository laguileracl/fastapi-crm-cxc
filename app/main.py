from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.database import engine, Base
from app.routers import client

# Inicializa FastAPI
app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye el router de la API REST (clients)
app.include_router(client.router)

# Crea las tablas en la BD al iniciar
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Endpoint raíz
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI CRM application!"}

# Configura Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Endpoint para la UI → NO choca con /clients/{id}
@app.get("/clients-ui", response_class=HTMLResponse)
async def clients_ui(request: Request):
    return templates.TemplateResponse("clients.html", {"request": request})
