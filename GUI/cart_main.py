import tkinter as tk
from tkinter import ttk, messagebox, font
import sqlite3
import cv2
from pyzbar.pyzbar import decode

# --- Configuration & Theme ---
THEME = {
    "bg": "#101622",           # Dark Background
    "card": "#151a25",         # Card/Panel Background
    "primary": "#135bec",      # Blue
    "primary_hover": "#2563eb",# Lighter Blue
    "white": "#ffffff",
    "gray": "#92a4c9",
    "success": "#10b981",      # Green for checkout
    "danger": "#ef4444"        # Red for errors
}

class SmartCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Shopping Cart")
        self.root.geometry("1024x600")
        self.root.configure(bg=THEME["bg"])
        self.root.minsize(800, 500)

        self.cart_items = {}
        self.total = 0.0
        self.tax_rate = 0.05  # 5% tax

        # Fonts definition (matching the previous theme)
        self.fonts = {
            "header": font.Font(family="Helvetica", size=24, weight="bold"),
            "sub": font.Font(family="Helvetica", size=14),
            "table": font.Font(family="Arial", size=11),
            "total": font.Font(family="Arial", size=16, weight="bold")
        }

        # Layout configuration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._configure_styles()
        self._create_widgets()
        self._update_totals()
        self.update_status("System Ready. Scan item to begin.")
        self._toggle_cart_view()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam') # 'clam' allows for better color customization

        # General App Style
        style.configure('TFrame', background=THEME["bg"])
        style.configure('TLabel', background=THEME["bg"], foreground=THEME["white"])
        
        # Card/Panel Style (for Treeview and Totals)
        style.configure('Card.TFrame', background=THEME["card"], relief='flat')
        
        # Treeview (The List)
        style.configure('Treeview', 
                        background=THEME["card"], 
                        fieldbackground=THEME["card"], 
                        foreground=THEME["white"],
                        font=self.fonts["table"],
                        borderwidth=0,
                        rowheight=35)
        
        style.configure('Treeview.Heading', 
                        background=THEME["bg"], 
                        foreground=THEME["gray"], 
                        font=("Helvetica", 10, "bold"),
                        borderwidth=1)
        
        style.map('Treeview', background=[('selected', THEME["primary"])])

        # Buttons (Customizing ttk buttons to look like the custom frames)
        # Base Button
        style.configure('TButton', 
                        font=("Helvetica", 11, "bold"), 
                        padding=12, 
                        borderwidth=0, 
                        background=THEME["card"], 
                        foreground=THEME["gray"])
        
        style.map('TButton', 
                  background=[('active', THEME["primary"]), ('pressed', THEME["primary_hover"])],
                  foreground=[('active', THEME["white"])])

        # Accent Button (Blue - Scan)
        style.configure('Accent.TButton', 
                        background=THEME["primary"], 
                        foreground=THEME["white"])
        
        style.map('Accent.TButton', background=[('active', THEME["primary_hover"])])

        # Success Button (Green - Checkout)
        style.configure('Success.TButton', 
                        background=THEME["success"], 
                        foreground=THEME["white"])
        
        # Danger Button (Red - Remove)
        style.configure('Danger.TButton', 
                        background=THEME["danger"], 
                        foreground=THEME["white"])

        # Totals Panel
        style.configure('Totals.TFrame', background=THEME["card"])
        style.configure('Totals.TLabel', background=THEME["card"], foreground=THEME["gray"], font=self.fonts["sub"])
        style.configure('GrandTotal.TLabel', background=THEME["card"], foreground=THEME["primary"], font=self.fonts["total"])

        # Scrollbar
        style.configure("Vertical.TScrollbar", gripcount=0, background=THEME["card"], troughcolor=THEME["bg"], borderwidth=0, arrowsize=15)

    def _create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # --- Header ---
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))

        header_label = ttk.Label(header_frame, text="SMART CART DASHBOARD", font=self.fonts["header"], foreground=THEME["white"])
        header_label.pack(side=tk.LEFT)

        # --- Cart items display ---
        self.cart_frame = ttk.Frame(main_frame, style='Card.TFrame')
        self.cart_frame.grid(row=1, column=0, sticky="nsew")
        self.cart_frame.columnconfigure(0, weight=1)
        self.cart_frame.rowconfigure(0, weight=1)

        # Treeview
        columns = ("name", "quantity", "price", "total")
        self.tree = ttk.Treeview(self.cart_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("name", text="PRODUCT NAME")
        self.tree.heading("quantity", text="QTY")
        self.tree.heading("price", text="UNIT PRICE")
        self.tree.heading("total", text="TOTAL")

        self.tree.column("name", width=300)
        self.tree.column("quantity", anchor=tk.CENTER, width=80)
        self.tree.column("price", anchor=tk.E, width=120)
        self.tree.column("total", anchor=tk.E, width=120)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.cart_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Empty Cart Message ---
        self.empty_cart_label = ttk.Label(main_frame, text="CART IS EMPTY", font=("Helvetica", 18), foreground=THEME["gray"], anchor="center")
        
        # --- Totals Display ---
        totals_frame = ttk.Frame(main_frame, padding=20, style='Totals.TFrame')
        totals_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        totals_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.subtotal_label = ttk.Label(totals_frame, text="Subtotal: ₹0.00", style='Totals.TLabel')
        self.subtotal_label.grid(row=0, column=0, sticky="w")
        
        self.tax_label = ttk.Label(totals_frame, text="Tax (5%): ₹0.00", style='Totals.TLabel')
        self.tax_label.grid(row=0, column=1, sticky="w")
        
        self.total_label = ttk.Label(totals_frame, text="Total: ₹0.00", style='GrandTotal.TLabel')
        self.total_label.grid(row=0, column=3, sticky="e")

        # --- Buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky="ew", pady=30)
        button_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.scan_camera_button = ttk.Button(button_frame, text="📷 SCAN ITEM", command=self.scan_with_camera, style='Accent.TButton')
        self.scan_camera_button.grid(row=0, column=0, padx=10, ipady=5, sticky="ew")
        
        self.scan_button = ttk.Button(button_frame, text="🎲 SIMULATE", command=self.simulate_scan)
        self.scan_button.grid(row=0, column=1, padx=10, ipady=5, sticky="ew")

        self.remove_button = ttk.Button(button_frame, text="🗑 REMOVE", command=self.remove_item, style='Danger.TButton')
        self.remove_button.grid(row=0, column=2, padx=10, ipady=5, sticky="ew")

        self.checkout_button = ttk.Button(button_frame, text="✔ CHECKOUT", command=self.checkout, style='Success.TButton')
        self.checkout_button.grid(row=0, column=3, padx=10, ipady=5, sticky="ew")

        # --- Status Bar ---
        self.status_bar = ttk.Label(self.root, text="Welcome", relief=tk.FLAT, anchor=tk.W, padding=10, font=("Arial", 10), background=THEME["primary"], foreground=THEME["white"])
        self.status_bar.grid(row=1, column=0, sticky="ew")

    def scan_with_camera(self):
        self.update_status("Opening camera... Please show a barcode.")
        cap = cv2.VideoCapture(0) # Standard index is 0, changed from 1 for general compatibility
        
        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Could not open webcam.")
            self.update_status("Failed to open camera.", "error")
            return

        found_barcode = False
        while not found_barcode:
            success, img = cap.read()
            if not success:
                continue

            for barcode in decode(img):
                barcode_data = barcode.data.decode('utf-8')
                self.update_status(f"Barcode found: {barcode_data}")
                
                # Look up product in DB
                try:
                    conn = sqlite3.connect('products.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT name, price FROM products WHERE barcode=?", (barcode_data,))
                    product = cursor.fetchone()
                    conn.close()

                    if product:
                        name, price = product
                        self.add_item(barcode_data, name, price)
                        self.update_status(f"Added: {name}")
                    else:
                        self.update_status(f"Barcode {barcode_data} not found in database.", "error")
                    
                    found_barcode = True
                    break # Exit inner loop
                except sqlite3.Error as e:
                    self.update_status(f"Database error: {e}", "error")

            cv2.imshow('Barcode Scanner', img)
            if cv2.waitKey(1) & 0xFF == ord('q') or \
                cv2.getWindowProperty('Barcode Scanner', cv2.WND_PROP_VISIBLE) < 1:
                break
        
        cap.release()
        cv2.destroyAllWindows()
        if not found_barcode:
            self.update_status("Camera closed. No item scanned.")

    def simulate_scan(self):
        """Simulates scanning a random item from the database."""
        try:
            conn = sqlite3.connect('products.db')
            cursor = conn.cursor()
            cursor.execute("SELECT barcode, name, price FROM products ORDER BY RANDOM() LIMIT 1")
            product = cursor.fetchone()
            conn.close()

            if product:
                barcode, name, price = product
                self.add_item(barcode, name, price)
                self.update_status(f"Scanned: {name}")
            else:
                self.update_status("Database is empty. No item to scan.", "error")
        except sqlite3.Error as e:
            self.update_status(f"Database error: {e}", "error")
            # Create a mock DB if it doesn't exist for testing purposes
            self.create_mock_db()

    def create_mock_db(self):
        # Helper to create a dummy DB if user runs this without one
        try:
            conn = sqlite3.connect('products.db')
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS products (barcode TEXT, name TEXT, price REAL)")
            cursor.execute("INSERT INTO products VALUES ('12345', 'Dark Energy Drink', 150.00)")
            cursor.execute("INSERT INTO products VALUES ('67890', 'Neural Interface', 2500.00)")
            cursor.execute("INSERT INTO products VALUES ('11223', 'Quantum Chip', 500.00)")
            conn.commit()
            conn.close()
            self.update_status("Created mock database. Try scanning again.")
        except Exception as e:
            print(e)

    def add_item(self, barcode, name, price):
        """Adds or updates an item in the cart."""
        if barcode in self.cart_items:
            self.cart_items[barcode]['quantity'] += 1
        else:
            self.cart_items[barcode] = {'name': name, 'price': price, 'quantity': 1}
        self._update_cart_display()

    def remove_item(self):
        """Removes the selected item from the cart."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an item to remove.")
            return

        item_id = selected_item[0]
        item_name = self.tree.item(item_id, 'values')[0]
        barcode_to_remove = None
        for barcode, details in self.cart_items.items():
            if details['name'] == item_name:
                barcode_to_remove = barcode
                break

        if barcode_to_remove:
            if self.cart_items[barcode_to_remove]['quantity'] > 1:
                 self.cart_items[barcode_to_remove]['quantity'] -= 1
            else:
                del self.cart_items[barcode_to_remove]
            self.update_status(f"Removed one unit of {item_name}.")
        self._update_cart_display()

    def _update_cart_display(self):
        """Refreshes the items list in the UI."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for barcode, details in self.cart_items.items():
            name = details['name']
            quantity = details['quantity']
            price = details['price']
            total_price = price * quantity
            self.tree.insert("", tk.END, values=(name, quantity, f"₹{price:.2f}", f"₹{total_price:.2f}"))

        self._update_totals()
        self._toggle_cart_view()

    def _toggle_cart_view(self):
        """Shows or hides the empty cart message."""
        if not self.cart_items:
            self.empty_cart_label.grid(row=1, column=0, sticky="nsew")
            self.cart_frame.grid_remove()
        else:
            self.empty_cart_label.grid_remove()
            self.cart_frame.grid()

    def _update_totals(self):
        """Calculates and updates subtotal, tax, and total."""
        self.subtotal = sum(item['price'] * item['quantity'] for item in self.cart_items.values())
        self.tax = self.subtotal * self.tax_rate
        self.total = self.subtotal + self.tax

        self.subtotal_label.config(text=f"SUBTOTAL: ₹{self.subtotal:.2f}")
        self.tax_label.config(text=f"TAX (5%): ₹{self.tax:.2f}")
        self.total_label.config(text=f"TOTAL: ₹{self.total:.2f}")

    def checkout(self):
        """Handles the checkout process."""
        if not self.cart_items:
            messagebox.showinfo("Empty Cart", "Your cart is empty. Please scan items to checkout.")
            return

        checkout_message = f"Your total bill is ₹{self.total:.2f}.\n\nThank you for shopping with us!"
        messagebox.showinfo("Checkout Successful", checkout_message)
        self.update_status("Checkout complete! Thank you.", "success")
        self.cart_items.clear()
        self._update_cart_display()

    def update_status(self, message, level="info"):
        self.status_bar.config(text=f"  {message}")
        if level == "error":
            self.status_bar.config(background=THEME["danger"], foreground="white")
        elif level == "success":
            self.status_bar.config(background=THEME["success"], foreground="white")
        else:
            self.status_bar.config(background=THEME["primary"], foreground="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCartApp(root)
    root.mainloop()