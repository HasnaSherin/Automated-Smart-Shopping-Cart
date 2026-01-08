import tkinter as tk
from tkinter import font

class WelcomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home System")
        self.root.geometry("1024x600") # 7-inch Landscape
        
        # --- Theme Colors (Same as Admin Dashboard) ---
        self.colors = {
            "bg": "#101622",           # Dark Background
            "card": "#151a25",         # Card Background
            "primary": "#135bec",      # Blue
            "primary_hover": "#2563eb",# Lighter Blue for hover
            "white": "#ffffff",
            "gray": "#92a4c9",
            "danger": "#ef4444"
        }
        
        self.root.configure(bg=self.colors["bg"])

        # --- Fonts ---
        self.fonts = {
            "hero": font.Font(family="Helvetica", size=32, weight="bold"),
            "sub": font.Font(family="Helvetica", size=14),
            "btn": font.Font(family="Helvetica", size=16, weight="bold"),
            "small": font.Font(family="Arial", size=10)
        }

        # --- Layout ---
        self.create_admin_button()
        self.create_center_content()
        self.create_footer()

    """def create_admin_button(self):
        #Discreet Admin Button in Top-Left Corner
        # Using a Frame to create a custom button look
        self.admin_btn_frame = tk.Frame(self.root, bg=self.colors["bg"], cursor="hand2")
        self.admin_btn_frame.place(x=20, y=20)

        # Icon and Text
        icon_lbl = tk.Label(self.admin_btn_frame, text="⚙️", bg=self.colors["bg"], fg=self.colors["gray"], font=("Arial", 16))
        icon_lbl.pack(side="left")
        
        text_lbl = tk.Label(self.admin_btn_frame, text="ADMIN", bg=self.colors["bg"], fg=self.colors["gray"], font=("Helvetica", 10, "bold"))
        text_lbl.pack(side="left", padx=5)"""
    
    def create_admin_button(self):
        """Discreet Admin Button in Bottom-Left Corner"""
        # Using a Frame to create a custom button look
        self.admin_btn_frame = tk.Frame(self.root, bg=self.colors["bg"], cursor="hand2")
        self.admin_btn_frame.place(x=20, rely=1.0, anchor="sw", y=-20)

        # Icon and Text
        icon_lbl = tk.Label(self.admin_btn_frame, text="⚙️", bg=self.colors["bg"], fg=self.colors["gray"], font=("Arial", 16))
        icon_lbl.pack(side="left")
        
        text_lbl = tk.Label(self.admin_btn_frame, text="ADMIN", bg=self.colors["bg"], fg=self.colors["gray"], font=("Helvetica", 10, "bold"))
        text_lbl.pack(side="left", padx=5)

        # Bind events for hover effect
        for widget in [self.admin_btn_frame, icon_lbl, text_lbl]:
            widget.bind("<Enter>", lambda e: self.on_hover(self.admin_btn_frame, icon_lbl, text_lbl, is_admin=True))
            widget.bind("<Leave>", lambda e: self.on_leave(self.admin_btn_frame, icon_lbl, text_lbl, is_admin=True))
            widget.bind("<Button-1>", lambda e: self.open_admin_panel())

        # Bind events for hover effect
        for widget in [self.admin_btn_frame, icon_lbl, text_lbl]:
            widget.bind("<Enter>", lambda e: self.on_hover(self.admin_btn_frame, icon_lbl, text_lbl, is_admin=True))
            widget.bind("<Leave>", lambda e: self.on_leave(self.admin_btn_frame, icon_lbl, text_lbl, is_admin=True))
            widget.bind("<Button-1>", lambda e: self.open_admin_panel())

    def create_center_content(self):
        """Centered Welcome Text and Big Start Button"""
        center_frame = tk.Frame(self.root, bg=self.colors["bg"])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Hero Title
        tk.Label(center_frame, text="SMART SHOPPING CART", bg=self.colors["bg"], fg=self.colors["white"], font=self.fonts["hero"]).pack(pady=(0, 5))
        
        # 2. Subtitle
        tk.Label(center_frame, text="for automated billing", bg=self.colors["bg"], fg=self.colors["gray"], font=self.fonts["sub"]).pack(pady=(0, 40))

        # 3. The "START" Button (Custom styled)
        self.start_btn = tk.Frame(center_frame, bg=self.colors["primary"], width=200, height=60, cursor="hand2")
        self.start_btn.pack_propagate(False) # Force the frame to stay 200x60
        self.start_btn.pack()

        self.start_label = tk.Label(self.start_btn, text="GET STARTED  →", bg=self.colors["primary"], fg=self.colors["white"], font=self.fonts["btn"])
        self.start_label.place(relx=0.5, rely=0.5, anchor="center")

        # Bind Hover Events for Start Button
        for widget in [self.start_btn, self.start_label]:
            widget.bind("<Enter>", lambda e: self.start_hover(True))
            widget.bind("<Leave>", lambda e: self.start_hover(False))
            widget.bind("<Button-1>", lambda e: self.start_app())

    def create_footer(self):
        """Optional footer for aesthetics"""
        footer = tk.Label(self.root, text="v1.0.0 • System Ready", bg=self.colors["bg"], fg="#334155", font=self.fonts["small"])
        footer.place(relx=0.5, rely=0.95, anchor="center")

    # --- Interaction Logic ---

    def start_hover(self, hovering):
        """Handles the hover animation for the main button"""
        color = self.colors["primary_hover"] if hovering else self.colors["primary"]
        self.start_btn.configure(bg=color)
        self.start_label.configure(bg=color)

    def on_hover(self, frame, icon, text, is_admin=False):
        """Handles hover for text/icon buttons"""
        if is_admin:
            icon.configure(fg=self.colors["white"])
            text.configure(fg=self.colors["white"])

    def on_leave(self, frame, icon, text, is_admin=False):
        """Reset hover"""
        if is_admin:
            icon.configure(fg=self.colors["gray"])
            text.configure(fg=self.colors["gray"])

    # --- Commands ---

    def start_app(self):
        print("System Starting...")
        # Add code here to switch frames or open the Dashboard

    def open_admin_panel(self):
        print("Requesting Admin Access...")
        # Add code here to open login popup

if __name__ == "__main__":
    root = tk.Tk()
    app = WelcomeScreen(root)
    root.mainloop()