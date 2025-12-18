import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
import json
import os
import secrets
import string

# ---------- CONFIG ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

DATA_FILE   = "passwords.json"
MASTER_HASH = hashlib.sha256("admin123".encode()).hexdigest()
FONT        = ("Arial", 14)

# ---------- UTILS ----------
def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# ---------- LOGIN ----------
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager – Login")
        self.geometry("380x220")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Password Manager", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)
        self.entry = ctk.CTkEntry(self, show="*", width=250, font=FONT)
        self.entry.pack(pady=10)
        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.verify())

        ctk.CTkButton(self, text="Unlock", command=self.verify, width=150, font=FONT).pack(pady=10)

    def verify(self):
        if hashlib.sha256(self.entry.get().encode()).hexdigest() == MASTER_HASH:
            self.withdraw()
            AppWindow(self)
        else:
            messagebox.showerror("Access Denied", "Incorrect master password")

# ---------- MAIN APP ----------
class AppWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Password Manager")
        self.geometry("1000x700")
        self.minsize(900, 600)
        self.protocol("WM_DELETE_WINDOW", parent.destroy)

        self.passwords = []          # live list
        self.filtered   = []         # what is currently shown
        self._build_ui()
        self._load_data()

    # ---------- UI ----------
    def _build_ui(self):
        # ---- top input bar ----
        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=15, pady=(15,5))

        self.site_ent = ctk.CTkEntry(top, placeholder_text="Website",   width=240, font=FONT)
        self.user_ent = ctk.CTkEntry(top, placeholder_text="Username",  width=240, font=FONT)
        self.pwd_ent  = ctk.CTkEntry(top, placeholder_text="Password",  width=240, font=FONT, show="*")
        self.show_var = ctk.BooleanVar(value=False)

        self.site_ent.grid(row=0, column=0, padx=5)
        self.user_ent.grid(row=0, column=1, padx=5)
        self.pwd_ent.grid( row=0, column=2, padx=5)

        ctk.CTkButton(top, text="👁", width=30, command=self._toggle_show).grid(row=0, column=3, padx=(0,5))
        ctk.CTkButton(top, text="Save", width=80,  command=self._add_password).grid(row=0, column=4, padx=5)
        ctk.CTkButton(top, text="Generate", width=80, command=self._generate_and_fill).grid(row=0, column=5, padx=5)

        for w in (self.site_ent, self.user_ent, self.pwd_ent):
            w.bind("<Return>", lambda e: self._add_password())

        # ---- search bar ----
        search_bar = ctk.CTkFrame(self)
        search_bar.pack(fill="x", padx=15, pady=5)

        self.search_ent = ctk.CTkEntry(search_bar, placeholder_text="Search website …", font=FONT)
        self.search_ent.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.search_ent.bind("<KeyRelease>", lambda e: self._search())

        ctk.CTkButton(search_bar, text="Clear", width=60, command=self._clear_search).pack(side="right")

        # ---- scrollable table ----
        container = ctk.CTkScrollableFrame(self)
        container.pack(fill="both", expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(container, columns=("Site","User","Password"), show="headings", height=18)
        self.tree.pack(fill="both", expand=True)
        for col, w in zip(("Site","User","Password"), (350,300,300)):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w", width=w)

        self.tree.bind("<Double-1>", self._reveal_password)
        self.tree.bind("<Button-3>", self._context_menu)

        # ---- bottom buttons ----
        bot = ctk.CTkFrame(self)
        bot.pack(pady=10)

        ctk.CTkButton(bot, text="Copy Password", command=self._copy_password).grid(row=0, column=0, padx=10)
        ctk.CTkButton(bot, text="Delete",       command=self._delete_selected).grid(row=0, column=1, padx=10)

        # ---- status bar ----
        self.status = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.status.pack(pady=(0,10))

    # ---------- DATA ----------
    def _load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE) as f:
                self.passwords = json.load(f)
        self._refresh_tree()

    def _save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.passwords, f, indent=2)

    # ---------- TREE ----------
    def _refresh_tree(self, data_source=None):
        data_source = data_source or self.passwords
        self.filtered = data_source
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in data_source:
            self.tree.insert("", "end", values=(p["site"], p["user"], "•"*len(p["pwd"])))

    # ---------- ACTIONS ----------
    def _add_password(self):
        s, u, p = self.site_ent.get(), self.user_ent.get(), self.pwd_ent.get()
        if not all((s,u,p)):
            messagebox.showwarning("Input required", "All fields are required")
            return
        self.passwords.append({"site":s, "user":u, "pwd":p})
        self._save_data()
        self._refresh_tree()
        for w in (self.site_ent, self.user_ent, self.pwd_ent):
            w.delete(0, "end")
        self._status("Saved.")

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        if not messagebox.askyesno("Confirm", "Delete this entry?"):
            return
        self.passwords.pop(idx)
        self._save_data()
        self._refresh_tree()
        self._status("Deleted.")

    def _copy_password(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = self.tree.index(sel[0])
        real = self.filtered[idx]["pwd"]
        self.clipboard_clear()
        self.clipboard_append(real)
        self._status("Password copied.")

    def _generate_and_fill(self):
        pw = generate_password()
        self.pwd_ent.delete(0, "end")
        self.pwd_ent.insert(0, pw)
        self.clipboard_clear()
        self.clipboard_append(pw)
        self._status("Generated & copied.")

    def _toggle_show(self):
        self.show_var.set(not self.show_var.get())
        self.pwd_ent.configure(show="" if self.show_var.get() else "*")

    def _search(self):
        q = self.search_ent.get().lower()
        res = [p for p in self.passwords if q in p["site"].lower()]
        self._refresh_tree(res)

    def _clear_search(self):
        self.search_ent.delete(0, "end")
        self._refresh_tree()

    def _status(self, msg):
        self.status.configure(text=msg)
        self.after(2000, lambda: self.status.configure(text=""))

    # ---------- SECURITY ----------
    def _reveal_password(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        idx   = self.tree.index(sel[0])
        entry = self.filtered[idx]

        popup = ctk.CTkToplevel(self)
        popup.title("Verify Master Password")
        popup.geometry("350x180")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="Enter master password to reveal:", font=FONT).pack(pady=20)
        ent = ctk.CTkEntry(popup, show="*", width=250, font=FONT)
        ent.pack(pady=5)
        ent.focus()
        ent.bind("<Return>", lambda e: verify())

        def verify():
            if hashlib.sha256(ent.get().encode()).hexdigest() == MASTER_HASH:
                self.tree.item(sel[0], values=(entry["site"], entry["user"], entry["pwd"]))
                popup.destroy()
            else:
                messagebox.showerror("Denied", "Incorrect master password", parent=popup)

        ctk.CTkButton(popup, text="Verify", command=verify, width=150, font=FONT).pack(pady=20)

    # ---------- CONTEXT MENU ----------
    def _context_menu(self, event):
        iid = self.tree.identify_row(event.y)
        if not iid:
            return
        self.tree.selection_set(iid)
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Reveal",   command=self._reveal_password)
        menu.add_command(label="Copy",     command=self._copy_password)
        menu.add_separator()
        menu.add_command(label="Delete",   command=self._delete_selected)
        menu.tk_popup(event.x_root, event.y_root)


# ---------- RUN ----------
if __name__ == "__main__":
    LoginWindow().mainloop()