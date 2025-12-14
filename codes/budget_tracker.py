import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Personal Budget Tracker")
root.geometry("700x450")
root.resizable(False, False)

transactions = []
def add_transaction():
    desc = desc_entry.get()
    amount = amount_entry.get()
    t_type = type_var.get()

    if desc == "" or amount == "":
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Amount", "Amount must be a number")
        return

    transactions.append((desc, t_type, amount))
    tree.insert("", tk.END, values=(desc, t_type, f"{amount:.2f}"))

    desc_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    update_summary()

def update_summary():
    income = sum(a for d, t, a in transactions if t == "Income")
    expense = sum(a for d, t, a in transactions if t == "Expense")
    balance = income - expense

    income_label.config(text=f"₱ {income:.2f}")
    expense_label.config(text=f"₱ {expense:.2f}")
    balance_label.config(text=f"₱ {balance:.2f}")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="x")

tk.Label(frame, text="Description").grid(row=0, column=0, padx=5)
desc_entry = tk.Entry(frame, width=20)
desc_entry.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Amount").grid(row=0, column=2, padx=5)
amount_entry = tk.Entry(frame, width=15)
amount_entry.grid(row=0, column=3, padx=5)

type_var = tk.StringVar(value="Expense")
type_menu = ttk.Combobox(frame, textvariable=type_var, values=["Income", "Expense"], width=10)
type_menu.grid(row=0, column=4, padx=5)

add_btn = tk.Button(frame, text="Add", command=add_transaction)
add_btn.grid(row=0, column=5, padx=5)

columns = ("Description", "Type", "Amount")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(pady=10, fill="x", padx=10)

summary = tk.Frame(root)
summary.pack(pady=10)

tk.Label(summary, text="Total Income:").grid(row=0, column=0, padx=10)
income_label = tk.Label(summary, text="Php 0.00", fg="green")
income_label.grid(row=0, column=1)

tk.Label(summary, text="Total Expense:").grid(row=0, column=2, padx=10)
expense_label = tk.Label(summary, text="Php 0.00", fg="red")
expense_label.grid(row=0, column=3)

tk.Label(summary, text="Balance:").grid(row=0, column=4, padx=10)
balance_label = tk.Label(summary, text="Php 0.00", fg="blue")
balance_label.grid(row=0, column=5)

root.mainloop()

