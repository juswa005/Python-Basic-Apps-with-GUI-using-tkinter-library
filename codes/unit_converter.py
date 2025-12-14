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

