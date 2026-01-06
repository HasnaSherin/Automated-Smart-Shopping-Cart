
import sqlite3

def create_inventory_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT UNIQUE NOT NULL,
        product_name TEXT NOT NULL,
        mrp REAL NOT NULL,
        discount REAL NOT NULL,
        tax_rate REAL NOT NULL,
        quantity_value REAL NOT NULL,
        quantity_unit TEXT NOT NULL,
        stock_quantity INTEGER NOT NULL,
        reorder_level INTEGER NOT NULL
    )
    """)

    products = [
        ('8901057512345', 'Aashirvaad Atta', 350, 5, 5, 5, 'kg', 60, 15),
        ('8901725187654', 'Sunflower Oil', 180, 3, 5, 1, 'L', 45, 10),
        ('8901302009876', 'Nescafe Coffee', 290, 8, 12, 100, 'g', 35, 8),
        ('8901491198765', 'Dettol Liquid', 85, 4, 12, 250, 'ml', 70, 15),
        ('8906003012345', 'Himalaya Soap', 45, 0, 5, 75, 'g', 120, 25),
        ('8901719101122', 'Bru Coffee', 240, 6, 12, 200, 'g', 40, 10),
        ('8901526709988', 'Dove Soap', 55, 2, 5, 100, 'g', 95, 20),
        ('7501031312345', 'Sprite Bottle', 45, 0, 12, 500, 'ml', 85, 20),
        ('8901725198760', 'Kissan Jam', 140, 5, 12, 500, 'g', 50, 12),
        ('8906003098765', 'Pears Soap', 60, 3, 5, 125, 'g', 65, 15)
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO products
    (barcode, product_name, mrp, discount, tax_rate,
     quantity_value, quantity_unit, stock_quantity, reorder_level)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products)

    conn.commit()
    conn.close()
    print("✅ Inventory database created and data inserted")

if __name__ == "__main__":
    create_inventory_db()
