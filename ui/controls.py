import tkinter as tk

class ControlsPanel:
    def __init__(self, parent, gui):
        self.gui = gui
        self.frame = tk.Frame(parent)
        self.frame.pack(side="left", fill="y", padx=10)

        tk.Label(self.frame, text="Petri Net Controls", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.frame, text="Add Place").pack()
        self.place_name_entry = tk.Entry(self.frame)
        self.place_name_entry.pack(pady=2)
        self.place_name_entry.insert(0, "Name")

        self.place_tokens_entry = tk.Entry(self.frame)
        self.place_tokens_entry.pack(pady=2)
        self.place_tokens_entry.insert(0, "Tokens")

        self.add_place_btn = tk.Button(self.frame, text="Add Place", command=self.add_place)
        self.add_place_btn.pack(pady=5)

        tk.Label(self.frame, text="Add Transition").pack()
        self.trans_name_entry = tk.Entry(self.frame)
        self.trans_name_entry.pack(pady=2)
        self.trans_name_entry.insert(0, "Name")

        self.trans_inputs_entry = tk.Entry(self.frame)
        self.trans_inputs_entry.pack(pady=2)
        self.trans_inputs_entry.insert(0, "Inputs (P1:2,P2:1)")

        self.trans_outputs_entry = tk.Entry(self.frame)
        self.trans_outputs_entry.pack(pady=2)
        self.trans_outputs_entry.insert(0, "Outputs (P3:1)")

        self.add_trans_btn = tk.Button(self.frame, text="Add Transition", command=self.add_transition)
        self.add_trans_btn.pack(pady=5)

        tk.Label(self.frame, text="Fire Transition").pack()
        self.fire_trans_entry = tk.Entry(self.frame)
        self.fire_trans_entry.pack(pady=2)
        self.fire_trans_entry.insert(0, "Transition Name")

        self.fire_trans_btn = tk.Button(self.frame, text="Fire Transition", command=self.fire_transition)
        self.fire_trans_btn.pack(pady=5)

        self.demo_btn = tk.Button(self.frame, text="Demo Petri Net", command=self.gui.run_demo)
        self.demo_btn.pack(pady=10)

    def add_place(self):
        name = self.place_name_entry.get().strip()
        tokens_str = self.place_tokens_entry.get().strip()
        if not tokens_str.isdigit():
            return
        tokens = int(tokens_str)
        self.gui.add_place(name, tokens)

    def add_transition(self):
        name = self.trans_name_entry.get()
        inputs = self.parse_places(self.trans_inputs_entry.get())
        outputs = self.parse_places(self.trans_outputs_entry.get())
        self.gui.add_transition(name, inputs, outputs)

    def fire_transition(self):
        name = self.fire_trans_entry.get()
        self.gui.fire_transition(name)

    def parse_places(self, text):
        places = {}
        for item in text.split(","):
            if ":" in item:
                name, tokens = item.split(":")
                places[name.strip()] = int(tokens)
        return places