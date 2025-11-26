import sqlite3

def init_database():
    """
    Inicializa la base de datos con la tabla cities
    """
    conn = sqlite3.connect("cities.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            country TEXT DEFAULT 'Colombia',
            timezone TEXT DEFAULT 'America/Bogota',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertar datos de ejemplo
    cursor.execute('''
        INSERT OR IGNORE INTO cities (name, country, timezone) 
        VALUES 
        ('Bogotá', 'Colombia', 'America/Bogota'),
        ('Medellín', 'Colombia', 'America/Bogota'),
        ('Cali', 'Colombia', 'America/Bogota')
    ''')
    
    conn.commit()
    conn.close()

def get_cities(conn):
    """Obtiene todas las ciudades activas"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cities WHERE is_active = TRUE')
    return [dict(row) for row in cursor.fetchall()]

def get_city_by_id(conn, city_id):
    """Obtiene una ciudad por ID"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cities WHERE id = ?', (city_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

def create_city(conn, name, country, timezone, is_active):
    """Crea una nueva ciudad"""
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO cities (name, country, timezone, is_active) VALUES (?, ?, ?, ?)',
            (name, country, timezone, is_active)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("Ya existe una ciudad con ese nombre")

def update_city(conn, city_id, name, country, timezone, is_active):
    """Actualiza una ciudad existente"""
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE cities SET name = ?, country = ?, timezone = ?, is_active = ? WHERE id = ?',
        (name, country, timezone, is_active, city_id)
    )
    conn.commit()
    return cursor.rowcount > 0

def delete_city(conn, city_id):
    """Elimina una ciudad"""
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cities WHERE id = ?', (city_id,))
    conn.commit()
    return cursor.rowcount > 0