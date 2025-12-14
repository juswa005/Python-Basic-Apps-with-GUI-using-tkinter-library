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

