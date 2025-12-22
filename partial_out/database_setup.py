import sqlite3

def setup_database():
    """Creates and populates the SQLite database with sample product data."""
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        # Create table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            barcode TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            weight_grams INTEGER NOT NULL
        )
        ''')

        # Sample data
        products = [
            ('8901030723829', 'Good Day Cashew Cookies 200g', 45.00, 200),
            ('8901719124022', 'Lays Classic Salted Chips 52g', 20.00, 52),
            ('8901207038986', 'Amul Gold Milk 1L', 68.00, 1000),
            ('8901030729784', 'Britannia Bourbon Biscuits 150g', 30.00, 150),
            ('4902430713781', 'Gillette Mach3 Razor', 150.00, 75),
            ('8901491102016', 'Tata Salt 1kg', 25.00, 1000),
            ('8901030752454', 'Parle-G Gold Biscuits 1kg', 120.00, 1000),
            ('7506206822187', 'Coca-Cola Can 300ml', 40.00, 330),
            ('8906002012011', 'Maggi 2-Minute Noodles 70g', 12.00, 70),
            ('8901526101509', 'Colgate MaxFresh Toothpaste 150g', 95.00, 150)
        ]

        # Insert data, ignore if barcode already exists
        cursor.executemany("INSERT OR IGNORE INTO products (barcode, name, price, weight_grams) VALUES (?,?,?,?)", products)

        conn.commit()
        print("Database 'products.db' created and populated successfully.")
        print(f"{len(products)} sample products added.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    setup_database()
