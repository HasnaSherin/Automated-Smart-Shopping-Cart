import sqlite3
import random

barcodes = [
    '8901057512345',
    '8901725187654',
    '8901302009876',
    '8901491198765',
    '8906003012345'
]

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

total_bill = 0

while True:
    barcode = random.choice(barcodes)
    print("\n📦 Scanned Barcode:", barcode)

    cursor.execute("""
    SELECT product_name, mrp, discount, tax_rate,
           quantity_value, quantity_unit,
           stock_quantity, reorder_level
    FROM products WHERE barcode = ?
    """, (barcode,))

    product = cursor.fetchone()

    if product:
        name, price, discount, tax, qty, unit, stock, reorder = product

        discount_amt = price * discount / 100
        price_after_discount = price - discount_amt
        tax_amt = price_after_discount * tax / 100
        final_price = price_after_discount + tax_amt

        print("Product :", name)
        print("Quantity:", qty, unit)
        print("MRP     : ₹", price)
        print("Final   : ₹", round(final_price, 2))

        total_bill += final_price

        cursor.execute("""
        UPDATE products
        SET stock_quantity = stock_quantity - 1
        WHERE barcode = ?
        """, (barcode,))
        conn.commit()

        if stock - 1 <= reorder:
            print("⚠ LOW STOCK - Reorder needed")

    else:
        print("❌ Product not found")

    choice = input("\nAdd another product? (yes/no): ").lower()
    if choice != "yes":
        break

conn.close()

print("\n💰 TOTAL AMOUNT: ₹", round(total_bill, 2))
print("🙏 Thank you for shopping")
