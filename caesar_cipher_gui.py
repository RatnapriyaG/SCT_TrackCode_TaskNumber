import tkinter as tk
from tkinter import ttk, messagebox

# Caesar Cipher Algorithm
def caesar_cipher(text, shift, mode):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            if mode == "Encrypt":
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result

# Function to process the text
def process_text():
    text = input_text.get("1.0", tk.END).strip()
    shift_val = shift_entry.get()
    mode = mode_choice.get()

    if not shift_val.lstrip('-').isdigit():
        messagebox.showerror("Invalid Input", "Shift value must be a number!")
        return

    shift = int(shift_val)
    if text == "":
        messagebox.showwarning("Empty Field", "Please enter a message first!")
        return

    result = caesar_cipher(text, shift, mode)
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state='disabled')

    # Update summary
    summary_label.config(text=f"✅ {mode}ed successfully | Characters: {len(result)}")

# Function to clear all fields
def clear_fields():
    input_text.delete("1.0", tk.END)
    shift_entry.delete(0, tk.END)
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.config(state='disabled')
    summary_label.config(text="")

# Create main window
root = tk.Tk()
root.title("Caesar Cipher - Light Mode")
root.geometry("600x500")
root.config(bg="white")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
                background="#1E88E5",
                foreground="white",
                font=("Poppins", 11, "bold"),
                borderwidth=0,
                padding=6)
style.map("TButton", background=[("active", "#1565C0")])

# Title
title_label = tk.Label(root, text="🔐 Caesar Cipher Encryption Tool",
                       font=("Poppins", 18, "bold"), fg="#1565C0", bg="white")
title_label.pack(pady=15)

# Mode selection frame
mode_frame = tk.Frame(root, bg="white")
mode_frame.pack(pady=5)

tk.Label(mode_frame, text="Select Mode:", bg="white", fg="black", font=("Poppins", 12)).grid(row=0, column=0)
mode_choice = ttk.Combobox(mode_frame, values=["Encrypt", "Decrypt"], state="readonly", width=10, font=("Poppins", 11))
mode_choice.grid(row=0, column=1, padx=10)
mode_choice.set("Encrypt")

# Shift Entry
tk.Label(mode_frame, text="Shift Value:", bg="white", fg="black", font=("Poppins", 12)).grid(row=0, column=2)
shift_entry = tk.Entry(mode_frame, width=6, font=("Consolas", 12))
shift_entry.grid(row=0, column=3, padx=5)

# Input Area
input_label = tk.Label(root, text="Enter Message:", fg="#0D47A1", bg="white", font=("Poppins", 12, "bold"))
input_label.pack()
input_text = tk.Text(root, height=5, width=60, font=("Consolas", 11),
                     bg="#f5f5f5", fg="black", insertbackground="black")
input_text.pack(pady=5)

# Buttons Frame
btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=10)

encrypt_btn = ttk.Button(btn_frame, text="Process", command=process_text)
encrypt_btn.grid(row=0, column=0, padx=10)

clear_btn = ttk.Button(btn_frame, text="Clear", command=clear_fields)
clear_btn.grid(row=0, column=1, padx=10)

# Output Area
output_label = tk.Label(root, text="Result:", fg="#0D47A1", bg="white", font=("Poppins", 12, "bold"))
output_label.pack()
output_text = tk.Text(root, height=5, width=60, font=("Consolas", 11),
                      bg="#f5f5f5", fg="green", state='disabled')
output_text.pack(pady=5)

# Summary Label
summary_label = tk.Label(root, text="", fg="#1565C0", bg="white", font=("Poppins", 11, "italic"))
summary_label.pack(pady=10)

# Footer
footer = tk.Label(root, text="Developed by Ashish Mohanty © 2025", bg="white", fg="gray", font=("Poppins", 9, "italic"))
footer.pack(side="bottom", pady=5)

# Run app
root.mainloop()
