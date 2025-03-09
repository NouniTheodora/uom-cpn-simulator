import tkinter as tk
from tkinter import ttk
from ui.controls import ControlsPanel
from ui.visualization import VisualizationPanel
from ui.status_log import StatusLog
from models.petri_net import PetriNet
from tkinter import messagebox
import time

class PetriNetGUI:
    MAX_PLACES = 20  # Μέγιστος αριθμός θέσεων
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

        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, "Simulation Log Ready...\n")
        self.log_text.config(state=tk.DISABLED)


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
        if len(self.pn.places) >= self.MAX_PLACES:
            print("❌ Δεν μπορεί να προστεθεί άλλη θέση! Έχει επιτευχθεί το μέγιστο όριο των 20 θέσεων.")
            messagebox.showwarning("Όριο Θέσεων", "Δεν μπορεί να προστεθεί άλλη θέση! Έχει επιτευχθεί το μέγιστο όριο των 20 θέσεων.")
            return
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
        """Τρέχει όλες τις μεταβάσεις και εμφανίζει την κίνηση των tokens με απλή καταγραφή"""
        self.log = []  # Αρχικοποίηση λίστας για αποθήκευση των βημάτων

        # Ενημέρωση για την αρχική κατάσταση
        self.update_status("▶️ Starting Full Simulation")
        self.log.append("▶️ Starting Full Simulation")

        # Καταγραφή αρχικής κατάστασης των θέσεων
        self.log.append(self.get_places_status())

        transitions = list(self.pn.transitions.keys())  # Λήψη όλων των transitions
        
        for step, transition_name in enumerate(transitions, 1):
            log_entry = f"🔹 Step {step}: Executing Transition {transition_name}"
            self.log.append(log_entry)  # Αποθήκευση στο log
            self.update_status(log_entry, step)
            success = self.pn.fire_transition(transition_name)  
            self.update_preview()
            
            if not success:
                self.log.append(f"❌ Transition {transition_name} could not be fired.")
                break

            time.sleep(1)  # Καθυστέρηση για οπτικοποίηση

        self.update_status("✅ Simulation Completed")
        self.log.append("✅ Simulation Completed")

        messagebox.showinfo("Full Simulation", "Η προσομοίωση ολοκληρώθηκε!")
        self.root.after(100, self.show_log_window) 

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
        """Εμφανίζει το παράθυρο Simulation Log με τα καταγεγραμμένα μηνύματα"""
        log_window = tk.Toplevel(self.root)
        log_window.title("Simulation Log")
        log_window.geometry("650x450")

        frame = tk.Frame(log_window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_area = tk.Text(frame, wrap="word", width=80, height=22, font=("Courier", 11), bg="white", fg="black", borderwidth=0)
        self.text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)

        # ✅ Αν η `self.log` είναι κενή, εμφανίζουμε μήνυμα
        if not self.log:
            text_area.insert(tk.END, "⚠️ No logs available.\n")
        else:
            # ✅ Εμφάνιση όλων των logs στο Text Widget
            for log_entry in self.log:
                self.text_area.insert(tk.END, f"{log_entry}\n")

        self.text_area.config(state=tk.DISABLED)  # Απενεργοποίηση επεξεργασίας

        close_button = tk.Button(frame, text="Close", command=log_window.destroy, font=("Arial", 12))
        close_button.pack(pady=5)



    def reset_all(self):
        """Επαναφέρει το Petri Net στην αρχική του κατάσταση και ανανεώνει το UI"""
        print("\n🔄 [RESET] Ξεκινά η επαναφορά του Petri Net...")
        print("=" * 70)
        
        # Διαγραφή όλων των θέσεων και μεταβάσεων
        self.pn.places.clear()
        self.pn.transitions.clear()
        
        
        print("✔ Όλες οι θέσεις και οι μεταβάσεις διαγράφηκαν επιτυχώς.")
        
        self.update_status()
        self.update_preview()
        
        print("⚡ Το Petri Net επανήλθε στην αρχική του κατάσταση.")
        print("=" * 70)
        
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