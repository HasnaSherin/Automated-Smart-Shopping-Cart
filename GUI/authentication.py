import tkinter as tk
from tkinter import font

# --- Configuration & Theme (Derived from your snippet) ---
THEME = {
    "bg": "#101622",           # Dark Background
    "card": "#151a25",         # Input/Card Background
    "primary": "#135bec",      # Blue
    "primary_hover": "#2563eb",# Lighter Blue
    "white": "#ffffff",
    "gray": "#92a4c9",
    "danger": "#ef4444"
}

# Mock Database for testing logic
EXISTING_EMAILS = ["test@gmail.com", "admin@shc.com"] 

class AuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Checkout Authentication")
        self.geometry("1024x600")
        self.configure(bg=THEME["bg"])
        
        # --- Shared Data Store ---
        self.shared_data = {
            "email": "",
            "username": "",
            "mobile": "",
            "is_registered": False
        }

        # --- Fonts Setup ---
        self.fonts = {
            "hero": font.Font(family="Helvetica", size=32, weight="bold"),
            "header": font.Font(family="Helvetica", size=24, weight="bold"),
            "sub": font.Font(family="Helvetica", size=14),
            "btn": font.Font(family="Helvetica", size=14, weight="bold"),
            "input": font.Font(family="Arial", size=12),
            "small": font.Font(family="Arial", size=10, weight="bold")
        }

        # --- Container for Pages ---
        self.container = tk.Frame(self, bg=THEME["bg"])
        self.container.pack(side="top", fill="both", expand=True)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Initialize all pages
        for F in (EmailPage, RegisterPage, OTPPage, WelcomePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("EmailPage")

    def show_frame(self, page_name):
        '''Brings the requested frame to the top'''
        frame = self.frames[page_name]
        # If the page has an update function (to load data), call it
        if hasattr(frame, "update_view"):
            frame.update_view()
        frame.tkraise()

    def get_font(self, name):
        return self.fonts[name]

# --- UI Component Helpers ---

class StyledEntry(tk.Entry):
    '''Custom Entry widget to match the dark theme'''
    def __init__(self, parent, controller, placeholder=""):
        super().__init__(
            parent, 
            bg=THEME["card"], 
            fg=THEME["white"], 
            insertbackground=THEME["white"], # Cursor color
            font=controller.get_font("input"),
            relief="flat",
            highlightthickness=1,
            highlightbackground=THEME["gray"],
            highlightcolor=THEME["primary"]
        )

class PrimaryButton(tk.Frame):
    '''The Blue "Next" Button Component'''
    def __init__(self, parent, text, command, controller):
        super().__init__(parent, bg=THEME["primary"], width=200, height=50, cursor="hand2")
        self.controller = controller
        self.command = command
        self.pack_propagate(False)
        
        self.lbl = tk.Label(self, text=text, bg=THEME["primary"], fg=THEME["white"], font=controller.get_font("btn"))
        self.lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        # Bindings
        for widget in [self, self.lbl]:
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)
            widget.bind("<Button-1>", lambda e: self.command())

    def on_enter(self, e):
        self.configure(bg=THEME["primary_hover"])
        self.lbl.configure(bg=THEME["primary_hover"])

    def on_leave(self, e):
        self.configure(bg=THEME["primary"])
        self.lbl.configure(bg=THEME["primary"])

class BackButton(tk.Frame):
    '''The Bottom-Left Back Button'''
    def __init__(self, parent, controller, target_page):
        super().__init__(parent, bg=THEME["bg"], cursor="hand2")
        self.place(x=20, rely=1.0, anchor="sw", y=-20)
        
        self.lbl = tk.Label(self, text="← BACK", bg=THEME["bg"], fg=THEME["gray"], font=controller.get_font("small"))
        self.lbl.pack()

        # Bindings
        for widget in [self, self.lbl]:
            widget.bind("<Enter>", lambda e: self.lbl.configure(fg=THEME["white"]))
            widget.bind("<Leave>", lambda e: self.lbl.configure(fg=THEME["gray"]))
            widget.bind("<Button-1>", lambda e: controller.show_frame(target_page))


# --- PAGES ---

class EmailPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg"])
        self.controller = controller
        
        center_frame = tk.Frame(self, bg=THEME["bg"])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # UI
        tk.Label(center_frame, text="Sign In", bg=THEME["bg"], fg=THEME["white"], font=controller.get_font("hero")).pack(pady=(0, 10))
        tk.Label(center_frame, text="Enter your email to continue", bg=THEME["bg"], fg=THEME["gray"], font=controller.get_font("sub")).pack(pady=(0, 30))

        tk.Label(center_frame, text="Email Address", bg=THEME["bg"], fg=THEME["gray"], font=controller.get_font("small")).pack(anchor="w", pady=(0,5))
        
        self.email_entry = StyledEntry(center_frame, controller)
        self.email_entry.pack(ipadx=10, ipady=10, fill="x", pady=(0, 30))
        self.email_entry.focus() # Auto focus

        self.btn = PrimaryButton(center_frame, "NEXT  →", self.process_email, controller)
        self.btn.pack()

        # No Back button on first page (optional)
    
    def process_email(self):
        email = self.email_entry.get().strip()
        if not email:
            return # Add error handling logic here if desired
        
        self.controller.shared_data["email"] = email
        
        # LOGIC: Check if registered
        if email in EXISTING_EMAILS:
            print(f"User {email} found. Redirecting to OTP.")
            self.controller.shared_data["is_registered"] = True
            # Simulate fetching username from DB
            self.controller.shared_data["username"] = "Existing User" 
            self.controller.show_frame("OTPPage")
        else:
            print(f"User {email} not found. Redirecting to Register.")
            self.controller.shared_data["is_registered"] = False
            self.controller.show_frame("RegisterPage")


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg"])
        self.controller = controller

        center_frame = tk.Frame(self, bg=THEME["bg"])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="Registration", bg=THEME["bg"], fg=THEME["white"], font=controller.get_font("header")).pack(pady=(0, 10))
        tk.Label(center_frame, text="We need a few details.", bg=THEME["bg"], fg=THEME["gray"], font=controller.get_font("sub")).pack(pady=(0, 30))

        # Username
        tk.Label(center_frame, text="Username", bg=THEME["bg"], fg=THEME["gray"], font=controller.get_font("small")).pack(anchor="w", pady=(0,5))
        self.user_entry = StyledEntry(center_frame, controller)
        self.user_entry.pack(ipadx=10, ipady=10, fill="x", pady=(0, 15))

        # Mobile
        tk.Label(center_frame, text="Mobile Number", bg=THEME["bg"], fg=THEME["gray"], font=controller.get_font("small")).pack(anchor="w", pady=(0,5))
        self.mobile_entry = StyledEntry(center_frame, controller)
        self.mobile_entry.pack(ipadx=10, ipady=10, fill="x", pady=(0, 30))

        self.btn = PrimaryButton(center_frame, "NEXT  →", self.process_register, controller)
        self.btn.pack()

        # Back Button
        BackButton(self, controller, "EmailPage")

    def process_register(self):
        username = self.user_entry.get()
        mobile = self.mobile_entry.get()
        
        if username and mobile:
            self.controller.shared_data["username"] = username
            self.controller.shared_data["mobile"] = mobile
            self.controller.show_frame("OTPPage")


class OTPPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg"])
        self.controller = controller
        
        self.center_frame = tk.Frame(self, bg=THEME["bg"])
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.center_frame, text="Verification", bg=THEME["bg"], fg=THEME["white"], font=controller.get_font("header")).pack(pady=(0, 10))
        
        # Dynamic label (updated in update_view)
        self.info_label = tk.Label(self.center_frame, text="", bg=THEME["bg"], fg=THEME["gray"], font=controller.get_font("sub"))
        self.info_label.pack(pady=(0, 30))

        tk.Label(self.center_frame, text="Enter 4-digit OTP", bg=THEME["bg"], fg=THEME["gray"], font=controller.get_font("small")).pack(anchor="w", pady=(0,5))
        
        self.otp_entry = StyledEntry(self.center_frame, controller)
        self.otp_entry.pack(ipadx=10, ipady=10, fill="x", pady=(0, 30))

        self.btn = PrimaryButton(self.center_frame, "VERIFY & LOGIN", self.process_otp, controller)
        self.btn.pack()

        # Back Button Logic (Dynamic destination based on where we came from)
        self.back_btn_frame = tk.Frame(self, bg=THEME["bg"], cursor="hand2")
        self.back_btn_frame.place(x=20, rely=1.0, anchor="sw", y=-20)
        
        self.back_lbl = tk.Label(self.back_btn_frame, text="← BACK", bg=THEME["bg"], fg=THEME["gray"], font=controller.get_font("small"))
        self.back_lbl.pack()
        
        # Bind Back Button
        for w in [self.back_btn_frame, self.back_lbl]:
            w.bind("<Button-1>", lambda e: self.go_back())
            w.bind("<Enter>", lambda e: self.back_lbl.configure(fg=THEME["white"]))
            w.bind("<Leave>", lambda e: self.back_lbl.configure(fg=THEME["gray"]))

    def update_view(self):
        """Called every time this frame is shown"""
        email = self.controller.shared_data["email"]
        self.info_label.config(text=f"Enter the OTP sent to\n{email}")
        self.otp_entry.delete(0, tk.END) # Clear previous input

    def go_back(self):
        # Determine previous page based on registration status
        if self.controller.shared_data["is_registered"]:
            self.controller.show_frame("EmailPage")
        else:
            self.controller.show_frame("RegisterPage")

    def process_otp(self):
        otp = self.otp_entry.get()
        # Mock verification - verify any 4 digit code or specific "1234"
        if len(otp) > 0: 
            self.controller.show_frame("WelcomePage")


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=THEME["bg"])
        self.controller = controller
        
        self.center_frame = tk.Frame(self, bg=THEME["bg"])
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Dynamic Welcome Text
        self.welcome_label = tk.Label(self.center_frame, text="", bg=THEME["bg"], fg=THEME["primary"], font=controller.get_font("hero"))
        self.welcome_label.pack(pady=(0, 10))
        
        tk.Label(self.center_frame, text="Authentication Successful", bg=THEME["bg"], fg=THEME["white"], font=controller.get_font("sub")).pack()

        # Logout / Restart
        BackButton(self, controller, "EmailPage")

    def update_view(self):
        user = self.controller.shared_data["username"]
        self.welcome_label.config(text=f"Welcome, {user}!")


if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()