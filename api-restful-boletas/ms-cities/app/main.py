from fastapi import FastAPI
from .routers import cities
from .database import init_database

app = FastAPI(
    title="API RESTFul Boletas - Cities Microservice",
    description="Microservicio para gestión de ciudades",
    version="1.0.0"
)

# Incluir routers
app.include_router(cities.router)

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
    return {"message": "Bienvenido al Microservicio de Ciudades"}

@app.get("/health")
def health_check():
    """
    Endpoint para verificar el estado del servicio
    """
    return {"status": "healthy", "service": "cities"}