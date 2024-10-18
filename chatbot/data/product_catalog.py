import sqlite3
import os

# Get the path to the database file
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'product_database.db')

products = {
    "apparel": [
        {"id": "A001", "name": "Classic T-Shirt", "price": 19.99, "categories": ["tops", "casual"]},
        {"id": "A002", "name": "Slim Fit Jeans", "price": 49.99, "categories": ["bottoms", "casual"]},
        {"id": "A003", "name": "Summer Dress", "price": 39.99, "categories": ["dresses", "summer"]},
    ],
    "home_accessories": [
        {"id": "H001", "name": "Decorative Pillow", "price": 24.99, "categories": ["living room", "bedroom"]},
        {"id": "H002", "name": "Table Lamp", "price": 34.99, "categories": ["lighting", "living room"]},
        {"id": "H003", "name": "Wall Clock", "price": 29.99, "categories": ["decor", "kitchen"]},
    ],
}

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        price REAL,
        description TEXT,
        image_url TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_product(id, name, price, categories, description='', image_url=''):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?)",
              (id, name, price, description, image_url))
    c.execute("DELETE FROM product_categories WHERE product_id=?", (id,))
    for category in categories:
        if category:
            c.execute("INSERT INTO product_categories VALUES (?, ?)", (id, category))
    conn.commit()
    conn.close()

def get_product_by_id(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return dict(product) if product else None

def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products

def search_products(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM products 
        WHERE id LIKE ? OR name LIKE ? OR description LIKE ?
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products

def get_products_by_category(category):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id LIKE ?", (f"{category.upper()}%",))
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products
