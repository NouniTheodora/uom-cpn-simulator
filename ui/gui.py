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
        """Τρέχει όλες τις μεταβάσεις και εμφανίζει την κίνηση των tokens"""
        # Ενημέρωση για την αρχική κατάσταση
        self.update_status()

        # Εκτέλεση όλων των μεταβάσεων
        transitions = list(self.pn.transitions.keys())  # Λαμβάνουμε όλα τα transitions

        # Κίνηση των tokens με κάθε μετάβαση
        for step, transition_name in enumerate(transitions, 1):
            self.update_status(f"Executing Transition: {transition_name}", step)
            self.pn.fire_transition(transition_name)  # Εκτέλεση της μετάβασης
            self.update_preview()  # Ενημέρωση του διαγράμματος μετά από κάθε μετάβαση
            time.sleep(1)  # Μικρή καθυστέρηση για να δείξουμε την κίνηση των tokens

        # Ενημέρωση για την τελική κατάσταση
        self.update_status()

        messagebox.showinfo("Full Simulation", "Η πλήρης προσομοίωση ολοκληρώθηκε και τα tokens μετακινήθηκαν!")

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