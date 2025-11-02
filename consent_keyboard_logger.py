"""
consent_keyboard_logger.py

Safe, consent-based keyboard-event logger for educational/debugging use.
It ONLY listens to key events while its window is focused and only logs
when the user explicitly checks the Consent box. The user must click
'Save Log' to write logs to disk.

Do NOT use this to monitor others without explicit informed consent.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

class ConsentLoggerApp:
    def __init__(self, root):
        self.root = root
        root.title("Consent Keyboard Logger (Safe Demo)")
        root.geometry("700x500")
        root.configure(bg="#f4f6f8")

        # State
        self.logging_enabled = tk.BooleanVar(value=False)
        self.logs = []

        # Header
        header = tk.Label(root, text="Consent Keyboard Logger", font=("Segoe UI", 18, "bold"), bg="#f4f6f8")
        header.pack(pady=(12, 6))

        subtitle = tk.Label(root, text="This program records keystrokes only while its window is focused and when you explicitly allow it.",
                            font=("Segoe UI", 10), bg="#f4f6f8")
        subtitle.pack(pady=(0, 12))

        # Controls frame
        controls = tk.Frame(root, bg="#f4f6f8")
        controls.pack(fill="x", padx=16)

        consent_chk = tk.Checkbutton(controls, text="I consent to record keystrokes in this window",
                                     variable=self.logging_enabled, bg="#f4f6f8", font=("Segoe UI", 10, "bold"),
                                     command=self.on_consent_change)
        consent_chk.grid(row=0, column=0, sticky="w")

        self.status_label = tk.Label(controls, text="Not recording", bg="#f4f6f8", font=("Segoe UI", 10))
        self.status_label.grid(row=0, column=1, padx=12, sticky="w")

        save_btn = ttk.Button(controls, text="Save Log", command=self.save_log)
        save_btn.grid(row=0, column=2, padx=8)
        clear_btn = ttk.Button(controls, text="Clear Log", command=self.clear_log)
        clear_btn.grid(row=0, column=3, padx=8)

        # Logging area
        area_frame = tk.Frame(root)
        area_frame.pack(fill="both", expand=True, padx=16, pady=(12,16))

        self.log_text = tk.Text(area_frame, wrap="none", state="disabled", font=("Consolas", 11))
        self.log_text.pack(side="left", fill="both", expand=True)

        # Scrollbars
        yscroll = ttk.Scrollbar(area_frame, orient="vertical", command=self.log_text.yview)
        yscroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=yscroll.set)

        # Bind key events when the window has focus
        root.bind("<KeyPress>", self.on_key_press)
        root.bind("<KeyRelease>", self.on_key_release)
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Info footer
        footer = tk.Label(root, text="Only records while this window is focused. Logs stored in memory until you save.",
                          font=("Segoe UI", 9), bg="#f4f6f8")
        footer.pack(side="bottom", pady=6)

    def on_consent_change(self):
        if self.logging_enabled.get():
            self.status_label.config(text="Recording (consent given) — window must be focused", fg="green")
        else:
            self.status_label.config(text="Not recording", fg="black")

    def on_key_press(self, event):
        # Only record when consent is given and window is focused
        if not self.logging_enabled.get():
            return
        # event.keysym is human-readable, event.char may be empty for special keys
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        entry = f"{timestamp}  PRESS   key={event.keysym!r}  char={event.char!r}\n"
        self.append_log(entry)

    def on_key_release(self, event):
        if not self.logging_enabled.get():
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        entry = f"{timestamp}  RELEASE key={event.keysym!r}  char={event.char!r}\n"
        self.append_log(entry)

    def append_log(self, text):
        # store in memory
        self.logs.append(text)
        # append to the text widget
        self.log_text.config(state="normal")
        self.log_text.insert("end", text)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def save_log(self):
        if not self.logs:
            messagebox.showinfo("Save Log", "No log entries to save.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save log to file"
        )
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(self.logs)
            messagebox.showinfo("Save Log", f"Log saved to: {file_path}")
        except Exception as e:
            messagebox.showerror("Save Log", f"Failed to save log: {e}")

    def clear_log(self):
        if not self.logs:
            return
        if not messagebox.askyesno("Clear Log", "Clear the current log from memory and display?"):
            return
        self.logs.clear()
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    def on_close(self):
        if self.logs:
            if not messagebox.askyesno("Exit", "There are unsaved log entries. Exit without saving?"):
                return
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ConsentLoggerApp(root)
    root.mainloop()
