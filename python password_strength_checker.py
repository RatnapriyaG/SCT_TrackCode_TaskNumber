import tkinter as tk
from tkinter import ttk
import re

# ----------------- Password Strength Function -----------------
def check_strength(event=None):
    password = password_entry.get()
    score = 0

    # Criteria
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[@$!%*?&#^()_\-+=]", password):
        score += 1

    # Strength details
    strength = {
        0: ("Very Weak", "red"),
        1: ("Weak", "orange red"),
        2: ("Fair", "orange"),
        3: ("Strong", "yellow green"),
        4: ("Very Strong", "green"),
        5: ("Excellent", "dark green")
    }

    label, color = strength[score]
    result_label.config(text=f"Strength: {label}", fg=color)
    progress["value"] = score * 20
    progress.configure(style=f"{color}.Horizontal.TProgressbar")

# ----------------- Toggle Password Visibility -----------------
def toggle_password():
    if password_entry.cget('show') == '':
        password_entry.config(show='*')
        toggle_btn.config(text='👁️')
    else:
        password_entry.config(show='')
        toggle_btn.config(text='🙈')

# ----------------- UI Setup -----------------
root = tk.Tk()
root.title("🔐 Advanced Password Strength Checker")
root.geometry("420x300")
root.resizable(False, False)
root.configure(bg="#121212")

style = ttk.Style()
style.theme_use("clam")

# Progress bar color styles
for color in ["red", "orange red", "orange", "yellow green", "green", "dark green"]:
    style.configure(f"{color}.Horizontal.TProgressbar", troughcolor="#222", background=color, thickness=15)

# Title
title = tk.Label(root, text="🔒 Password Strength Analyzer", font=("Segoe UI", 14, "bold"), bg="#121212", fg="white")
title.pack(pady=15)

# Password Entry Frame
frame = tk.Frame(root, bg="#121212")
frame.pack(pady=10)

password_entry = tk.Entry(frame, show="*", font=("Segoe UI", 12), width=25, bd=2, relief="solid")
password_entry.grid(row=0, column=0, padx=5)
password_entry.bind("<KeyRelease>", check_strength)

toggle_btn = tk.Button(frame, text="👁️", font=("Segoe UI", 10), command=toggle_password, bg="#333", fg="white", bd=0)
toggle_btn.grid(row=0, column=1, padx=5)

# Progress Bar
progress = ttk.Progressbar(root, length=300, mode="determinate", maximum=100)
progress.pack(pady=15)

# Result Label
result_label = tk.Label(root, text="Start typing a password...", font=("Segoe UI", 12, "bold"), bg="#121212", fg="white")
result_label.pack(pady=10)



root.mainloop()
