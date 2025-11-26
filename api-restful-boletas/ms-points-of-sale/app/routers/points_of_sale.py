from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from ..models import PointOfSaleCreate, PointOfSaleResponse
from ..dependencies import get_admin_role, get_db_connection
from ..database import (
    get_points_of_sale, get_point_of_sale_by_id, create_point_of_sale, 
    update_point_of_sale, delete_point_of_sale
)

router = APIRouter(prefix="/api/v1/points-of-sale", tags=["points-of-sale"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_point_of_sale_endpoint(
    point_of_sale: PointOfSaleCreate,
    conn: sqlite3.Connection = Depends(get_db_connection),
    is_admin: bool = Depends(get_admin_role)
):
    """
    Crea un nuevo punto de venta
    """
    try:
        pos_id = create_point_of_sale(
            conn, 
            point_of_sale.name, 
            point_of_sale.address, 
            point_of_sale.city_id, 
            point_of_sale.phone, 
            point_of_sale.is_active
        )
        return {
            "message": "Punto de venta creado exitosamente", 
            "id": pos_id
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=list[PointOfSaleResponse])
def get_points_of_sale_endpoint(conn: sqlite3.Connection = Depends(get_db_connection)):
    """
    Recupera todos los puntos de venta activos
    """
    return get_points_of_sale(conn)

@router.get("/{pos_id}", response_model=PointOfSaleResponse)
def get_point_of_sale_endpoint(
    pos_id: int, 
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    """
    Obtiene un punto de venta específico
    """
    point_of_sale = get_point_of_sale_by_id(conn, pos_id)
    if not point_of_sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de venta no encontrado"
        )
    return point_of_sale

@router.put("/{pos_id}")
def update_point_of_sale_endpoint(
    pos_id: int,
    point_of_sale: PointOfSaleCreate,
    conn: sqlite3.Connection = Depends(get_db_connection),
    is_admin: bool = Depends(get_admin_role)
):
    """
    Actualiza un punto de venta existente
    """
    if not update_point_of_sale(
        conn, 
        pos_id, 
        point_of_sale.name, 
        point_of_sale.address, 
        point_of_sale.city_id, 
        point_of_sale.phone, 
        point_of_sale.is_active
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de venta no encontrado"
        )
    return {"message": "Punto de venta actualizado exitosamente"}

@router.delete("/{pos_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_point_of_sale_endpoint(
    pos_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection),
    is_admin: bool = Depends(get_admin_role)
):
    """
    Elimina punto de venta existente
    """
    if not delete_point_of_sale(conn, pos_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de venta no encontrado"
        )