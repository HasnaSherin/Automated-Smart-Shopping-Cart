from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

import tkinter as tk
from tkinter import ttk, messagebox

class SmartCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Shopping Cart")
        self.root.geometry("800x480")  # 7-inch display
        self.root.configure(bg="#f2f2f2")

        # ------------------ START PAGE ------------------
        start_frame = tk.Frame(self.root, bg="#D7FDFF")
        title_label = tk.Label(
                start_frame,
                text="Smart Shopping Cart",
                font=("Arial", 36, "bold"),
                fg="#000000",
                bg="#D7EBFD"
            )
        title_label.pack(pady=80)

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
        start_button.pack()

        start_frame.pack(fill="both", expand=True)

        # ---------- LOGIN PAGE ----------
    def login_page(self):
        self.clear_screen()

        header = tk.Frame(self.root, bg="#1f2937", height=60)
        header.pack(fill="x")
        tk.Label(header, text="SMART CART LOGIN", fg="white", bg="#1f2937",
                 font=("Arial", 18, "bold")).pack(pady=15)

        body = tk.Frame(self.root, bg="#f2f2f2")
        body.pack(expand=True)

        tk.Label(body, text="Mobile Number", font=("Arial", 14), bg="#f2f2f2").pack(pady=10)
        self.mobile_entry = tk.Entry(body, font=("Arial", 14), width=25)
        self.mobile_entry.pack()
        #self.mobile_entry.bind("<FocusOut>", self.fetch_user)

        tk.Button(body, text="Search", bg="#16a34a", fg="white",
                  font=("Arial", 14), width=15, command=self.fetch_user).pack(pady=25)


    def fetch_user(self, event=None):
        mobile = self.mobile_entry.get()
        if mobile.isdigit() and len(mobile) == 10:
            #return
            data = supabase.table("users").select("*").eq("id", mobile).execute()
            if data.data == []:
                messagebox.showinfo("Info", "User not found. Please register.")

                body = tk.Frame(self.root, bg="#f2f2f2")
                body.pack(expand=True)

                tk.Label(body, text="Name", font=("Arial", 14), bg="#f2f2f2").pack(pady=10)
                self.name_entry = tk.Entry(body, font=("Arial", 14), width=25)
                self.name_entry.pack()
                
                name = self.name_entry.get()
                tk.Button(body, text="Register", bg="#16a34a", fg="white",
                          font=("Arial", 14), width=15, command=lambda: self.register_user(mobile, name)).pack(pady=15)
                
            else:
                body = tk.Frame(self.root, bg="#f2f2f2")
                body.pack(expand=True)

                #print(f"Welcome {data.data[0]['username']}! Start shopping now.\n")
                messagebox.showinfo("Welcome", f"Welcome {data.data[0]['username']}")
                tk.Label(body, text=f"Welcome {data.data[0]['username']}! Start shopping now.", font=("Arial", 14), bg="#f2f2f2").pack(pady=10)
                tk.Button(body, text="Continue", bg="#16a34a", fg="white",
                  font=("Arial", 14), width=15, command=self.cart_page).pack(pady=25)

        # result = data.data[0] if data.data else None
        # if result:
        #     self.name_entry.delete(0, tk.END)
        #     self.name_entry.insert(0, result["name"])
        #     messagebox.showinfo("Welcome", f"Welcome {result['name']}")

    # def register_user(self, mobile, name):
    #     supabase.table("users").insert({"id": mobile, "username": name}).execute()
    #     messagebox.showinfo("Success", f"User {name} registered successfully!")
    #     self.cart_page()
        #return messagebox.showinfo("Success", f"User {name} registered successfully!")

    def register_user(self, mobile, name):
        if not name:
            messagebox.showerror("Error", "Please enter your name to register")
            return

        supabase.table("users").insert({"id": mobile, "username": name}).execute()
        messagebox.showinfo("Success", f"User {name} registered successfully!")
        self.cart_page()


    # ---------- CART PAGE ----------
    def cart_page(self):
        self.clear_screen()
        self.cart = []

        header = tk.Frame(self.root, bg="#1f2937", height=50)
        header.pack(fill="x")

        back_btn = tk.Button(header, text="← Home", bg="#374151", fg="white",
                             font=("Arial", 11), command=self.login_page)
        back_btn.place(x=10, y=10)

        title = tk.Label(header, text="MY CART", bg="#1f2937", fg="white",
                         font=("Arial", 16, "bold"))
        title.place(relx=0.5, rely=0.5, anchor="center")

        table_frame = tk.Frame(self.root, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Item", "MRP", "Tax", "Qty", "Discount", "Amount")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True)

        total_frame = tk.Frame(self.root, bg="#e5e7eb", height=50)
        total_frame.pack(fill="x", padx=10, pady=5)

        self.total_var = tk.StringVar(value="Total: ₹0.00")
        tk.Label(total_frame, textvariable=self.total_var,
                 font=("Arial", 14, "bold"), bg="#e5e7eb").pack(side="right", padx=20)

        footer = tk.Frame(self.root, bg="#f2f2f2", height=60)
        footer.pack(fill="x")

        tk.Button(footer, text="Remove Item", bg="#dc2626", fg="white",
                  font=("Arial", 12), width=15, command=self.remove_item).pack(side="left", padx=20)

        tk.Button(footer, text="Checkout", bg="#16a34a", fg="white",
                  font=("Arial", 12), width=15, command=self.checkout).pack(side="right", padx=20)

        tk.Button(footer, text="Scan Item", bg="#2563eb", fg="white",
                  font=("Arial", 12), width=15, command=self.scan_item).pack(pady=5)
        
    def remove_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self.update_total()

    def checkout(self): 
        messagebox.showinfo("Checkout", "Proceeding to checkout...")
        # Implement checkout logic here

    def scan_item(self):
        messagebox.showinfo("Scan Item", "Scanning item...")
        # Implement scan item logic here

    # ---------- COMMON FUNCTIONS ----------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    SmartCartApp(root)
    root.mainloop()
