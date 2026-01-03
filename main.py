import tkinter as tk
from tkinter import messagebox
import sqlite3
# Import the actual cart logic from cart.py
# We alias it as 'ShoppingCart' to avoid confusion with the Login class
from cart import SmartCartApp as ShoppingCart

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Shopping Cart - Login")
        self.root.geometry("800x480")
        self.root.configure(bg="#D7FDFF")

        # Connect to database
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        
        # Ensure the users table exists (optional safety check)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                             (id TEXT PRIMARY KEY, username TEXT)''')
        self.conn.commit()

        self.start_page()

    def clear_screen(self):
        """Removes all widgets from the current window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------ START PAGE ------------------
    def start_page(self):
        self.clear_screen()
        self.root.configure(bg="#D7FDFF")
        
        start_frame = tk.Frame(self.root, bg="#D7FDFF")
        start_frame.pack(fill="both", expand=True)

        title_label = tk.Label(
            start_frame,
            text="Smart Shopping Cart",
            font=("Arial", 36, "bold"),
            fg="#000000",
            bg="#D7EBFD"
        )
        title_label.pack(pady=60)

        start_button = tk.Button(
            start_frame,
            text="START",
            font=("Arial", 18, "bold"),
            bg="#FFFAED",
            fg="black",
            width=15,
            height=2,
            relief="ridge",
            command=self.login_page
        )
        start_button.pack(pady=(0,20))

    # ------------------ LOGIN PAGE ------------------
    def login_page(self):
        self.clear_screen()
        self.root.configure(bg="#f2f2f2")

        header = tk.Frame(self.root, bg="#1f2937", height=60)
        header.pack(fill="x")
        tk.Label(header, text="SMART CART LOGIN", fg="white", bg="#1f2937",
                 font=("Arial", 18, "bold")).pack(pady=15)

        body = tk.Frame(self.root, bg="#f2f2f2")
        body.pack(expand=True)

        tk.Label(body, text="Mobile Number", font=("Arial", 14), bg="#f2f2f2").pack(pady=10)
        self.mobile_entry = tk.Entry(body, font=("Arial", 14), width=25)
        self.mobile_entry.pack()

        tk.Button(body, text="Search", bg="#16a34a", fg="white",
                  font=("Arial", 14), width=15, command=self.fetch_user).pack(pady=25)
        
        # Back button
        tk.Button(self.root, text="Back", command=self.start_page).place(x=10, y=10)

    def fetch_user(self):
        mobile = self.mobile_entry.get()
        
        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showerror("Error", "Please enter a valid 10-digit mobile number")
            return

        self.cursor.execute("SELECT username FROM users WHERE id=?", (mobile,))
        data = self.cursor.fetchone()

        if data is None:
            # User not found -> Show Registration UI
            messagebox.showinfo("Info", "User not found. Please register.")
            
            # Clear the Search button and show registration fields instead
            for widget in self.root.winfo_children():
                # Keep the header, destroy body to rebuild it
                if isinstance(widget, tk.Frame) and widget['height'] != 60: 
                    widget.destroy()

            # Rebuild body for registration
            body = tk.Frame(self.root, bg="#f2f2f2")
            body.pack(expand=True)
            
            tk.Label(body, text=f"Registering Mobile: {mobile}", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(pady=5)

            tk.Label(body, text="Enter Name", font=("Arial", 14), bg="#f2f2f2").pack(pady=10)
            self.name_entry = tk.Entry(body, font=("Arial", 14), width=25)
            self.name_entry.pack()
            
            tk.Button(body, text="Register", bg="#16a34a", fg="white",
                      font=("Arial", 14), width=15, 
                      command=lambda: self.register_user(mobile)).pack(pady=25)

        else:
            # User found -> Login Success
            username = data[0]
            messagebox.showinfo("Welcome", f"Welcome back, {username}!")
            self.launch_cart_app()

    def register_user(self, mobile):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter your name to register")
            return

        try:
            # Insert new user
            self.cursor.execute("INSERT INTO users (id, username) VALUES (?, ?)", (mobile, name))
            self.conn.commit()
            messagebox.showinfo("Success", f"User {name} registered successfully!")
            self.launch_cart_app()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not register: {e}")

    # ------------------ TRANSITION ------------------
    def launch_cart_app(self):
        """Destroys current login widgets and launches the Cart App"""
        self.clear_screen()
        # Close the local user database connection as we are moving to the cart
        self.conn.close()
        
        # Initialize the class from cart.py, passing the SAME root window
        ShoppingCart(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()