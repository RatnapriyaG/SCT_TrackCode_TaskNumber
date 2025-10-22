import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import random
import os

# ---------- Core Encryption / Decryption Logic ----------
def encrypt_image(image_path, key):
    img = Image.open(image_path)
    img_array = np.array(img)

    random.seed(key)
    flat_pixels = img_array.flatten()
    indices = np.arange(len(flat_pixels))
    random.shuffle(indices)
    shuffled_pixels = flat_pixels[indices]

    # FIX: prevent overflow using uint16
    encrypted_pixels = (shuffled_pixels.astype(np.uint16) + key) % 256
    encrypted_array = encrypted_pixels.reshape(img_array.shape).astype(np.uint8)

    encrypted_img = Image.fromarray(encrypted_array)
    output_path = os.path.splitext(image_path)[0] + "_encrypted.png"
    encrypted_img.save(output_path)
    return output_path


def decrypt_image(image_path, key):
    img = Image.open(image_path)
    img_array = np.array(img)

    flat_pixels = img_array.flatten()
    # FIX: prevent overflow using uint16
    decrypted_pixels = (flat_pixels.astype(np.uint16) - key) % 256

    random.seed(key)
    indices = np.arange(len(decrypted_pixels))
    random.shuffle(indices)

    reversed_pixels = np.zeros_like(decrypted_pixels)
    reversed_pixels[indices] = decrypted_pixels
    decrypted_array = reversed_pixels.reshape(img_array.shape).astype(np.uint8)

    decrypted_img = Image.fromarray(decrypted_array)
    output_path = os.path.splitext(image_path)[0] + "_decrypted.png"
    decrypted_img.save(output_path)
    return output_path


# ---------- GUI ----------
class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Image Encryption Tool with Preview")
        self.root.geometry("600x600")
        self.root.config(bg="#1e1e2f")

        self.image_path = None
        self.image_label = None
        self.tk_image = None  # store reference to avoid garbage collection

        tk.Label(root, text="Simple Image Encryption Tool", fg="white", bg="#1e1e2f",
                 font=("Arial", 18, "bold")).pack(pady=10)

        tk.Button(root, text="Select Image", command=self.load_image,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=10)

        self.path_label = tk.Label(root, text="No image selected", bg="#1e1e2f", fg="gray")
        self.path_label.pack()

        # Image preview area
        self.preview_frame = tk.Frame(root, bg="#1e1e2f")
        self.preview_frame.pack(pady=10)
        self.image_label = tk.Label(self.preview_frame, bg="#1e1e2f")
        self.image_label.pack()

        tk.Label(root, text="Enter Encryption Key:", bg="#1e1e2f", fg="white").pack(pady=5)
        self.key_entry = tk.Entry(root, font=("Arial", 12), justify="center")
        self.key_entry.pack(pady=5)

        btn_frame = tk.Frame(root, bg="#1e1e2f")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Encrypt", command=self.encrypt, bg="#0078D7",
                  fg="white", font=("Arial", 12, "bold"), width=10).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Decrypt", command=self.decrypt, bg="#E91E63",
                  fg="white", font=("Arial", 12, "bold"), width=10).grid(row=0, column=1, padx=10)

        tk.Button(root, text="Exit", command=root.quit, bg="#555", fg="white",
                  font=("Arial", 10, "bold"), width=15).pack(pady=10)

    # ---------- Helper Methods ----------
    def load_image(self):
        self.image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if self.image_path:
            self.path_label.config(text=f"Loaded: {os.path.basename(self.image_path)}", fg="#00FFAA")
            self.show_image(self.image_path)

    def show_image(self, path):
        """Display image preview (auto-resized)."""
        try:
            img = Image.open(path)
            img.thumbnail((400, 300))
            self.tk_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image preview:\n{e}")

    def get_key(self):
        try:
            key = int(self.key_entry.get())
            if key < 0:
                messagebox.showerror("Invalid Input", "Key must be a positive number!")
                return None
            return key
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric key!")
            return None

    def encrypt(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
        key = self.get_key()
        if key is None:
            return
        output_path = encrypt_image(self.image_path, key)
        self.show_image(output_path)
        messagebox.showinfo("Success", f"✅ Image encrypted and saved as:\n{output_path}")

    def decrypt(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
        key = self.get_key()
        if key is None:
            return
        output_path = decrypt_image(self.image_path, key)
        self.show_image(output_path)
        messagebox.showinfo("Success", f"🔓 Image decrypted and saved as:\n{output_path}")


# ---------- Run App ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
