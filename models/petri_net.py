import networkx as nx
import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
from models.place import Place
from models.transition import Transition
from models.token_manager import TokenManager

class PetriNet:
    
    def __init__(self, name: str):
        self.name = name
        self.places = {}
        self.transitions = {}

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
        inputs = {self.places[p]: tokens for p, tokens in input_places.items()}
        outputs = {self.places[p]: tokens for p, tokens in output_places.items()}
        self.transitions[name] = Transition(name, inputs, outputs)

    def fire_transition(self, transition_name):
        """Εκτελεί μια μετάβαση αν είναι ενεργοποιήσιμη."""
        if transition_name not in self.transitions:
            print(f"❌ Transition {transition_name} does not exist!")
            return

        transition = self.transitions[transition_name]

        if not hasattr(transition, 'inputs') or not hasattr(transition, 'outputs'):
            print(f"❌ Transition {transition_name} is missing inputs/outputs attributes.")
            return

        # 1️⃣ Έλεγχος αν υπάρχουν αρκετά tokens στις εισόδους
        for place, required_tokens in transition.inputs.items():
            if self.places.get(place, 0) < required_tokens:
                print(f"⚠️ Not enough tokens in {place} to fire {transition_name}")
                return

        # 2️⃣ Αφαίρεση tokens από τις εισόδους
        for place, required_tokens in transition.inputs.items():
            self.places[place] -= required_tokens

        # 3️⃣ Προσθήκη tokens στις εξόδους
        for place, tokens_to_add in transition.outputs.items():
            self.places[place] = self.places.get(place, 0) + tokens_to_add

        print(f"✅ Transition {transition_name} fired successfully!")


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