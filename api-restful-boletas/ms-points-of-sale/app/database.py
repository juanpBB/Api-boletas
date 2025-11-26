import sqlite3

def init_database():
    """
    Inicializa la base de datos con la tabla points_of_sale
    """
    conn = sqlite3.connect("points_of_sale.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS points_of_sale (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            city_id INTEGER NOT NULL,
            phone TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertar datos de ejemplo
    cursor.execute('''
        INSERT OR IGNORE INTO points_of_sale (name, address, city_id, phone) 
        VALUES 
        ('Centro Comercial Andino', 'Cra 11 #82-71', 1, '+57 1234567'),
        ('Plaza Central', 'Av. Caracas #24-55', 1, '+57 7654321'),
        ('Mall Plaza Medellín', 'Cl 30 #45-67', 2, '+57 9876543')
    ''')
    
    conn.commit()
    conn.close()

def get_points_of_sale(conn):
    """Obtiene todos los puntos de venta activos"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM points_of_sale WHERE is_active = TRUE')
    return [dict(row) for row in cursor.fetchall()]

def get_point_of_sale_by_id(conn, pos_id):
    """Obtiene un punto de venta por ID"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM points_of_sale WHERE id = ?', (pos_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

def create_point_of_sale(conn, name, address, city_id, phone, is_active):
    """Crea un nuevo punto de venta"""
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO points_of_sale (name, address, city_id, phone, is_active) VALUES (?, ?, ?, ?, ?)',
            (name, address, city_id, phone, is_active)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("Error al crear el punto de venta")

def update_point_of_sale(conn, pos_id, name, address, city_id, phone, is_active):
    """Actualiza un punto de venta existente"""
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE points_of_sale SET name = ?, address = ?, city_id = ?, phone = ?, is_active = ? WHERE id = ?',
        (name, address, city_id, phone, is_active, pos_id)
    )
    conn.commit()
    return cursor.rowcount > 0

def delete_point_of_sale(conn, pos_id):
    """Elimina un punto de venta"""
    cursor = conn.cursor()
    cursor.execute('DELETE FROM points_of_sale WHERE id = ?', (pos_id,))
    conn.commit()
    return cursor.rowcount > 0