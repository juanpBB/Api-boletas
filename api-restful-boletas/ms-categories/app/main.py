from fastapi import FastAPI
from .routers import categories
from .database import init_database

app = FastAPI(
    title="API RESTFul Boletas - Categories Microservice",
    description="Microservicio para gestión de categorías de eventos",
    version="1.0.0"
)

# Incluir routers
app.include_router(categories.router)

@app.on_event("startup")
def on_startup():
    """
    Evento que se ejecuta al iniciar la aplicación
    """
    init_database()

@app.get("/")
def read_root():
    """
    Endpoint de bienvenida
    """
    return {"message": "Bienvenido al Microservicio de Categorías"}

@app.get("/health")
def health_check():
    """
    Endpoint para verificar el estado del servicio
    """
    return {"status": "healthy", "service": "categories"}