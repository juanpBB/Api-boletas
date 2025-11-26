from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from ..models import CategoryCreate, CategoryResponse
from ..dependencies import get_admin_role, get_db_connection
from ..database import (
    get_categories, get_category_by_id, create_category, 
    update_category, delete_category
)

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category_endpoint(
    category: CategoryCreate,
    conn: sqlite3.Connection = Depends(get_db_connection),
    is_admin: bool = Depends(get_admin_role)
):
    """
    Crea una nueva categoría de evento
    """
    try:
        category_id = create_category(
            conn, 
            category.name, 
            category.description, 
            category.is_active
        )
        return {
            "message": "Categoría creada exitosamente", 
            "id": category_id
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=list[CategoryResponse])
def get_categories_endpoint(conn: sqlite3.Connection = Depends(get_db_connection)):
    """
    Recupera todas las categorías activas
    """
    return get_categories(conn)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_endpoint(
    category_id: int, 
    conn: sqlite3.Connection = Depends(get_db_connection)
):
    """
    Obtiene una categoría específica
    """
    category = get_category_by_id(conn, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    return category

@router.put("/{category_id}")
def update_category_endpoint(
    category_id: int,
    category: CategoryCreate,
    conn: sqlite3.Connection = Depends(get_db_connection),
    is_admin: bool = Depends(get_admin_role)
):
    """
    Actualiza una categoría existente
    """
    if not update_category(
        conn, 
        category_id, 
        category.name, 
        category.description, 
        category.is_active
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    return {"message": "Categoría actualizada exitosamente"}

@router.delete("/{category_id}")  # ✅ REMOVER status_code=204
def delete_category_endpoint(
    category_id: int,
    conn: sqlite3.Connection = Depends(get_db_connection),
    is_admin: bool = Depends(get_admin_role)
):
    """
    Elimina categoría existente
    """
    if not delete_category(conn, category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    # ✅ SOLUCIÓN: Devolver mensaje de confirmación
    return {
        "message": "Categoría eliminada exitosamente",
        "id": category_id
    }