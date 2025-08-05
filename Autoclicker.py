import tkinter as tk
import threading
import pyautogui
import time
import random
import keyboard

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("370x260")
        self.root.resizable(False, False)

        self.running = False
        self.dark_mode = True  # start in dark mode

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(fill='both', expand=True)

        self.min_label = tk.Label(self.frame, text="Min Delay (ms):")
        self.min_label.grid(row=0, column=0, sticky="w")
        self.min_delay = tk.Entry(self.frame, width=10)
        self.min_delay.grid(row=0, column=1, padx=10, pady=5)

        self.max_label = tk.Label(self.frame, text="Max Delay (ms):")
        self.max_label.grid(row=1, column=0, sticky="w")
        self.max_delay = tk.Entry(self.frame, width=10)
        self.max_delay.grid(row=1, column=1, padx=10, pady=5)

        self.toggle_button = tk.Button(self.frame, text="Start Clicking", width=20, command=self.toggle_clicking)
        self.toggle_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.status_label = tk.Label(self.frame, text="Status: Idle", fg="blue")
        self.status_label.grid(row=3, column=0, columnspan=2)

        self.theme_button = tk.Button(self.frame, text="Switch to Light Mode", command=self.toggle_theme)
        self.theme_button.grid(row=4, column=0, columnspan=2, pady=10)

        keyboard.add_hotkey('f6', self.toggle_clicking)

        self.apply_theme()

    def toggle_clicking(self):
        if not self.running:
            try:
                min_d = int(self.min_delay.get())
                max_d = int(self.max_delay.get())
                if min_d < 0 or max_d < min_d:
                    raise ValueError
            except ValueError:
                self.status_label.config(text="Invalid delay values!", fg="red")
                return

            self.running = True
            self.toggle_button.config(text="Stop Clicking")
            self.status_label.config(text="Status: Clicking...", fg="green")
            threading.Thread(target=self.click_loop, daemon=True).start()
        else:
            self.running = False
            self.toggle_button.config(text="Start Clicking")
            self.status_label.config(text="Status: Idle", fg="blue")

    def click_loop(self):
        while self.running:
            try:
                pyautogui.click()
                delay = random.uniform(int(self.min_delay.get()), int(self.max_delay.get())) / 1000
                time.sleep(delay)
            except:
                break

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            bg = "#1e1e1e"
            fg = "#ffffff"
            entry_bg = "#2e2e2e"
            self.theme_button.config(text="Switch to Light Mode")
        else:
            bg = "#f0f0f0"
            fg = "#000000"
            entry_bg = "#ffffff"
            self.theme_button.config(text="Switch to Dark Mode")

        self.root.config(bg=bg)
        self.frame.config(bg=bg)

        widgets = [
            self.min_label, self.max_label,
            self.status_label, self.toggle_button,
            self.theme_button
        ]

        for widget in widgets:
            widget.config(bg=bg, fg=fg)

        self.min_delay.config(bg=entry_bg, fg=fg, insertbackground=fg)
        self.max_delay.config(bg=entry_bg, fg=fg, insertbackground=fg)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
