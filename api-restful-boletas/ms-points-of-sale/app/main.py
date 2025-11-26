from fastapi import FastAPI
from .routers import points_of_sale
from .database import init_database

app = FastAPI(
    title="API RESTFul Boletas - Points of Sale Microservice",
    description="Microservicio para gestión de puntos de venta",
    version="1.0.0"
)

# Incluir routers
app.include_router(points_of_sale.router)

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
    return {"message": "Bienvenido al Microservicio de Puntos de Venta"}

@app.get("/health")
def health_check():
    """
    Endpoint para verificar el estado del servicio
    """
    return {"status": "healthy", "service": "points-of-sale"}