import tkinter as tk
from tkinter import font
import sqlite3

THEME = {
    "bg": "#101622", "card": "#151a25", "primary": "#135bec",
    "primary_hover": "#2563eb", "white": "#ffffff", "gray": "#92a4c9"
}

class AuthApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # MainApp
        self.configure(bg=THEME["bg"])
        
        self.auth_data = {"email": "", "username": "", "mobile": ""}
        self.fonts = {
            "hero": font.Font(family="Helvetica", size=32, weight="bold"),
            "sub": font.Font(family="Helvetica", size=14),
            "input": font.Font(family="Arial", size=12),
            "header": font.Font(family="Helvetica", size=24, weight="bold"),
            "sub": font.Font(family="Helvetica", size=14),
            "small": font.Font(family="Arial", size=10, weight="bold")
        }

        # Internal container for swapping Auth pages
        self.container = tk.Frame(self, bg=THEME["bg"])
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (EmailPage, RegisterPage, OTPPage, WelcomePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_internal("EmailPage")

    def show_internal(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "on_show"): frame.on_show()
        frame.tkraise()

    def on_show(self):
        """Reset auth flow when MainApp switches here"""
        self.show_internal("EmailPage")

# --- UI Helpers ---
class StyledEntry(tk.Entry):
    def __init__(self, parent, font_obj):
        super().__init__(parent, bg=THEME["card"], fg="white", font=font_obj, insertbackground="white", relief="flat")

class PrimaryButton(tk.Button):
    def __init__(self, parent, text, command):
        super().__init__(parent, text=text, command=command, bg=THEME["primary"], fg="white", font=("Arial", 12, "bold"), relief="flat", padx=20, pady=10)

# --- Pages ---

class EmailPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg"])
        self.controller = controller
        
        box = tk.Frame(self, bg=THEME["bg"])
        box.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(box, text="Sign In", bg=THEME["bg"], fg="white", font=controller.fonts["hero"]).pack(pady=10)
        tk.Label(box, text="Enter Email", bg=THEME["bg"], fg="gray").pack(anchor="w")
        
        self.entry = StyledEntry(box, controller.fonts["input"])
        self.entry.pack(pady=5, ipadx=10, ipady=10, fill="x")
        
        PrimaryButton(box, "NEXT →", self.process_email).pack(pady=20)
        
        # Back to Cart button
        tk.Button(self, text="← Cancel", bg=THEME["bg"], fg="gray", borderwidth=0, 
                  command=lambda: controller.controller.show_frame("SmartCartApp")).place(x=20, rely=0.9)

    def process_email(self):
        email = self.entry.get().strip()
        # ---------- DATABASE ----------
        self.conn = sqlite3.connect("cart_database.db")
        self.cursor = self.conn.cursor()
        
        if not email:
            return
        
        if email:
            self.controller.auth_data["email"] = email
            # Save to MainApp shared data too
            self.controller.controller.shared_data["user_info"]["email"] = email
            
            self.cursor.execute("SELECT username FROM users WHERE email=?", (email,))
            result = self.cursor.fetchone()
            if result:
                # Existing User
                self.controller.auth_data["username"] = result[0]
                self.controller.controller.shared_data["user_info"]["name"] = result[0]
                self.controller.show_internal("OTPPage")
            else:
                # New User
                self.controller.show_internal("RegisterPage")
            
            # self.controller.show_internal("OTPPage")
            

class OTPPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg"])
        self.controller = controller
        
        box = tk.Frame(self, bg=THEME["bg"])
        box.place(relx=0.5, rely=0.5, anchor="center")
        
        self.lbl = tk.Label(box, text="Verify", bg=THEME["bg"], fg="white", font=controller.fonts["hero"])
        self.lbl.pack(pady=10)
        
        self.entry = StyledEntry(box, controller.fonts["input"])
        self.entry.pack(pady=5, ipadx=10, ipady=10, fill="x")
        
        PrimaryButton(box, "VERIFY", self.verify).pack(pady=20)

    def on_show(self):
        email = self.controller.auth_data["email"]
        self.lbl.config(text=f"OTP sent to {email}")

    def verify(self):
        # Mock verification
        self.controller.show_internal("WelcomePage")
        
        
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg"])
        self.controller = controller
        
        box = tk.Frame(self, bg=THEME["bg"])
        box.place(relx=0.5, rely=0.5, anchor="center")

        # center_frame = tk.Frame(self, bg=THEME["bg"])
        # center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(box, text="Registration", bg=THEME["bg"], fg=THEME["white"], font=controller.fonts["header"]).pack(pady=(0, 10))
        tk.Label(box, text="We need a few details.", bg=THEME["bg"], fg=THEME["gray"], font=controller.fonts["sub"]).pack(pady=(0, 30))

        # Username
        tk.Label(box, text="Username", bg=THEME["bg"], fg=THEME["gray"], font=controller.fonts["small"]).pack(anchor="w", pady=(0,5))
        self.user_entry = StyledEntry(box, controller)
        self.user_entry.pack(ipadx=10, ipady=10, fill="x", pady=(0, 15))

        # Mobile
        tk.Label(box, text="Mobile Number", bg=THEME["bg"], fg=THEME["gray"], font=controller.fonts["small"]).pack(anchor="w", pady=(0,5))
        self.mobile_entry = StyledEntry(box, controller)
        self.mobile_entry.pack(ipadx=10, ipady=10, fill="x", pady=(0, 30))

        PrimaryButton(box, "NEXT →", self.process_register).pack(pady=20)

        # Back Button
        # BackButton(self, controller, "EmailPage")
        tk.Button(self, text="← Cancel", bg=THEME["bg"], fg="gray", borderwidth=0, 
                  command=lambda: controller.controller.show_frame("SmartCartApp")).place(x=20, rely=0.9)

        

    def process_register(self):
        username = self.user_entry.get()
        mobile = self.mobile_entry.get()
        
        if username and mobile:
            self.controller.shared_data["username"] = username
            self.controller.shared_data["mobile"] = mobile
            self.controller.show_frame("OTPPage")


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg"])
        self.controller = controller # This is AuthApp
        
        self.box = tk.Frame(self, bg=THEME["bg"])
        self.box.place(relx=0.5, rely=0.5, anchor="center")
        
        self.header = tk.Label(self.box, text="Success", bg=THEME["bg"], fg=THEME["primary"], font=controller.fonts["hero"])
        self.header.pack(pady=10)
        
        self.msg = tk.Label(self.box, text="", bg=THEME["bg"], fg="white", font=controller.fonts["input"])
        self.msg.pack(pady=10)
        
        PrimaryButton(self.box, "DONE", self.finish).pack(pady=20)

    def on_show(self):
        """Logic: Check if there is a pending cart to process"""
        main_app = self.controller.controller
        
        if main_app.shared_data.get("pending_checkout"):
            self.save_order(main_app)
        else:
            self.header.config(text="Welcome Back")
            self.msg.config(text="You are logged in.")

    def save_order(self, main_app):
        cart = main_app.shared_data["cart_items"]
        total = main_app.shared_data["cart_total"]
        email = main_app.shared_data["user_info"].get("email", "Guest")
        
        try:
            conn = sqlite3.connect("smart_cart.db")
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, email TEXT, total REAL)")
            cur.execute("INSERT INTO orders (email, total) VALUES (?, ?)", (email, total))
            conn.commit()
            conn.close()
            
            self.header.config(text="Order Placed!")
            self.msg.config(text=f"Amount ₹{total:.2f} billed to {email}")
            
            # Clear Cart Data in MainApp
            main_app.shared_data["pending_checkout"] = False
            main_app.shared_data["cart_items"] = {}
            main_app.shared_data["cart_total"] = 0.0
            
        except Exception as e:
            self.header.config(text="Error", fg="red")
            self.msg.config(text=str(e))

    def finish(self):
        # Go back to Welcome Screen or Cart
        self.controller.controller.show_frame("WelcomeScreen")