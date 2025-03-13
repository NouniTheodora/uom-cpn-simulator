import tkinter as tk

class StatusLog:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="x", padx=10, pady=10)

        self.status_label = tk.Label(self.frame, text="Petri Net Status", font=("Arial", 12, "bold"))
        self.status_label.pack()

        self.status_text = tk.Text(self.frame, height=40, width=80, state="disabled", bg="black", fg="lime")
        self.status_text.pack(fill="both", expand=True)

    def write_log(self, message:str):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.config(state="disabled")