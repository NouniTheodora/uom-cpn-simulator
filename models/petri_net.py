import networkx as nx
import matplotlib.pyplot as plt
from models.place import Place
from models.transition import Transition

class PetriNet:
    def __init__(self, name: str):
        self.name = name
        self.places = {}
        self.transitions = {}

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

    def fire_transition(self, name: str):
        """Εκτελεί μια μετάβαση αν είναι δυνατή."""
        if name not in self.transitions:
            raise ValueError(f"Η μετάβαση {name} δεν υπάρχει στο Petri Net!")
        
        transition = self.transitions[name]
        if transition.is_enabled():
            transition.fire()
            print(f"✔ Μετάβαση {name} εκτελέστηκε επιτυχώς.")
        else:
            print(f"❌ Η μετάβαση {name} δεν μπορεί να εκτελεστεί λόγω έλλειψης tokens.")

    def show_state(self):
        """Εμφανίζει την τρέχουσα κατάσταση του Petri Net."""
        print(f"\n📌 Κατάσταση του Petri Net '{self.name}':")
        for place in self.places.values():
            print(place)
            
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