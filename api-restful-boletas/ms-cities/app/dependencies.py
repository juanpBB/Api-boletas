from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_admin_role(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifica si el usuario tiene rol de administrador
    """
    token = credentials.credentials
    
    if token != "admin-token-secreto":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requiere el rol de Administrador."
        )
    return True

def get_db_connection():
    """
    Proporciona conexión a la base de datos de cities
    """
    import sqlite3
    conn = sqlite3.connect("cities.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()