import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
import json
import os

# ================= CONFIG =================
ctk.set_appearance_mode("light")  # Light mode
ctk.set_default_color_theme("blue")

DATA_FILE = "passwords.json"
MASTER_HASH = hashlib.sha256("admin123".encode()).hexdigest()
passwords = []

FONT = ("Arial", 14)  # Updated font and bigger size

# ================= LOGIN WINDOW =================
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager Login")
        self.geometry("380x220")
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text="Password Manager",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=20)

        self.entry = ctk.CTkEntry(self, show="*", width=250, font=FONT)
        self.entry.pack(pady=10)
        self.entry.focus()

        ctk.CTkButton(
            self,
            text="Unlock",
            command=self.verify,
            width=150,
            font=FONT
        ).pack(pady=10)

    def verify(self):
        entered = self.entry.get()
        hashed = hashlib.sha256(entered.encode()).hexdigest()
        if hashed == MASTER_HASH:
            self.withdraw()
            AppWindow(self)
        else:
            messagebox.showerror("Access Denied", "Incorrect master password")


# ================= MAIN APP =================
class AppWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Password Manager")
        self.geometry("950x650")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", parent.destroy)

        self.create_ui()
        self.load_data()

    # ---------- UI ----------
    def create_ui(self):
        self.main = ctk.CTkFrame(self)
        self.main.pack(fill="both", expand=True, padx=15, pady=15)

        # Input section
        input_frame = ctk.CTkFrame(self.main)
        input_frame.pack(fill="x", pady=10)

        self.site = ctk.CTkEntry(input_frame, placeholder_text="Website", font=FONT)
        self.site.grid(row=0, column=0, padx=5, pady=5)

        self.user = ctk.CTkEntry(input_frame, placeholder_text="Username", font=FONT)
        self.user.grid(row=0, column=1, padx=5, pady=5)

        self.pwd = ctk.CTkEntry(input_frame, placeholder_text="Password", show="*", font=FONT)
        self.pwd.grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkButton(input_frame, text="Save", command=self.add_password, font=FONT)\
            .grid(row=0, column=3, padx=5, pady=5)

        # Search
        self.search = ctk.CTkEntry(self.main, placeholder_text="Search website", font=FONT)
        self.search.pack(pady=5)

        ctk.CTkButton(self.main, text="Search", command=self.search_password, font=FONT)\
            .pack(pady=5)

        # Table
        self.table_frame = ctk.CTkFrame(self.main)
        self.table_frame.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("Site", "User", "Password"),
            show="headings",
            height=12
        )

        for col in ("Site", "User", "Password"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=300)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.reveal_password)

        # Buttons
        btns = ctk.CTkFrame(self.main)
        btns.pack(pady=10)

        ctk.CTkButton(btns, text="Copy Password", command=self.copy_password, font=FONT)\
            .grid(row=0, column=0, padx=10)

        ctk.CTkButton(btns, text="Delete", command=self.delete_selected, font=FONT)\
            .grid(row=0, column=1, padx=10)

    # ---------- DATA ----------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                for p in json.load(f):
                    passwords.append(p)
                    self.tree.insert(
                        "",
                        "end",
                        values=(p["site"], p["user"], "*" * len(p["pwd"]))
                    )

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(passwords, f, indent=4)

    # ---------- ACTIONS ----------
    def add_password(self):
        s, u, p = self.site.get(), self.user.get(), self.pwd.get()
        if not s or not u or not p:
            messagebox.showwarning("Error", "All fields required")
            return

        passwords.append({"site": s, "user": u, "pwd": p})
        self.tree.insert("", "end", values=(s, u, "*" * len(p)))
        self.save_data()

        self.site.delete(0, "end")
        self.user.delete(0, "end")
        self.pwd.delete(0, "end")

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel)
        self.tree.delete(sel)
        passwords.pop(idx)
        self.save_data()

    def copy_password(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel)
        self.clipboard_clear()
        self.clipboard_append(passwords[idx]["pwd"])
        messagebox.showinfo("Copied", "Password copied to clipboard")

    def search_password(self):
        q = self.search.get().lower()
        self.tree.delete(*self.tree.get_children())
        for p in passwords:
            if q in p["site"].lower():
                self.tree.insert(
                    "",
                    "end",
                    values=(p["site"], p["user"], "*" * len(p["pwd"]))
                )

    # ---------- SECURITY ----------
    def reveal_password(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel)
        real_pwd = passwords[idx]["pwd"]

        # Popup
        popup = ctk.CTkToplevel(self)
        popup.title("Verify Master Password")
        popup.geometry("350x180")
        popup.resizable(False, False)
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="Enter Master Password", font=FONT).pack(pady=20)

        entry = ctk.CTkEntry(popup, show="*", width=250, font=FONT)
        entry.pack(pady=5)
        entry.focus()

        def verify():
            hashed = hashlib.sha256(entry.get().encode()).hexdigest()
            if hashed == MASTER_HASH:
                self.tree.item(
                    sel,
                    values=(passwords[idx]["site"], passwords[idx]["user"], real_pwd)
                )
                popup.destroy()
            else:
                messagebox.showerror("Denied", "Incorrect master password")

        ctk.CTkButton(popup, text="Verify", command=verify, font=FONT, width=150)\
            .pack(pady=20)


# ================= RUN =================
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
