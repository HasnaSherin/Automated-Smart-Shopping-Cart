import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import cv2
from pyzbar.pyzbar import decode

class SmartCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Shopping Cart")
        self.root.geometry("800x480")
        self.root.configure(bg="#f0f2f5")
        self.root.minsize(700, 500) # Set a minimum size

        self.cart_items = {}
        self.total = 0.0
        self.tax_rate = 0.05  # 5% tax

        # This makes the main window resizable
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._create_widgets()
        self._update_totals()
        self.update_status("Welcome! Scan your first item to begin.")
        self._toggle_cart_view()

    def _create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1) # The cart frame will expand

        # --- Header ---
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        header_label = ttk.Label(header_frame, text="Your Shopping Cart", font=("Arial", 24, "bold"), background="#f0f2f5")
        header_label.pack(side=tk.LEFT)

        # --- Cart items display ---
        self.cart_frame = ttk.Frame(main_frame, style='Card.TFrame')
        self.cart_frame.grid(row=1, column=0, sticky="nsew")
        self.cart_frame.columnconfigure(0, weight=1)
        self.cart_frame.rowconfigure(0, weight=1)

        # Treeview for item list
        columns = ("name", "quantity", "price", "total")
        self.tree = ttk.Treeview(self.cart_frame, columns=columns, show="headings", height=15)
        self.tree.heading("name", text="Item Name")
        self.tree.heading("quantity", text="Qty")
        self.tree.heading("price", text="Unit Price")
        self.tree.heading("total", text="Total")

        self.tree.column("name", width=300)
        self.tree.column("quantity", anchor=tk.CENTER, width=80)
        self.tree.column("price", anchor=tk.E, width=120)
        self.tree.column("total", anchor=tk.E, width=120)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(self.cart_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Empty Cart Message ---
        self.empty_cart_label = ttk.Label(main_frame, text="Your cart is empty.", font=("Arial", 18), background="white", anchor="center")
        # Will be placed on top of cart_frame using grid

        # --- Totals Display ---
        totals_frame = ttk.Frame(main_frame, padding=(0, 20, 0, 0), style='Totals.TFrame')
        totals_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        totals_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.subtotal_label = ttk.Label(totals_frame, text="Subtotal: ₹0.00", font=("Arial", 14), background="#e9ecef")
        self.subtotal_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.tax_label = ttk.Label(totals_frame, text="Tax (5%): ₹0.00", font=("Arial", 14), background="#e9ecef")
        self.tax_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.total_label = ttk.Label(totals_frame, text="Total: ₹0.00", font=("Arial", 18, "bold"), background="#e9ecef")
        self.total_label.grid(row=0, column=3, sticky="e", padx=10, pady=5)


        # --- Buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky="ew", pady=20)
        button_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.scan_camera_button = ttk.Button(button_frame, text="Scan with Camera", command=self.scan_with_camera, style='Accent.TButton')
        self.scan_camera_button.grid(row=0, column=0, padx=5, ipady=10, sticky="ew")
        
        self.scan_button = ttk.Button(button_frame, text="Simulate Scan", command=self.simulate_scan)
        self.scan_button.grid(row=0, column=1, padx=5, ipady=10, sticky="ew")

        self.remove_button = ttk.Button(button_frame, text="Remove Selected", command=self.remove_item)
        self.remove_button.grid(row=0, column=2, padx=5, ipady=10, sticky="ew")

        self.checkout_button = ttk.Button(button_frame, text="Checkout", command=self.checkout, style='Success.TButton')
        self.checkout_button.grid(row=0, column=3, padx=5, ipady=10, sticky="ew")

        # --- Status Bar ---
        self.status_bar = ttk.Label(self.root, text="Welcome!", relief=tk.SUNKEN, anchor=tk.W, padding=5)
        self.status_bar.grid(row=1, column=0, sticky="ew")

        self._configure_styles()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f2f5')
        style.configure('Card.TFrame', background='white', relief='raised', borderwidth=1)
        style.configure('Totals.TFrame', background='#e9ecef', relief='groove')
        style.configure('TButton', font=('Arial', 12), padding=10, background='#ffffff', foreground='#333333')
        style.map('TButton',
            background=[('active', '#e0e0e0')],
            foreground=[('active', '#000000')]
        )
        style.configure('Accent.TButton', font=('Arial', 12, 'bold'), background='#0d6efd', foreground='white')
        style.map('Accent.TButton',
            background=[('active', '#0b5ed7')]
        )
        style.configure('Success.TButton', font=('Arial', 12, 'bold'), background='#198754', foreground='white')
        style.map('Success.TButton',
            background=[('active', '#157347')]
        )
        style.configure('Treeview', rowheight=30, font=('Arial', 12))
        style.configure('Treeview.Heading', font=('Arial', 14, 'bold'))
        style.map("Treeview", background=[('selected', '#0d6efd')])

    def scan_with_camera(self):
        self.update_status("Opening camera... Please show a barcode.")
        cap = cv2.VideoCapture(1)
        
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
            cursor.execute("SELECT barcode, name, price, weight_grams FROM products ORDER BY RANDOM() LIMIT 1")
            product = cursor.fetchone()
            conn.close()

            if product:
                barcode, name, price, weight = product
                self.add_item(barcode, name, price)
                self.update_status(f"Scanned: {name}")
            else:
                self.update_status("Database is empty. No item to scan.", "error")
        except sqlite3.Error as e:
            self.update_status(f"Database error: {e}", "error")
            messagebox.showerror("Database Error", "Could not connect to the product database. Please make sure 'products.db' exists and is valid.")


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

        self.subtotal_label.config(text=f"Subtotal: ₹{self.subtotal:.2f}")
        self.tax_label.config(text=f"Tax ({self.tax_rate:.0%}): ₹{self.tax:.2f}")
        self.total_label.config(text=f"Total: ₹{self.total:.2f}")

    def checkout(self):
        """Handles the checkout process."""
        if not self.cart_items:
            messagebox.showinfo("Empty Cart", "Your cart is empty. Please scan items to checkout.")
            return

        checkout_message = f"Your total bill is ₹{self.total:.2f}.\n\nThank you for shopping with us!"
        messagebox.showinfo("Checkout Successful", checkout_message)
        self.update_status("Checkout complete! Thank you.")
        self.cart_items.clear()
        self._update_cart_display()

    def update_status(self, message, level="info"):
        self.status_bar.config(text=message)
        if level == "error":
            self.status_bar.config(background="#dc3545", foreground="white")
        else:
            self.status_bar.config(background="#f0f2f5", foreground="black")


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCartApp(root)
    root.mainloop()