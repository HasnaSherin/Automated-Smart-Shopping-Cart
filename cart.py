import tkinter as tk
from tkinter import ttk, messagebox, font
import cv2
from pyzbar.pyzbar import decode
import sqlite3

# --- Theme Constants ---
THEME = {
    "bg": "#101622", "card": "#151a25", "primary": "#135bec",
    "primary_hover": "#2563eb", "white": "#ffffff", "gray": "#92a4c9",
    "success": "#10b981", "danger": "#ef4444"
}

class SmartCartApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=THEME["bg"])
        
        self.cart_items = {}
        self.total = 0.0
        self.tax_rate = 0.05

        self.fonts = {
            "header": font.Font(family="Helvetica", size=24, weight="bold"),
            "sub": font.Font(family="Helvetica", size=14),
            "table": font.Font(family="Arial", size=11),
            "total": font.Font(family="Arial", size=16, weight="bold")
        }

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._configure_styles()
        self._create_widgets()
        self._update_totals()
        self._toggle_cart_view()

    def on_show(self):
        """Called when this screen appears"""
        self.status_bar.config(text="System Ready. Scan item to begin.")
        # Optional: Clear cart if coming from a fresh start
        # self.cart_items = {}
        # self._update_cart_display()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=THEME["bg"])
        style.configure('TLabel', background=THEME["bg"], foreground=THEME["white"])
        style.configure('Card.TFrame', background=THEME["card"], relief='flat')
        style.configure('Treeview', background=THEME["card"], fieldbackground=THEME["card"], foreground=THEME["white"], font=self.fonts["table"], rowheight=35, borderwidth=0)
        style.configure('Treeview.Heading', background=THEME["bg"], foreground=THEME["gray"], font=("Helvetica", 10, "bold"))
        style.map('Treeview', background=[('selected', THEME["primary"])])
        
        # Buttons
        style.configure('TButton', font=("Helvetica", 11, "bold"), padding=10, borderwidth=0, background=THEME["card"], foreground=THEME["gray"])
        style.map('TButton', background=[('active', THEME["primary"]), ('pressed', THEME["primary_hover"])], foreground=[('active', THEME["white"])])
        
        style.configure('Accent.TButton', background=THEME["primary"], foreground=THEME["white"])
        style.map('Accent.TButton', background=[('active', THEME["primary_hover"])])
        style.configure('Success.TButton', background=THEME["success"], foreground=THEME["white"])
        style.configure('Danger.TButton', background=THEME["danger"], foreground=THEME["white"])
        
        style.configure('Totals.TFrame', background=THEME["card"])
        style.configure('Totals.TLabel', background=THEME["card"], foreground=THEME["gray"], font=self.fonts["sub"])
        style.configure('GrandTotal.TLabel', background=THEME["card"], foreground=THEME["primary"], font=self.fonts["total"])

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="30")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Header
        ttk.Label(main_frame, text="SMART CART DASHBOARD", font=self.fonts["header"]).grid(row=0, column=0, sticky="w", pady=(0, 25))

        # Cart List
        self.cart_frame = ttk.Frame(main_frame, style='Card.TFrame')
        self.cart_frame.grid(row=1, column=0, sticky="nsew")
        self.cart_frame.columnconfigure(0, weight=1)
        self.cart_frame.rowconfigure(0, weight=1)

        columns = ("name", "quantity", "price", "total")
        self.tree = ttk.Treeview(self.cart_frame, columns=columns, show="headings", height=12)
        self.tree.heading("name", text="PRODUCT NAME")
        self.tree.heading("quantity", text="QTY")
        self.tree.heading("price", text="UNIT PRICE")
        self.tree.heading("total", text="TOTAL")
        self.tree.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # Empty State
        self.empty_cart_label = ttk.Label(main_frame, text="CART IS EMPTY", font=("Helvetica", 18), foreground=THEME["gray"], anchor="center")

        # Totals
        totals_frame = ttk.Frame(main_frame, padding=20, style='Totals.TFrame')
        totals_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        totals_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.subtotal_label = ttk.Label(totals_frame, text="Subtotal: ₹0.00", style='Totals.TLabel')
        self.subtotal_label.grid(row=0, column=0, sticky="w")
        self.tax_label = ttk.Label(totals_frame, text="Tax (5%): ₹0.00", style='Totals.TLabel')
        self.tax_label.grid(row=0, column=1, sticky="w")
        self.total_label = ttk.Label(totals_frame, text="Total: ₹0.00", style='GrandTotal.TLabel')
        self.total_label.grid(row=0, column=3, sticky="e")

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, sticky="ew", pady=30)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)

        ttk.Button(btn_frame, text="📷 SCAN", command=self.scan_with_camera, style='Accent.TButton').grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(btn_frame, text="🎲 SIMULATE", command=self.simulate_scan).grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(btn_frame, text="🗑 REMOVE", command=self.remove_item, style='Danger.TButton').grid(row=0, column=2, padx=5, sticky="ew")
        ttk.Button(btn_frame, text="✔ CHECKOUT", command=self.checkout, style='Success.TButton').grid(row=0, column=3, padx=5, sticky="ew")

        # Status Bar
        self.status_bar = ttk.Label(self, text="Welcome", padding=10, background=THEME["primary"], foreground=THEME["white"])
        self.status_bar.grid(row=1, column=0, sticky="ew")
        

    #Scan with Camera
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
        
        
    # Simulate Scan from Database
    def simulate_scan(self):
        """Simulates scanning a random item from the database."""
        try:
            conn = sqlite3.connect('cart_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT barcode, product_name, mrp FROM products ORDER BY RANDOM() LIMIT 1")
            product = cursor.fetchone()
            conn.close()

            if product:
                barcode, product_name, price = product
                self.add_item(barcode, product_name, price)
                self.update_status(f"Scanned: {product_name}")
            else:
                self.update_status("Database is empty. No item to scan.", "error")
        except sqlite3.Error as e:
            self.update_status(f"Database error: {e}", "error")
            # Create a mock DB if it doesn't exist for testing purposes
            messagebox.showinfo("Info", "Error accessing database.")
            # self.create_mock_db()


    def add_item_from_db(self, barcode):
        # In a real app, query SQLite here
        # For now, we simulate a DB hit
        self.add_item(barcode, f"Item-{barcode}", 100.0)

    def add_item(self, barcode, name, price):
        if barcode in self.cart_items:
            self.cart_items[barcode]['quantity'] += 1
        else:
            self.cart_items[barcode] = {'name': name, 'price': price, 'quantity': 1}
        self._update_cart_display()
        self.status_bar.config(text=f"Added: {name}")

    def remove_item(self):
        selected = self.tree.selection()
        if not selected: return
        item_name = self.tree.item(selected[0], 'values')[0]
        
        # Find barcode by name (inefficient but works for small lists)
        target_code = next((code for code, det in self.cart_items.items() if det['name'] == item_name), None)
        if target_code:
            if self.cart_items[target_code]['quantity'] > 1:
                self.cart_items[target_code]['quantity'] -= 1
            else:
                del self.cart_items[target_code]
        self._update_cart_display()

    def _update_cart_display(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for code, item in self.cart_items.items():
            total = item['price'] * item['quantity']
            self.tree.insert("", "end", values=(item['name'], item['quantity'], f"₹{item['price']}", f"₹{total}"))
        self._update_totals()
        self._toggle_cart_view()

    def _toggle_cart_view(self):
        if not self.cart_items:
            self.empty_cart_label.grid(row=1, column=0, sticky="nsew")
            self.cart_frame.grid_remove()
        else:
            self.empty_cart_label.grid_remove()
            self.cart_frame.grid()

    def _update_totals(self):
        self.subtotal = sum(i['price'] * i['quantity'] for i in self.cart_items.values())
        self.tax = self.subtotal * self.tax_rate
        self.total = self.subtotal + self.tax
        self.subtotal_label.config(text=f"SUBTOTAL: ₹{self.subtotal:.2f}")
        self.tax_label.config(text=f"TAX (5%): ₹{self.tax:.2f}")
        self.total_label.config(text=f"TOTAL: ₹{self.total:.2f}")
        
        
    def update_status(self, message, level="info"):
        self.status_bar.config(text=f"  {message}")
        if level == "error":
            self.status_bar.config(background=THEME["danger"], foreground="white")
        elif level == "success":
            self.status_bar.config(background=THEME["success"], foreground="white")
        else:
            self.status_bar.config(background=THEME["primary"], foreground="white")
            
    

    def checkout(self):
        if not self.cart_items:
            messagebox.showwarning("Empty", "Cart is empty!")
            return
        
        checkout_message = f"Your total bill is ₹{self.total:.2f}.\n\nThank you for shopping with us!"
        messagebox.showinfo("Checkout Successful", checkout_message)
        self.update_status("Checkout complete! Thank you.", "success")
        
        # --- CRITICAL: PASS DATA TO CONTROLLER ---
        self.controller.shared_data["cart_items"] = self.cart_items
        self.controller.shared_data["cart_total"] = self.total
        self.controller.shared_data["pending_checkout"] = True
        
        # Switch to Auth for payment/verification
        self.controller.show_frame("AuthApp")