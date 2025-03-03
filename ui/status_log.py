import tkinter as tk

class StatusLog:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="x", padx=10, pady=10)

        self.status_label = tk.Label(self.frame, text="Petri Net Status", font=("Arial", 12, "bold"))
        self.status_label.pack()

        self.status_text = tk.Text(self.frame, height=8, width=80, state="disabled", bg="black", fg="lime")
        self.status_text.pack(fill="both", expand=True)

    def update_status(self, pn, message=None, step=None):
        """Ενημερώνει το text box με την τρέχουσα κατάσταση του Petri Net"""
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)

        # Εμφάνιση αρχικής κατάστασης
        if message and step:  # Αν έχουμε βήμα, θα εμφανίσουμε το μήνυμα και το βήμα
            self.status_text.insert(tk.END, f"🔁 Step {step}: {message}\n")

        # Εμφάνιση της τρέχουσας κατάστασης του Petri Net
        places_status = "\n".join([f"Place: {p.name} - Tokens: {p.tokens}" for p in pn.places.values()])
        
        transitions_status = "\n".join([
            f"Transition: {t.name} - Inputs: {', '.join(f'{p.name}({c})' for p, c in t.inputs.items())} "
            f"→ Outputs: {', '.join(f'{p.name}({c})' for p, c in t.outputs.items())}"
            for t in pn.transitions.values()
        ])

        status_text = "📌 Places:\n" + (places_status if places_status else "No Places") + "\n\n" \
                    "🔀 Transitions:\n" + (transitions_status if transitions_status else "No Transitions")

        self.status_text.insert(tk.END, status_text + "\n")

        self.status_text.config(state="disabled")