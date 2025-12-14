import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Simple Password Manager")
root.geometry("600x400")
root.resizable(False, False)

passwords = []

def add_password():
    site = site_entry.get()
    user = user_entry.get()
    pwd = pass_entry.get()

    if site == "" or user == "" or pwd == "":
        messagebox.showwarning("Input Error", "All fields are required")
        return

    passwords.append((site, user, pwd))
    tree.insert("", tk.END, values=(site, user, pwd))

    site_entry.delete(0, tk.END)
    user_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)

def clear_all():
    if not passwords:
        return

    if messagebox.askyesno("Confirm", "Delete all saved passwords?"):
        passwords.clear()
        for item in tree.get_children():
            tree.delete(item)

input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(fill="x")

tk.Label(input_frame, text="Website").grid(row=0, column=0, padx=5, pady=5)
site_entry = tk.Entry(input_frame, width=25)
site_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Username").grid(row=1, column=0, padx=5, pady=5)
user_entry = tk.Entry(input_frame, width=25)
user_entry.grid(row=1, column=1, padx=5)

tk.Label(input_frame, text="Password").grid(row=2, column=0, padx=5, pady=5)
pass_entry = tk.Entry(input_frame, width=25)
pass_entry.grid(row=2, column=1, padx=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Save", width=12, command=add_password).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Clear All", width=12, command=clear_all).grid(row=0, column=1, padx=5)

columns = ("Website", "Username", "Password")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()

