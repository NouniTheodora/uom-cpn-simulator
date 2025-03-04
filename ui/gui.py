import tkinter as tk
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
        self.pn = PetriNet("GUI Net")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.controls = ControlsPanel(self.main_frame, self)
        self.visualization = VisualizationPanel(self.main_frame, self.pn)
        self.status_log = StatusLog(root)

        self.log = []  # Η λίστα για την καταγραφή των βημάτων της προσομοίωσης

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

        transitions = list(self.pn.transitions.keys())  # Λήψη όλων των transitions
        
        for step, transition_name in enumerate(transitions, 1):
            log_entry = f"Step {step}: Executing Transition {transition_name}"
            self.log.append(log_entry)  # Αποθήκευση στο log
            self.update_status(log_entry, step)

            self.pn.fire_transition(transition_name)  # Εκτέλεση της μετάβασης
            self.update_preview()  # Ενημέρωση του διαγράμματος
            time.sleep(1)  # Καθυστέρηση για οπτικοποίηση

        self.update_status("Simulation Completed")
        self.log.append("Simulation Completed")

        messagebox.showinfo("Full Simulation", "Η προσομοίωση ολοκληρώθηκε!")
        self.show_log_window()  # Εμφάνιση του ιστορικού

    def show_log_window(self):
        """Εμφανίζει ένα παράθυρο με όλα τα βήματα της προσομοίωσης σε μορφή λίστας."""
        log_window = tk.Toplevel(self.root)
        log_window.title("Simulation Log")
        log_window.geometry("600x400")

        # Frame για styling
        frame = tk.Frame(log_window, bg="#2c3e50")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Προσθήκη τίτλου
        title_label = tk.Label(frame, text="📜 Simulation Log", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(pady=5)

        # Προσθήκη `Text` widget με scrollbar
        text_area = tk.Text(frame, wrap="word", width=70, height=20, font=("Courier", 11), bg="#ecf0f1", fg="black")
        text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_area)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_area.yview)

        # Εισαγωγή των logs με styling
        for step, log_entry in enumerate(self.log, 1):
            if "Executing Transition" in log_entry:
                text_area.insert(tk.END, f"🔹 {log_entry}\n", "transition")
            elif "Simulation Completed" in log_entry:
                text_area.insert(tk.END, f"✅ {log_entry}\n", "completed")
            else:
                text_area.insert(tk.END, f"{log_entry}\n")

        # Ορισμός χρώματος για τα διαφορετικά στάδια
        text_area.tag_config("transition", foreground="blue", font=("Courier", 11, "bold"))
        text_area.tag_config("completed", foreground="green", font=("Courier", 12, "bold"))

        text_area.config(state=tk.DISABLED)  # Απενεργοποίηση επεξεργασίας

        # Κουμπί κλεισίματος
        close_button = tk.Button(frame, text="Close", command=log_window.destroy, font=("Arial", 12), bg="#e74c3c", fg="white")
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


    def run_demo(self):
        """Δημιουργεί ένα προ-ορισμένο Petri Net για δοκιμή"""
        self.pn.add_place("P1", 3)
        self.pn.add_place("P2", 0)
        self.pn.add_transition("T1", {"P1": 2}, {"P2": 1})
        self.pn.fire_transition("T1")
        self.update_status()
        self.update_preview()
        messagebox.showinfo("Demo", "Το Demo Petri Net εκτελέστηκε!")