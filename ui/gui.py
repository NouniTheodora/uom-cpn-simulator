import tkinter as tk
from ui.controls import ControlsPanel
from ui.visualization import VisualizationPanel
from ui.status_log import StatusLog
from models.petri_net import PetriNet
from tkinter import messagebox

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

    def update_status(self):
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

    def run_demo(self):
        """Δημιουργεί ένα προ-ορισμένο Petri Net για δοκιμή"""
        self.pn.add_place("P1", 3)
        self.pn.add_place("P2", 0)
        self.pn.add_transition("T1", {"P1": 2}, {"P2": 1})
        self.pn.fire_transition("T1")
        self.update_status()
        self.update_preview()
        messagebox.showinfo("Demo", "Το Demo Petri Net εκτελέστηκε!")
