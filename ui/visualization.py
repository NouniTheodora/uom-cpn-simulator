import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VisualizationPanel:
    def __init__(self, parent, pn):
        self.pn = pn
        self.frame = tk.Frame(parent)
        self.frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()

        self.canvas_widget.grid(row=0, column=0, sticky="nsew")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.update_preview()

    def update_preview(self):
        """Ενημερώνει το mini preview του Petri Net"""
        self.ax.clear()

        G = nx.DiGraph()

        for place in self.pn.places.values():
            G.add_node(place.name, label=f"{place.name}\n({place.tokens})", color="lightblue")

        for transition in self.pn.transitions.values():
            G.add_node(transition.name, label=transition.name, color="red")

        for transition in self.pn.transitions.values():
            for place, tokens in transition.inputs.items():
                G.add_edge(place.name, transition.name, label=f"[{tokens}]")
            for place, tokens in transition.outputs.items():
                G.add_edge(transition.name, place.name, label=f"[{tokens}]")

        labels = nx.get_node_attributes(G, 'label')
        colors = [G.nodes[n]['color'] for n in G.nodes]

        pos = nx.spring_layout(G)

        nx.draw(G, pos, with_labels=True, labels=labels, node_color=colors, edge_color="black",
                node_size=1000, font_size=8, font_weight="bold", ax=self.ax)

        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, font_color="black", ax=self.ax)

        plt.tight_layout()

        self.canvas.draw_idle()