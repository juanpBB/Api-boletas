import sqlite3

def init_database():
    """
    Inicializa la base de datos con la tabla categories
    """
    conn = sqlite3.connect("categories.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertar datos de ejemplo
    cursor.execute('''
        INSERT OR IGNORE INTO categories (name, description) 
        VALUES 
        ('Conciertos', 'Eventos musicales en vivo'),
        ('Teatro', 'Obras teatrales y espectáculos'),
        ('Deportes', 'Eventos deportivos')
    ''')
    
    conn.commit()
    conn.close()

def get_categories(conn):
    """Obtiene todas las categorías activas"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories WHERE is_active = TRUE')
    return [dict(row) for row in cursor.fetchall()]

def get_category_by_id(conn, category_id):
    """Obtiene una categoría por ID"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

def create_category(conn, name, description, is_active):
    """Crea una nueva categoría"""
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO categories (name, description, is_active) VALUES (?, ?, ?)',
            (name, description, is_active)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("Ya existe una categoría con ese nombre")

def update_category(conn, category_id, name, description, is_active):
    """Actualiza una categoría existente"""
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE categories SET name = ?, description = ?, is_active = ? WHERE id = ?',
        (name, description, is_active, category_id)
    )
    conn.commit()
    return cursor.rowcount > 0

def delete_category(conn, category_id):
    """Elimina una categoría"""
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    return cursor.rowcount > 0