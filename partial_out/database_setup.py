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

def setup_users_database():
    try:
        # Connect to SQLite database (creates file if not exists)
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username VARCHAR(512),
            last_time_spend VARCHAR(512),
            avg_time VARCHAR(512),
            last_spend VARCHAR(512),
            avg_spend VARCHAR(512),
            last_purchase VARCHAR(512),
            total_purchase VARCHAR(512),
            created_at VARCHAR(512)
        )
        """)

        # Insert sample users
        users_data = [
            (
                1234567890, "Test User", "", "", "", "", "", "0",
                "2025-12-23 19:21:06.361401+00"
            ),
            (
                8848385318, "Abhijith", "", "", "", "", "", "0",
                "2025-12-18 19:30:09.192856+00"
            ),
            (
                8891114832, "hasna", "", "", "", "", "", "0",
                "2025-12-22 11:03:16.264095+00"
            )
        ]

        cursor.executemany("""
        INSERT OR IGNORE INTO users
        (id, username, last_time_spend, avg_time, last_spend, avg_spend,
         last_purchase, total_purchase, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, users_data)

        conn.commit()
        print("✅ users.db created and populated successfully")

    except sqlite3.Error as e:
        print("❌ Database error:", e)

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    setup_database()
    setup_users_database()
