# Tkinter Mini Apps Collection

A collection of beginner-friendly Python Tkinter applications designed for learning GUI development and basic application logic.

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-8.6-orange.svg)](https://docs.python.org/3/library/tkinter.html)


## Included Applications

### Personal Budget Tracker

Track income and expenses, view total balance, and manage transactions in a simple table-based interface.

Features:

* Add income and expense entries
* Automatic balance calculation
* Transaction history using Treeview


Code:
```python
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


```

Run:

```bash
python codes/budget_tracker.py
```

---

### Simple Password Manager (No Encryption)

A basic password manager that stores credentials in plain text for educational purposes only.

Features:

* Store website, username, and password
* View saved credentials
* Clear all entries

Warning: This app does not use encryption. Do not use for real passwords.

Code:

```python
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


```


Run:

```bash
python codes/password_manager.py
```

---

### Unit Converter

A simple utility for converting between common length and temperature units.

Supported conversions:

* Meters to Kilometers
* Kilometers to Meters
* Celsius to Fahrenheit
* Fahrenheit to Celsius
Code:

```python
import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Unit Converter")
root.geometry("350x300")
root.resizable(False, False)

def convert():
    try:
        value = float(value_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number")
        return

    conversion = convert_var.get()

    if conversion == "Meters to Kilometers":
        result = value / 1000
    elif conversion == "Kilometers to Meters":
        result = value * 1000
    elif conversion == "Celsius to Fahrenheit":
        result = (value * 9/5) + 32
    elif conversion == "Fahrenheit to Celsius":
        result = (value - 32) * 5/9

    result_label.config(text=f"Result: {result:.2f}")

tk.Label(root, text="Enter Value").pack(pady=5)
value_entry = tk.Entry(root)
value_entry.pack()

convert_var = tk.StringVar()
options = [
    "Meters to Kilometers",
    "Kilometers to Meters",
    "Celsius to Fahrenheit",
    "Fahrenheit to Celsius"
]
ttk.Combobox(root, textvariable=convert_var, values=options).pack(pady=10)

tk.Button(root, text="Convert", command=convert).pack()
result_label = tk.Label(root, text="Result:")
result_label.pack(pady=10)

root.mainloop()


```

Run:

```bash
python codes/unit_converter.py
```

---

### Random Password Generator

Generates random passwords using letters, numbers, and symbols.

Features:

* Custom password length
* One-click password generation

Code:

```python
import tkinter as tk
import random
import string

root = tk.Tk()
root.title("Random Password Generator")
root.geometry("400x250")
root.resizable(False, False)

def generate():
    try:
        length = int(length_entry.get())
    except ValueError:
        return

    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(length))
    output_entry.delete(0, tk.END)
    output_entry.insert(0, password)

tk.Label(root, text="Password Length").pack(pady=5)
length_entry = tk.Entry(root)
length_entry.pack()
length_entry.insert(0, "12")

tk.Button(root, text="Generate Password", command=generate).pack(pady=10)

output_entry = tk.Entry(root, width=40)
output_entry.pack(pady=5)

root.mainloop()


```

Run:

```bash
python codes/password_generator.py
```

---

### Flashcard Study Buddy

A flashcard-based study tool for memorization and quick review.

Features:

* Add question and answer flashcards
* Flip between question and answer
* Cycle through saved flashcards

Code:

```python
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Flashcard Study Buddy")
root.geometry("500x350")
root.resizable(False, False)

flashcards = []
index = 0
showing_answer = False

def add_card():
    q = question_entry.get()
    a = answer_entry.get()

    if q == "" or a == "":
        return

    flashcards.append((q, a))
    question_entry.delete(0, tk.END)
    answer_entry.delete(0, tk.END)
    messagebox.showinfo("Saved", "Flashcard added")

def show_card():
    global showing_answer
    if not flashcards:
        card_label.config(text="No flashcards yet")
        return

    card_label.config(text=flashcards[index][0])
    showing_answer = False

def flip():
    global showing_answer
    if not flashcards:
        return

    if showing_answer:
        card_label.config(text=flashcards[index][0])
    else:
        card_label.config(text=flashcards[index][1])

    showing_answer = not showing_answer

def next_card():
    global index
    if flashcards:
        index = (index + 1) % len(flashcards)
        show_card()

tk.Label(root, text="Question").pack()
question_entry = tk.Entry(root, width=40)
question_entry.pack()

tk.Label(root, text="Answer").pack()
answer_entry = tk.Entry(root, width=40)
answer_entry.pack()

tk.Button(root, text="Add Flashcard", command=add_card).pack(pady=5)

card_label = tk.Label(root, text="Flashcard Area", font=("Arial", 14), wraplength=400)
card_label.pack(pady=20)

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Flip", width=10, command=flip).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Next", width=10, command=next_card).grid(row=0, column=1, padx=5)

root.mainloop()


```

Run:

```bash
python codes/flashcard_app.py
```


---

## Requirements

* Python 3.x
* Tkinter (included with standard Python installation)

## Getting Started

Clone the repository:

```bash
git clone https://github.com/juswa005/Python-Basic-Apps-with-GUI-using-tkinter-library.git
```

Change into the project directory:

```bash
cd Python-Basic-Apps-with-GUI-using-tkinter-library
```

Run any application:

```bash
python codes/filename.py
```

## Purpose

This repository is intended for:

* Practicing Python Tkinter
* Learning event-driven programming

## License

This project is licensed under the MIT License.


---

## Author
Amiel Josh Basug
