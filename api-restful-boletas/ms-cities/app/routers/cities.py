from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3

# Importaciones relativas CORREGIDAS
from ..models import CityCreate, CityResponse
from ..dependencies import get_admin_role, get_db_connection
from ..database import (
    get_cities, get_city_by_id, create_city, 
    update_city, delete_city
)

router = APIRouter(prefix="/api/v1/cities", tags=["cities"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_city_endpoint(
    city: CityCreate,
    conn: sqlite3.Connection = Depends(get_db_connection),
    is_admin: bool = Depends(get_admin_role)
):
    """
    Crea una nueva ciudad
    """
    try:
        city_id = create_city(
            conn, 
            city.name, 
            city.country, 
            city.timezone, 
            city.is_active
        )
        return {
            "message": "Ciudad creada exitosamente", 
            "id": city_id
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=list[CityResponse])
def get_cities_endpoint(conn: sqlite3.Connection = Depends(get_db_connection)):
    """
    Recupera todas las ciudades activas
    """
    cities = get_cities(conn)
    return cities

@router.get("/{city_id}", response_model=CityResponse)
def get_city_endpoint(
    city_id: int, 
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    """
    Obtiene una ciudad específica
    """
    city = get_city_by_id(conn, city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada"
        )
    return city

@router.put("/{city_id}")
def update_city_endpoint(
    city_id: int,
    city: CityCreate,
    conn: sqlite3.Connection = Depends(get_db_connection),
    is_admin: bool = Depends(get_admin_role)
):
    """
    Actualiza una ciudad existente
    """
    if not update_city(
        conn, 
        city_id, 
        city.name, 
        city.country, 
        city.timezone, 
        city.is_active
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada"
        )
    return {"message": "Ciudad actualizada exitosamente"}

@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city_endpoint(
    city_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection),
    is_admin: bool = Depends(get_admin_role)
):
    """
    Elimina ciudad existente
    """
    if not delete_city(conn, city_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada"
        )