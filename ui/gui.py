from tkinter import ttk
from ui.controls import ControlsPanel
from ui.visualization import VisualizationPanel
from ui.status_log import StatusLog
from models.petri_net import PetriNet
from tkinter import messagebox

class PetriNetGUI:
    MAX_PLACES = 20

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

    def update_preview(self):
        self.visualization.update_preview()

    def add_place(self, name, tokens):
        if len(self.pn.places) >= self.MAX_PLACES:
            messagebox.showwarning("Sorry, you can not add more than 20 places for this petri net.")
            return
        self.pn.add_place(name, tokens)
        self.update_preview()

    def add_transition(self, name, inputs, outputs):
        self.pn.add_transition(name, inputs, outputs)
        self.update_preview()

    def fire_transition(self, name):
        self.pn.fire_transition(name)
        self.update_preview()

    def run_full_simulation(self):
        transitions = list(self.pn.transitions.keys())

        if not transitions:
            messagebox.showinfo("No transitions found", "You should add a transition before running the simulation.")
            return

        self.write_log("\n🚀 Starting Full Simulation")
        self.write_log(f"\nPlaces Status: {[f"{tokens}" for place, tokens in self.pn.places.items()]}\n")
        
        for step, transition_name in enumerate(transitions, 1):
            self.write_log(f"🔹 Step {step}: Executing Transition {transition_name}")
            success = self.pn.fire_transition(transition_name)  
            self.update_preview()
            
            if not success:
                self.write_log(f"\n❌ Transition {transition_name} could not be fired.")
                break

        self.write_log("\n✅ Simulation Completed")
 
    def reset_all(self):
        self.pn.places.clear()
        self.pn.transitions.clear()
        self.write_log("\nAll the places & transitions are cleared!\n")
        self.update_preview()
        self.root.after(100, lambda: messagebox.showinfo("Reset", "Petri net has been cleared!"))

    def run_demo(self):
        self.write_log("\n🚀 Starting Full Simulation of the demo Petri Net\n")
        self.pn.add_place("P1", 3)
        self.pn.add_place("P2", 1)
        self.pn.add_place("P3", 0)
        self.pn.add_place("P4", 0)
        self.pn.add_transition("T1", {"P1": 1, "P2": 1}, {"P3": 1})
        self.pn.add_transition("T2", {"P3": 1}, {"P4": 1})
        self.pn.fire_transition("T1")
        self.pn.fire_transition("T2")
        self.update_preview()
        self.write_log("\n✅ Simulation Completed")

    def write_log(self, message: str):
        self.status_log.write_log(message)