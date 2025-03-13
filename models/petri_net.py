import networkx as nx
import matplotlib.pyplot as plt
from models.place import Place
from models.transition import Transition

class PetriNet:
    
    def __init__(self, name, gui):
        self.name = name
        self.gui=gui
        self.places = {}
        self.transitions = {}

    def add_place(self, name: str, tokens: int = 0):
        self.places[name] = Place(name, tokens)
        self.log_message(f"📌 Place with name {name} is added, with {tokens} tokens\n")

    def add_transition(self, name: str, input_places: dict, output_places: dict):
        inputs = {}
        outputs = {}

        for place_name, tokens in input_places.items():
            if place_name in self.places:
                inputs[self.places[place_name]] = tokens

        for place_name, tokens in output_places.items():
            if place_name not in self.places:
                self.places[place_name] = Place(place_name, 0)
            outputs[self.places[place_name]] = tokens

        self.transitions[name] = Transition(name, inputs, outputs)
        self.log_message(f"🔀 Transition with name {name} is added\n")

    def fire_transition(self, transition_name):
        if transition_name not in self.transitions:
            self.log_message(f"❌ Transition {transition_name} does not exist in this Petri Net!\n")
            return False

        transition = self.transitions[transition_name]

        self.log_message(f"🔍 Before firing the transition {transition_name}: { {p: self.places[p].tokens for p in self.places} }")

        for place_obj, required_tokens in transition.inputs.items():
            place_name = place_obj.name
            available_tokens = self.places[place_name].tokens
            self.log_message(f"🔍 Checking {place_name}: Needs {required_tokens}, Available {available_tokens}")

            if available_tokens < required_tokens:
                self.log_message(f"\n❌ Not enough tokens in {place_name}: {available_tokens} tokens available to fire {transition_name}, but {required_tokens} are required")
                return False

        for place_obj, required_tokens in transition.inputs.items():
            place_name = place_obj.name
            self.places[place_name].tokens -= required_tokens

        for place_obj, tokens_to_add in transition.outputs.items():
            place_name = place_obj.name
            self.places[place_name].tokens += tokens_to_add

        if not transition.outputs.items():
            self.log_message(f"\nTransition {transition_name} was fired, but no output has been detected, so the token is lost\n")
            return True

        self.log_message(f"\n✅ After the Transition {transition_name} is fired: { {p: self.places[p].tokens for p in self.places} }\n")

        return True
    
    def log_message(self, message):
        if self.gui:
            self.gui.status_log.write_log(message)

    