import tkinter as tk
from tkinter import messagebox

class StatusLog:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="x", padx=10, pady=10)

        self.status_label = tk.Label(self.frame, text="Petri Net Status", font=("Arial", 12, "bold"))
        self.status_label.pack()

        self.status_text = tk.Text(self.frame, height=8, width=80, state="disabled", bg="black", fg="lime")
        self.status_text.pack(fill="both", expand=True)

        self.exit_btn = tk.Button(self.frame, text="Exit", command=self.exit_app, bg="red", fg="white")
        self.exit_btn.pack(pady=5)

    def update_status(self, pn):
        """Ενημερώνει το text box με την τρέχουσα κατάσταση του Petri Net"""
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)

        places_status = "\n".join([f"Place: {p.name} - Tokens: {p.tokens}" for p in pn.places.values()])
        
        transitions_status = "\n".join([
            f"Transition: {t.name} - Inputs: {', '.join(f'{p.name}({c})' for p, c in t.inputs.items())} "
            f"→ Outputs: {', '.join(f'{p.name}({c})' for p, c in t.outputs.items())}"
            for t in pn.transitions.values()
        ])

        status_text = "📌 Places:\n" + (places_status if places_status else "No Places") + "\n\n" \
                    "🔀 Transitions:\n" + (transitions_status if transitions_status else "No Transitions")

        self.status_text.insert(tk.END, status_text)
        self.status_text.config(state="disabled")

    def exit_app(self):
        """Εμφανίζει μήνυμα επιβεβαίωσης και κλείνει το πρόγραμμα"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.frame.master.quit()
