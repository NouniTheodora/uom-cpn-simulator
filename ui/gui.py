import tkinter as tk
from tkinter import ttk
from ui.controls import ControlsPanel
from ui.visualization import VisualizationPanel
from ui.status_log import StatusLog
from models.petri_net import PetriNet
from tkinter import messagebox
import time

class PetriNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Petri Net Simulator")
        self.root.geometry("1000x1000")
        self.pn = PetriNet("GUI Net",self)

        self.main_frame = ttk.Frame(root,padding="10")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.controls = ControlsPanel(self.main_frame, self)
        self.visualization = VisualizationPanel(self.main_frame, self.pn)
        self.status_log = StatusLog(root)

        self.log = []  # Η λίστα για την καταγραφή των βημάτων της προσομοίωσης
        # 🔹 Frame για το Log Output
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Simulation Log", padding=5)
        self.log_frame.pack(fill="both", expand=True, pady=10)

        # 🔹 Text Widget για logs (με Scrolling)
        self.log_text = tk.Text(self.log_frame, height=10, width=100, bg="#f4f4f4", fg="black", font=("Arial", 10))
        self.log_text.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=self.scrollbar.set, state=tk.DISABLED)

        # 🔹 Progress Bar
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.log_text = tk.Text(self.main_frame, height=10, width=100, state=tk.DISABLED)
        self.log_text.pack(pady=5)

        self.update_status()

    def update_status(self, message=None, step=None):
        """Ενημερώνει το StatusLog με την τρέχουσα κατάσταση του Petri Net"""
        # Αν δεν υπάρχει βήμα (όταν καλείται την πρώτη φορά), αποθηκεύουμε την αρχική κατάσταση
        if message is not None and step is not None:
            self.status_log.update_status(self.pn, message, step)
        else:
            self.status_log.update_status(self.pn)

    def update_preview(self):
        self.visualization.update_preview()

    def log_message(self, message):
        """Εμφανίζει το μήνυμα στο terminal και στο Text widget του GUI"""
        print(message)  # Εμφάνιση στο terminal
    
        # Ενεργοποιούμε προσωρινά το Text widget για να γράψουμε
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)  # Κάνει scroll στο τέλος του κειμένου
        self.log_text.config(state=tk.DISABLED)

    def add_place(self, name, tokens):
        self.pn.add_place(name, tokens)
        self.update_status()
        self.update_preview()

    def add_transition(self, name, inputs, outputs):
        self.pn.add_transition(name, inputs, outputs)
        self.update_status()
        self.update_preview()

    def fire_transition(self, name):
        self.pn.fire_transition(name)
        self.update_status()
        self.update_preview()

    def run_full_simulation(self):
        """Τρέχει όλες τις μεταβάσεις και εμφανίζει την κίνηση των tokens με λεπτομέρειες"""
        self.log = []  # Αρχικοποίηση λίστας για αποθήκευση των βημάτων

        # Ενημέρωση για την αρχική κατάσταση
        self.update_status("Starting Full Simulation")
        self.log.append("Starting Full Simulation")

        # Καταγραφή αρχικής κατάστασης των θέσεων
        self.log.append(self.get_places_status())

        transitions = list(self.pn.transitions.keys())  # Λήψη όλων των transitions
        
        for step, transition_name in enumerate(transitions, 1):
            # 1️⃣ Αποθήκευση αρχικής κατάστασης των tokens
            initial_state = self.pn.places.copy()

            log_entry = f"🔹 Step {step}: Executing Transition {transition_name}"
            self.log.append(log_entry)  # Αποθήκευση στο log
            self.update_status(log_entry, step)

            # 2️⃣ Εκτέλεση της μετάβασης
            self.pn.fire_transition(transition_name)  
            self.update_preview()  # Ενημέρωση του διαγράμματος

            # 3️⃣ Αποθήκευση νέας κατάστασης των tokens
            final_state = self.pn.places.copy()

            # 4️⃣ Υπολογισμός αλλαγών στα tokens
            token_changes = self.get_token_changes(initial_state, final_state)
            self.log.append(token_changes)

            time.sleep(1)  # Καθυστέρηση για οπτικοποίηση

        self.update_status("✅ Simulation Completed")
        self.log.append("✅ Simulation Completed")

        messagebox.showinfo("Full Simulation", "Η προσομοίωση ολοκληρώθηκε!")
        self.show_log_window()  # Εμφάνιση του ιστορικού

    def get_token_changes(self, initial_state, final_state):
        """Υπολογίζει ποια tokens προστέθηκαν ή αφαιρέθηκαν σε κάθε θέση."""
        changes = []
        for place in initial_state.keys():
            before = initial_state[place]
            after = final_state[place]
            if before != after:
                change = after - before
                if change > 0:
                    changes.append(f"🟢 {place}: +{change} tokens")
                else:
                    changes.append(f"🔴 {place}: {change} tokens")
        
        return "🔄 Token Changes: " + ", ".join(changes) if changes else "No changes in tokens"
 
    def show_log_window(self):
        """Εμφανίζει το παράθυρο Simulation Log με όλα τα μηνύματα."""
        log_window = tk.Toplevel(self.root)
        log_window.title("Simulation Log")
        log_window.geometry("650x450")

        frame = tk.Frame(log_window, bg="black", padx=5, pady=5)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        inner_frame = tk.Frame(frame, bg="white")
        inner_frame.pack(fill="both", expand=True, padx=3, pady=3)

        title_label = tk.Label(inner_frame, text="📜 Simulation Log", font=("Arial", 14, "bold"), fg="black", bg="white")
        title_label.pack(pady=5)

        text_area = tk.Text(inner_frame, wrap="word", width=80, height=22, font=("Courier", 11), bg="white", fg="black", borderwidth=0)
        text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_area)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_area.yview)

        # ✅ Εμφάνιση ΟΛΩΝ των logs από το Terminal στο Log Window
        for log_entry in self.log:
            text_area.insert(tk.END, f"{log_entry}\n")

        text_area.config(state=tk.DISABLED)  # Απενεργοποίηση επεξεργασίας

        close_button = tk.Button(inner_frame, text="Close", command=log_window.destroy, font=("Arial", 12), bg="red", fg="white")
        close_button.pack(pady=5)

    def reset_all(self):
        YELLOW = "\033[93m"
        """Επαναφέρει το Petri Net στην αρχική του κατάσταση"""
        self.pn = PetriNet("GUI Net")  # Δημιουργεί νέο Petri Net
    
        # Διαγράφουμε τα περιεχόμενα των panels
        self.controls.frame.destroy()  
        self.visualization.frame.destroy()
        self.status_log.frame.destroy()

        # Ξαναδημιουργούμε τα panels
        self.controls = ControlsPanel(self.main_frame, self)
        self.visualization = VisualizationPanel(self.main_frame, self.pn)
        self.status_log = StatusLog(self.main_frame)

        # Ενημερώνουμε το GUI
        self.update_status()
        self.update_preview()
        print(f"{YELLOW}⚡ Το Petri Net επανήλθε στην αρχική του κατάσταση.")
        # Προβολή μηνύματος επιτυχούς reset
        self.root.after(100, lambda: messagebox.showinfo("Reset", "Το Petri Net επαναφέρθηκε στην αρχική του κατάσταση!"))


    def get_places_status(self):
        """Επιστρέφει την τρέχουσα κατάσταση όλων των θέσεων και των tokens τους."""
        status = "🔘 Places Status: "
        status += ", ".join([f"{place}({tokens})" for place, tokens in self.pn.places.items()])
        return status

    def run_demo(self):
        """Δημιουργεί ένα προ-ορισμένο Petri Net για δοκιμή"""
        self.pn.add_place("P1", 3)
        self.pn.add_place("P2", 0)
        self.pn.add_transition("T1", {"P1": 2}, {"P2": 1})
        self.pn.fire_transition("T1")
        self.update_status()
        self.update_preview()
        messagebox.showinfo("Demo", "Το Demo Petri Net εκτελέστηκε!")