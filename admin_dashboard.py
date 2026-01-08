import tkinter as tk
from tkinter import font

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard (Landscape)")
        self.root.geometry("1024x600")
        
        # --- Colors ---
        self.bg_color = "#101622"       # Dark background
        self.card_bg = "#151a25"        # Standard card background
        self.hover_bg = "#232d3f"       # Lighter background for Hover effect
        self.primary_color = "#135bec"  # Blue
        self.primary_hover = "#2563eb"  # Lighter Blue for FAB hover
        self.text_white = "#ffffff"
        self.text_gray = "#92a4c9"
        self.accent_green = "#10B981"   
        self.accent_orange = "#F59E0B"  
        self.highlight_border = "#2563eb" 
        
        self.root.configure(bg=self.bg_color)

        # --- Fonts ---
        self.font_header = font.Font(family="Helvetica", size=18, weight="bold")
        self.font_title = font.Font(family="Helvetica", size=14, weight="bold") 
        self.font_subtitle = font.Font(family="Helvetica", size=11)
        self.font_large_num = font.Font(family="Helvetica", size=24, weight="bold")
        self.font_btn = font.Font(family="Helvetica", size=12, weight="bold")

        # --- Main Layout Construction ---
        self.create_header()
        
        # Container for the main content
        self.content_frame = tk.Frame(self.root, bg=self.bg_color)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Left and Right columns
        self.left_col = tk.Frame(self.content_frame, bg=self.bg_color)
        self.left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        self.right_col = tk.Frame(self.content_frame, bg=self.bg_color)
        self.right_col.pack(side="right", fill="both", expand=True, padx=(0, 0))

        # Populate Columns 
        self.create_quick_actions(self.left_col) 
        self.create_overview_section(self.right_col) 
        
        # Bottom Elements
        self.create_footer()
        self.create_fab()

    def add_hover_effect(self, widgets_to_change, trigger_widgets, hover_color, default_color):
        """
        Helper to add hover effects to composite widgets.
        widgets_to_change: List of widgets that should change color (e.g., background frame, labels).
        trigger_widgets: List of widgets that trigger the hover (usually same as above + icons).
        """
        def on_enter(event):
            for widget in widgets_to_change:
                widget.configure(bg=hover_color)

        def on_leave(event):
            # Check if mouse is still inside one of the trigger widgets to prevent flickering
            # when moving between the frame and the label inside it.
            x, y = self.root.winfo_pointerxy()
            widget_under_mouse = self.root.winfo_containing(x, y)
            
            if widget_under_mouse not in trigger_widgets:
                for widget in widgets_to_change:
                    widget.configure(bg=default_color)

        for widget in trigger_widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def create_header(self):
        """Top bar with profile only"""
        header_frame = tk.Frame(self.root, bg=self.bg_color, pady=15, padx=20)
        header_frame.pack(fill="x")

        # Profile Image Placeholder (Circle)
        profile_canvas = tk.Canvas(header_frame, width=40, height=40, bg=self.bg_color, highlightthickness=0)
        profile_canvas.pack(side="left")
        profile_canvas.create_oval(2, 2, 38, 38, fill=self.card_bg, outline=self.primary_color, width=2)
        tk.Label(header_frame, text="👨‍💼", bg=self.card_bg, fg="white", font=("Arial", 16)).place(in_=profile_canvas, x=8, y=5)

        # Welcome Text
        text_frame = tk.Frame(header_frame, bg=self.bg_color, padx=10)
        text_frame.pack(side="left")
        
        tk.Label(text_frame, text="WELCOME BACK", bg=self.bg_color, fg=self.text_gray, font=("Helvetica", 8, "bold")).pack(anchor="w")
        tk.Label(text_frame, text="Admin Dashboard", bg=self.bg_color, fg=self.text_white, font=self.font_title).pack(anchor="w")

    def create_overview_section(self, parent):
        """The statistic cards (Secondary)"""
        header = tk.Frame(parent, bg=self.bg_color)
        header.pack(fill="x", pady=(0, 15))
        tk.Label(header, text="Overview", bg=self.bg_color, fg=self.text_gray, font=("Helvetica", 14, "bold")).pack(side="left")

        grid_frame = tk.Frame(parent, bg=self.bg_color)
        grid_frame.pack(fill="both", expand=True)
        
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        self.create_stat_card(grid_frame, 0, 0, "👥", "TOTAL USERS", "1.2k", "+12%", self.accent_green)
        self.create_stat_card(grid_frame, 0, 1, "📦", "PRODUCTS", "450", "+5%", self.accent_green)
        self.create_stat_card(grid_frame, 1, 0, "👤", "NEW USERS", "12", "Today", self.text_gray)
        self.create_stat_card(grid_frame, 1, 1, "⚠", "LOW STOCK", "3", "Alerts", self.accent_orange)

    def create_stat_card(self, parent, row, col, icon, title, value, footer_text, footer_color):
        card = tk.Frame(parent, bg=self.card_bg, padx=15, pady=15)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        head_frame = tk.Frame(card, bg=self.card_bg)
        head_frame.pack(anchor="w", fill="x")
        tk.Label(head_frame, text=icon, bg=self.card_bg, fg=self.text_gray, font=("Arial", 14)).pack(side="left")
        tk.Label(head_frame, text=title, bg=self.card_bg, fg=self.text_gray, font=("Helvetica", 8, "bold")).pack(side="left", padx=5)

        tk.Label(card, text=value, bg=self.card_bg, fg=self.text_white, font=("Helvetica", 20, "bold")).pack(anchor="w", pady=(5,0))
        tk.Label(card, text=footer_text, bg=self.card_bg, fg=footer_color, font=("Helvetica", 8, "bold")).pack(anchor="w")

    def create_quick_actions(self, parent):
        """The main focus area"""
        tk.Label(parent, text="Quick Actions", bg=self.bg_color, fg=self.text_white, font=self.font_header).pack(anchor="w", pady=(0, 20))

        btn_container = tk.Frame(parent, bg=self.bg_color)
        btn_container.pack(fill="both", expand=True)

        # Action 1: Users List
        self.create_action_button(btn_container, "Users List", "Manage accounts & permissions", "👥", "#1e3a8a", self.open_users)
        
        # Spacer
        tk.Frame(btn_container, bg=self.bg_color, height=25).pack()

        # Action 2: Product List
        self.create_action_button(btn_container, "Product List", "Inventory, pricing & stock", "📦", "#312e81", self.open_products)

    def create_action_button(self, parent, title, subtitle, icon, color_tint, command):
        """Creates a very large, prominent button with hover effects"""
        
        # Outer frame for border
        border_frame = tk.Frame(parent, bg=self.highlight_border, padx=2, pady=2, cursor="hand2")
        border_frame.pack(fill="x")
        
        # Inner content frame
        btn_frame = tk.Frame(border_frame, bg=self.card_bg, height=140) 
        btn_frame.pack(fill="both", expand=True)
        btn_frame.pack_propagate(False) 

        # Visual accent on the left
        accent = tk.Frame(btn_frame, bg=color_tint, width=100)
        accent.pack(side="left", fill="y")
        
        # Icon inside accent
        icon_lbl = tk.Label(accent, text=icon, bg=color_tint, fg="white", font=("Arial", 32))
        icon_lbl.place(relx=0.5, rely=0.5, anchor="center")

        # Text Content container
        content = tk.Frame(btn_frame, bg=self.card_bg, padx=25)
        content.pack(side="left", fill="both", expand=True)

        title_lbl = tk.Label(content, text=title, bg=self.card_bg, fg=self.text_white, font=self.font_title)
        title_lbl.pack(anchor="w", pady=(30, 5))
        
        sub_lbl = tk.Label(content, text=subtitle, bg=self.card_bg, fg=self.text_gray, font=self.font_subtitle)
        sub_lbl.pack(anchor="w")

        # Bind click events
        clickable_widgets = [border_frame, btn_frame, accent, icon_lbl, content, title_lbl, sub_lbl]
        for widget in clickable_widgets: 
            widget.bind("<Button-1>", lambda e: command())

        # --- HOVER LOGIC ---
        # The widgets that should physically change color (Background and text areas)
        # Note: We do NOT change the accent color, it stays the tinted blue.
        change_group = [btn_frame, content, title_lbl, sub_lbl]
        
        # The widgets that trigger the hover (including the accent, so the button feels solid)
        trigger_group = clickable_widgets
        
        self.add_hover_effect(change_group, trigger_group, self.hover_bg, self.card_bg)

    def create_footer(self):
        """Bottom bar with Back Button"""
        nav_frame = tk.Frame(self.root, bg=self.bg_color, pady=20, padx=20)
        nav_frame.pack(side="bottom", fill="x")

        # Back Button logic
        back_btn_frame = tk.Frame(nav_frame, bg=self.card_bg, padx=15, pady=8, cursor="hand2")
        back_btn_frame.pack(side="left")
        
        lbl_icon = tk.Label(back_btn_frame, text="⬅", bg=self.card_bg, fg=self.text_white, font=("Arial", 12))
        lbl_icon.pack(side="left", padx=(0,10))
        
        lbl_text = tk.Label(back_btn_frame, text="Back to Start Page", bg=self.card_bg, fg=self.text_white, font=self.font_btn)
        lbl_text.pack(side="left")
        
        # Bind Click
        widgets = [back_btn_frame, lbl_icon, lbl_text]
        for w in widgets:
            w.bind("<Button-1>", lambda e: self.go_back())
            
        # Bind Hover
        self.add_hover_effect(widgets, widgets, self.hover_bg, self.card_bg)

    def create_fab(self):
        """Floating Action Button (+)"""
        fab = tk.Label(self.root, text="+", bg=self.primary_color, fg="white", font=("Arial", 24), width=2, height=1, cursor="hand2")
        fab.place(relx=0.95, rely=0.88, anchor="center")
        
        # Simple hover for single widget
        fab.bind("<Enter>", lambda e: fab.configure(bg=self.primary_hover))
        fab.bind("<Leave>", lambda e: fab.configure(bg=self.primary_color))
        
    # --- Button Commands ---
    def open_users(self):
        print("Opening User Details...")

    def open_products(self):
        print("Opening Product Details...")
        
    def go_back(self):
        print("Going back to Start Page...")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()