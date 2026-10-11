
import tkinter as tk
from tkinter import messagebox
import time
import winsound

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Clock & Timer")
        self.root.geometry("420x460")
        self.root.resizable(False, False)
        self.root.configure(bg="#101827")

        self.remaining = 0
        self.running = False
        self.paused = False
        self.after_id = None
        self.end_time = 0

        tk.Label(
            root,
            text="COUNTDOWN TIMER",
            font=("Arial", 20, "bold"),
            bg="#101827",
            fg="#60A5FA"
        ).pack(pady=20)

        tk.Label(
            root,
            text="Set your time",
            font=("Arial", 12),
            bg="#101827",
            fg="white"
        ).pack()

        inputs = tk.Frame(root, bg="#101827")
        inputs.pack(pady=15)

        self.hours = tk.Entry(
            inputs, width=5, font=("Arial", 16), justify="center"
        )
        self.minutes = tk.Entry(
            inputs, width=5, font=("Arial", 16), justify="center"
        )
        self.seconds = tk.Entry(
            inputs, width=5, font=("Arial", 16), justify="center"
        )

        for i, (entry, label) in enumerate([
            (self.hours, "Hours"),
            (self.minutes, "Minutes"),
            (self.seconds, "Seconds")
        ]):
            entry.grid(row=0, column=i, padx=7)
            entry.insert(0, "00")
            tk.Label(
                inputs, text=label,
                bg="#101827", fg="#CBD5E1"
            ).grid(row=1, column=i, pady=5)

        self.display = tk.Label(
            root,
            text="00:00:00",
            font=("Consolas", 36, "bold"),
            bg="#101827",
            fg="#34D399"
        )
        self.display.pack(pady=20)

        self.status = tk.Label(
            root,
            text="Ready to start",
            font=("Arial", 11),
            bg="#101827",
            fg="white"
        )
        self.status.pack(pady=5)

        buttons = tk.Frame(root, bg="#101827")
        buttons.pack(pady=20)

        tk.Button(
            buttons, text="START",
            command=self.start,
            bg="#16A34A", fg="white",
            font=("Arial", 11, "bold"),
            width=9
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            buttons, text="PAUSE",
            command=self.pause,
            bg="#D97706", fg="white",
            font=("Arial", 11, "bold"),
            width=9
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            buttons, text="RESET",
            command=self.reset,
            bg="#DC2626", fg="white",
            font=("Arial", 11, "bold"),
            width=9
        ).grid(row=0, column=2, padx=5)

    def start(self):
        if self.running:
            return

        if not self.paused:
            try:
                h = int(self.hours.get())
                m = int(self.minutes.get())
                s = int(self.seconds.get())

                if h < 0 or not 0 <= m <= 59 or not 0 <= s <= 59:
                    raise ValueError

                self.remaining = h * 3600 + m * 60 + s

                if self.remaining <= 0:
                    messagebox.showwarning(
                        "Invalid Time",
                        "Please enter a time greater than zero."
                    )
                    return

            except ValueError:
                messagebox.showerror(
                    "Invalid Input",
                    "Enter valid numbers. Minutes and seconds must be 0-59."
                )
                return

        self.running = True
        self.paused = False
        self.end_time = time.monotonic() + self.remaining
        self.status.config(text="Timer is running...", fg="#34D399")
        self.update_timer()

    def update_timer(self):
        if not self.running:
            return

        self.remaining = max(
            0, int(self.end_time - time.monotonic() + 0.999)
        )

        h = self.remaining // 3600
        m = (self.remaining % 3600) // 60
        s = self.remaining % 60

        self.display.config(text=f"{h:02d}:{m:02d}:{s:02d}")

        if self.remaining <= 0:
            self.running = False
            self.paused = False
            self.status.config(text="Time's up! Alarm ringing!", fg="#F87171")
            self.display.config(fg="#F87171")
            self.root.bell()
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            return

        self.after_id = self.root.after(100, self.update_timer)

    def pause(self):
        if self.running:
            self.remaining = max(
                0, int(self.end_time - time.monotonic() + 0.999)
            )
            self.running = False
            self.paused = True

            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None

            self.status.config(text="Timer paused", fg="#FBBF24")

    def reset(self):
        self.running = False
        self.paused = False

        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.remaining = 0
        self.display.config(text="00:00:00", fg="#34D399")
        self.status.config(text="Ready to start", fg="white")

        self.hours.delete(0, tk.END)
        self.hours.insert(0, "00")
        self.minutes.delete(0, tk.END)
        self.minutes.insert(0, "00")
        self.seconds.delete(0, tk.END)
        self.seconds.insert(0, "00")


if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
