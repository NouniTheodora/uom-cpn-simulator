import tkinter as tk
from tkinter import messagebox
from models.petri_net import PetriNet
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PetriNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Petri Net Simulator")
        self.pn = PetriNet("GUI Net")

        # Τίτλος
        tk.Label(root, text="Petri Net Simulator", font=("Arial", 14, "bold")).pack(pady=10)

        # --- Περιοχή Προσθήκης Places ---
        tk.Label(root, text="Προσθήκη Place:").pack()
        self.place_name_entry = tk.Entry(root)
        self.place_name_entry.pack(pady=2)
        self.place_name_entry.insert(0, "Όνομα Place")
        self.place_name_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(self.place_name_entry, "Όνομα Place"))

        self.place_tokens_entry = tk.Entry(root)
        self.place_tokens_entry.pack(pady=2)
        self.place_tokens_entry.insert(0, "Αρχικά tokens")
        self.place_tokens_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(self.place_tokens_entry, "Αρχικά tokens"))

        self.add_place_btn = tk.Button(root, text="Προσθήκη Place", command=self.add_place)
        self.add_place_btn.pack(pady=5)

        # --- Περιοχή Προσθήκης Transition ---
        tk.Label(root, text="Προσθήκη Transition:").pack()
        self.trans_name_entry = tk.Entry(root)
        self.trans_name_entry.pack(pady=2)
        self.trans_name_entry.insert(0, "Όνομα Transition")
        self.trans_name_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(self.trans_name_entry, "Όνομα Transition"))

        self.trans_inputs_entry = tk.Entry(root)
        self.trans_inputs_entry.pack(pady=2)
        self.trans_inputs_entry.insert(0, "Εισερχόμενα (π.χ. P1:2,P2:1)")
        self.trans_inputs_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(self.trans_inputs_entry, "Εισερχόμενα (π.χ. P1:2,P2:1)"))

        self.trans_outputs_entry = tk.Entry(root)
        self.trans_outputs_entry.pack(pady=2)
        self.trans_outputs_entry.insert(0, "Εξερχόμενα (π.χ. P3:1)")
        self.trans_outputs_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(self.trans_outputs_entry, "Εξερχόμενα (π.χ. P3:1)"))

        self.add_trans_btn = tk.Button(root, text="Προσθήκη Transition", command=self.add_transition)
        self.add_trans_btn.pack(pady=5)

        # --- Εκτέλεση Transition ---
        tk.Label(root, text="Εκτέλεση Transition:").pack()
        self.fire_trans_entry = tk.Entry(root)
        self.fire_trans_entry.pack(pady=2)
        self.fire_trans_entry.insert(0, "Όνομα Transition για εκτέλεση")
        self.fire_trans_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(self.fire_trans_entry, "Όνομα Transition για εκτέλεση"))

        self.fire_trans_btn = tk.Button(root, text="Εκτέλεση Transition", command=self.fire_transition)
        self.fire_trans_btn.pack(pady=5)

         # --- Περιοχή Οπτικοποίησης (Mini Preview) ---
        self.fig, self.ax = plt.subplots(figsize=(4, 3))  # Μικρό γράφημα
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(pady=10)

        self.update_preview()  # Αρχικό κενό γράφημα

        # --- Εμφάνιση Κατάστασης Petri Net ---
        self.status_label = tk.Label(root, text="Κατάσταση Petri Net:", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=10)

        self.status_text = tk.Text(root, height=10, width=40, state="disabled")
        self.status_text.pack()

        self.update_status()  # Ενημέρωση της αρχικής κατάστασης

        # --- Demo Petri Net ---
        self.demo_btn = tk.Button(root, text="Demo Petri Net", command=self.run_demo)
        self.demo_btn.pack(pady=10)

        # Κουμπί για Έξοδο από το πρόγραμμα
        self.exit_btn = tk.Button(root, text="Έξοδος", command=self.exit_app, bg="red", fg="white")
        self.exit_btn.pack(pady=10)

    def clear_placeholder(event, entry, placeholder):
        """Σβήνει το placeholder όταν ο χρήστης κλικάρει στο πεδίο"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def add_place(self):
        name = self.place_name_entry.get().strip()
        tokens_str = self.place_tokens_entry.get().strip()
        # Έλεγχος αν το πεδίο tokens περιέχει αριθμό
        if not tokens_str.isdigit():
            messagebox.showerror("Σφάλμα", "Τα tokens πρέπει να είναι αριθμός!")
            return
        tokens = int(tokens_str)
        self.pn.add_place(name, tokens)
        messagebox.showinfo("Success", f"Προστέθηκε το Place {name} με {tokens} tokens.")
        self.update_status()
        self.update_preview()

        # Καθαρισμός πεδίων
        self.place_name_entry.delete(0, tk.END)
        self.place_tokens_entry.delete(0, tk.END)

    def add_transition(self):
        name = self.trans_name_entry.get()
        inputs = self.parse_places(self.trans_inputs_entry.get())
        outputs = self.parse_places(self.trans_outputs_entry.get())
        self.pn.add_transition(name, inputs, outputs)
        messagebox.showinfo("Success", f"Προστέθηκε το Transition {name}.")
        self.update_status()
        self.update_preview()

    def fire_transition(self):
        name = self.fire_trans_entry.get()
        self.pn.fire_transition(name)
        self.update_status()
        self.update_preview()

    def run_demo(self):
        """Δημιουργεί ένα προ-ορισμένο Petri Net για δοκιμή"""
        self.pn = PetriNet("Demo Net")
        self.pn.add_place("P1", 3)
        self.pn.add_place("P2", 0)
        self.pn.add_transition("T1", {"P1": 2}, {"P2": 1})
        self.pn.fire_transition("T1")
        messagebox.showinfo("Demo", "Το Demo Petri Net εκτελέστηκε!")
        self.update_status()
        self.update_preview()

    def parse_places(self, text):
        """Μετατρέπει είσοδο τύπου 'P1:2,P2:1' σε λεξικό {όνομα: tokens}"""
        places = {}
        for item in text.split(","):
            if ":" in item:
                name, tokens = item.split(":")
                places[name.strip()] = int(tokens)
        return places

    def update_status(self):
        """Ενημερώνει το text box με την τρέχουσα κατάσταση του Petri Net (Places + Transitions)"""
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)

        # Εμφάνιση των Places
        places_status = "\n".join([f"Place: {p.name} - Tokens: {p.tokens}" for p in self.pn.places.values()])
        
        # Εμφάνιση των Transitions
        transitions_status = "\n".join([
            f"Transition: {t.name} - Inputs: {', '.join(f'{p.name}({c})' for p, c in t.inputs.items())} "
            f"→ Outputs: {', '.join(f'{p.name}({c})' for p, c in t.outputs.items())}"
            for t in self.pn.transitions.values()
        ])

        # Συνολικό status
        status_text = "📌 Places:\n" + (places_status if places_status else "No Places") + "\n\n" \
                    "🔀 Transitions:\n" + (transitions_status if transitions_status else "No Transitions")

        self.status_text.insert(tk.END, status_text)
        self.status_text.config(state="disabled")

    def exit_app(self):
        """Εμφανίζει μήνυμα επιβεβαίωσης και κλείνει το πρόγραμμα"""
        if messagebox.askyesno("Έξοδος", "Σίγουρα θέλετε να κλείσετε το πρόγραμμα;"):
            self.root.destroy()  # Κλείνει το παράθυρο

    def update_preview(self):
        """Σχεδιάζει το mini preview του Petri Net"""
        self.ax.clear()  # Καθαρισμός προηγούμενου διαγράμματος
        G = nx.DiGraph()

        # Προσθήκη κόμβων (Places & Transitions)
        for place in self.pn.places.values():
            G.add_node(place.name, label=f"{place.name}\n({place.tokens})", color="lightblue")

        for transition in self.pn.transitions.values():
            G.add_node(transition.name, label=transition.name, color="red")

        # Προσθήκη ακμών
        for transition in self.pn.transitions.values():
            for place, tokens in transition.inputs.items():
                G.add_edge(place.name, transition.name, label=f"-{tokens}->")
            for place, tokens in transition.outputs.items():
                G.add_edge(transition.name, place.name, label=f"-{tokens}->")

        # Ανάκτηση labels και χρωμάτων
        labels = nx.get_node_attributes(G, 'label')
        colors = [G.nodes[n]['color'] for n in G.nodes]

        # Σχεδίαση του mini preview
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, labels=labels, node_color=colors, edge_color="black",
                node_size=1000, font_size=8, font_weight="bold", ax=self.ax)

        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, font_color="black", ax=self.ax)

        self.canvas.draw()  # Ανανεώνει το preview

if __name__ == "__main__":
    root = tk.Tk()
    app = PetriNetGUI(root)
    root.mainloop()