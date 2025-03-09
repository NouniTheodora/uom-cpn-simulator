import networkx as nx
import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
from models.place import Place
from models.transition import Transition
from models.token_manager import TokenManager

class PetriNet:
    
    
    def __init__(self, name,gui):
        self.name = name
        self.gui=gui
        self.places = {}
        self.transitions = {}

    def run_full_simulation(self):
        """Τρέχει όλες τις μεταβάσεις και εμφανίζει την κίνηση των tokens με visualization"""
        self.log = []  # Αρχικοποίηση λίστας για αποθήκευση των βημάτων

        # Δημιουργία νέου παραθύρου για το simulation
        self.simulation_window = tk.Toplevel(self.root)
        self.simulation_window.title("Petri Net Simulation")
        self.simulation_window.geometry("800x600")

        #Προσθήκη του Visualization Panel στο νέο παράθυρο
        self.simulation_visualization = VisualizationPanel(self.simulation_window, self.pn)

        # Ενημέρωση για την αρχική κατάσταση
        self.log_message("🚀 Starting Full Simulation")
        self.log.append("🚀 Starting Full Simulation")

        #Καταγραφή αρχικής κατάστασης των θέσεων
        self.log.append(self.get_places_status())

        transitions = list(self.pn.transitions.keys())  # Λήψη όλων των transitions

        # Εκκίνηση της προσομοίωσης χωρίς να παγώνει το UI
        self.run_simulation_step(0, transitions)

    def run_simulation_step(self, step, transitions):
        
        """Εκτελεί μία μετάβαση τη φορά με χρήση του after() για ομαλή ανανέωση του UI"""
        if step >= len(transitions):
             # Τέλος της προσομοίωσης
            final_status = self.get_places_status()
            self.log.append(final_status)
            self.log_message(final_status)

            self.log_message("✅ Simulation Completed")
            self.log.append("✅ Simulation Completed")
            self.show_log_window()  # Εμφάνιση του ιστορικού
            messagebox.showinfo("Full Simulation", "Η προσομοίωση ολοκληρώθηκε!")
            return

        transition_name = transitions[step]

        # 1️⃣ Αποθήκευση αρχικής κατάστασης των tokens
        initial_state = {p: self.pn.places[p].tokens for p in self.pn.places}

        log_entry = f"🔹 Step {step + 1}: Executing Transition {transition_name}"
        self.log.append(log_entry)
        self.log_message(log_entry)

        # 2️⃣ Εκτέλεση της μετάβασης
        self.pn.fire_transition(transition_name)

        # 3️⃣ Αποθήκευση νέας κατάστασης των tokens
        final_state = {p: self.pn.places[p].tokens for p in self.pn.places}

        # 4️⃣ Υπολογισμός αλλαγών στα tokens
        token_changes = self.get_token_changes(initial_state, final_state)
        self.log.append(token_changes)
        self.log_message(token_changes)

        self.update_preview()  # Ενημέρωση του διαγράμματος
        self.root.update_idletasks()  # Ανανέωση του UI

        # 6️⃣ Καλούμε την επόμενη μετάβαση μετά από 1000ms (1 δευτερόλεπτο)
        self.root.after(1000, self.run_simulation_step, step + 1, transitions)



    def add_place(self, name: str, tokens: int = 0):
        """Προσθέτει έναν νέο κόμβο (Place) στο δίκτυο."""
        self.places[name] = Place(name, tokens)

    def add_transition(self, name: str, input_places: dict, output_places: dict):
        """
        Προσθέτει μια νέα μετάβαση στο Petri Net.
        
        :param name: Όνομα της μετάβασης
        :param input_places: Λεξικό {place_name: απαιτούμενα tokens}
        :param output_places: Λεξικό {place_name: tokens που προστίθενται}
        """
        inputs = {}
        outputs = {}

        # Επεξεργασία των εισόδων
        for place_name, tokens in input_places.items():
            if place_name in self.places:
                inputs[self.places[place_name]] = tokens
            else:
                print(f"⚠️ Warning: Το place '{place_name}' δεν υπάρχει. Η μετάβαση {name} δε θα λειτουργήσει σωστά.")

        # Επεξεργασία των εξόδων
        for place_name, tokens in output_places.items():
            if place_name not in self.places:
                # Αν δεν υπάρχει η θέση, τη δημιουργούμε αυτόματα με 0 tokens
                self.places[place_name] = Place(place_name, 0)
            outputs[self.places[place_name]] = tokens

        # Προσθήκη της μετάβασης
        self.transitions[name] = Transition(name, inputs, outputs)
        print(f"✅ Μετάβαση {name} προστέθηκε: Inputs {input_places}, Outputs {output_places}")

    def fire_transition(self, transition_name):
        """Εκτελεί μια μετάβαση αν είναι ενεργοποιήσιμη."""
        if transition_name not in self.transitions:
            self.gui.log_message(f"❌ Transition {transition_name} does not exist!")
            return

        transition = self.transitions[transition_name]

        # 🔍 Εκτύπωση της κατάστασης των θέσεων πριν την εκτέλεση
        self.gui.log_message(f"🔍 Before Transition {transition_name}: { {p: self.places[p].tokens for p in self.places} }")

        # 1️⃣ Έλεγχος αν υπάρχουν αρκετά tokens στις εισόδους
        for place_obj, required_tokens in transition.inputs.items():
            place_name = place_obj.name
            available_tokens = self.places[place_name].tokens
            self.gui.log_message(f"🔍 Checking {place_name}: Needs {required_tokens}, Available {available_tokens}")

            if available_tokens < required_tokens:
                self.gui.log_message(f"⚠️ Not enough tokens in {place_name}: {available_tokens} tokens to fire {transition_name}")
                return


        # 2️⃣ Αφαίρεση tokens από τις εισόδους
        for place_obj, required_tokens in transition.inputs.items():
            place_name = place_obj.name
            self.places[place_name].tokens -= required_tokens

        # 3️⃣ Προσθήκη tokens στις εξόδους
        for place_obj, tokens_to_add in transition.outputs.items():
            place_name = place_obj.name
            if place_name not in self.places:
                self.places[place_name] = Place(place_name, 0)  # Αν η θέση δεν υπάρχει, τη δημιουργούμε

            self.places[place_name].tokens += tokens_to_add  # ✅ Τώρα τα tokens προστίθενται σωστά!


        # 🔍 Εκτύπωση της κατάστασης των θέσεων μετά την εκτέλεση
        self.gui.log_message(f"✅ After Transition {transition_name}: { {p: self.places[p].tokens for p in self.places} }")

        self.gui.log_message(f"✅ Transition {transition_name} fired successfully!")

    def show_state(self):
        """Εμφανίζει την τρέχουσα κατάσταση του Petri Net."""
        print(f"\n📌 Κατάσταση του Petri Net '{self.name}':")
        for place in self.places.values():
            print(place)

    def get_token_changes(self, initial_state, final_state):
        """Υπολογίζει ποια tokens προστέθηκαν ή αφαιρέθηκαν σε κάθε θέση."""
        changes = []
        all_places = set(initial_state.keys()).union(set(final_state.keys()))

        for place in all_places:
            before = initial_state.get(place, 0)  # Αν δεν υπάρχει, υποθέτουμε 0
            after = final_state.get(place, 0)

            if before != after:
                change = after - before
                if change > 0:
                    changes.append(f"🟢 {place}: +{change} tokens")
                else:
                    changes.append(f"🔴 {place}: {change} tokens")

        return "🔄 Token Changes: " + ", ".join(changes) if changes else "No changes in tokens"

    def visualize(self):
        """Οπτικοποίηση του Petri Net με networkx και matplotlib"""
        G = nx.DiGraph()

        # Προσθήκη κόμβων (Places και Transitions)
        for place in self.places.values():
            G.add_node(place.name, label=f"{place.name}\n({place.tokens})", color="lightblue")

        for transition in self.transitions.values():
            G.add_node(transition.name, label=transition.name, color="red")

        # Προσθήκη ακμών (Σχέσεις μεταξύ Places και Transitions)
        for transition in self.transitions.values():
            for place, tokens in transition.inputs.items():
                G.add_edge(place.name, transition.name, label=f"-{tokens}->")
            for place, tokens in transition.outputs.items():
                G.add_edge(transition.name, place.name, label=f"-{tokens}->")

        # Ανάκτηση labels και χρωμάτων
        labels = nx.get_node_attributes(G, 'label')
        colors = [G.nodes[n]['color'] for n in G.nodes]

        # Σχεδίαση του γράφου
        pos = nx.spring_layout(G)  # Αυτόματη τοποθέτηση κόμβων
        nx.draw(G, pos, with_labels=True, labels=labels, node_color=colors, edge_color="black", node_size=2000, font_size=10, font_weight="bold")
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="black")

        # Εμφάνιση του διαγράμματος
        plt.title(f"Petri Net: {self.name}")
        plt.show()

    def __str__(self):
        return f"Petri Net ({self.name})"
    
    def log_message(self, message):
        """Στέλνει εμφανή μηνύματα στο GUI και στο terminal."""
        formatted_message = f"\n🚀 [Petri Net] {message}\n{'='*50}"
        if self.gui:
            self.gui.update_status(message)
            print(formatted_message)

    