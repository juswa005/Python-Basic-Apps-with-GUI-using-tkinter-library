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

