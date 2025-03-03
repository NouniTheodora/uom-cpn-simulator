import tkinter as tk

class ControlsPanel:
    def __init__(self, parent, gui):
        self.gui = gui
        self.frame = tk.Frame(parent)
        self.frame.pack(side="left", fill="y", padx=10)

        tk.Label(self.frame, text="Petri Net Controls", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.frame, text="Add Place").pack()
        self.place_name_entry = self.create_entry(self.frame, "Name")
        self.place_tokens_entry = self.create_entry(self.frame, "Tokens")
        self.add_place_btn = tk.Button(self.frame, text="Add Place", command=self.add_place)
        self.add_place_btn.pack(pady=5)

        tk.Label(self.frame, text="Add Transition").pack()
        self.trans_name_entry = self.create_entry(self.frame, "Name")
        self.trans_inputs_entry = self.create_entry(self.frame, "f.e. P1:1,P2:1")
        self.trans_outputs_entry = self.create_entry(self.frame, "f.e. P3:1, P4:1")
        self.add_trans_btn = tk.Button(self.frame, text="Add Transition", command=self.add_transition)
        self.add_trans_btn.pack(pady=5)

        tk.Label(self.frame, text="Fire Transition").pack()
        self.fire_trans_entry = self.create_entry(self.frame, "Transition Name")
        self.fire_trans_btn = tk.Button(self.frame, text="Fire Transition", command=self.fire_transition)
        self.fire_trans_btn.pack(pady=5)

        self.demo_btn = tk.Button(self.frame, text="Demo Petri Net", command=self.gui.run_demo)
        self.demo_btn.pack(pady=10)

    def create_entry(self, parent, placeholder):
        """Create an Entry widget with placeholder functionality"""
        entry = tk.Entry(parent)
        entry.insert(0, placeholder)  # Set placeholder text
        entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, entry, placeholder))
        entry.pack(pady=2)
        return entry

    def clear_placeholder(self, event, entry, placeholder):
        """Clear the placeholder when the field is focused"""
        if entry.get() == placeholder:  # If placeholder is there
            entry.delete(0, tk.END)

    def add_placeholder(self, event, entry, placeholder):
        """Add placeholder text back if the field is empty"""
        if not entry.get():
            entry.insert(0, placeholder)

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