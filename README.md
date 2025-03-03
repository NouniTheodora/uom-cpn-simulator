# Colored Petri Net Simulator - Desktop Application

## Description

The Colored Petri Net Simulator is a desktop application designed to help users define, visualize, and simulate Colored Petri Nets (CPNs). It allows users to input the structure of a Petri Net via the console, including places, transitions, and edges, and then provides an interactive graphical interface to visualize and manipulate token movements.

## Features

🔹 User-Defined Petri Net Input – The user can specify places (with token counts and colors), transitions, and edges via the console.

🔹 Graphical Visualization – The application renders the Petri Net using NetworkX and Matplotlib, displaying places as circles and transitions as squares.

🔹 Token Management – Users can add tokens to places dynamically through an interactive UI.

🔹 Transition Firing Simulation – The application processes token flow based on Petri Net rules, removing tokens from input places and adding them to output places when a transition fires.

🔹 Simple and Interactive UI – A Tkinter-based GUI provides buttons for adding tokens, firing transitions, and updating the simulation.

🔹 Real-Time Updates – Every transition firing updates the graphical representation of the Petri Net.

## Technology Stack
 - Python – Core programming language for logic and simulation.
 - Tkinter – For the graphical user interface.
 - NetworkX & Matplotlib – For visualizing the Petri Net.
 - Console Input Handling – For initial Petri Net configuration.

## 🚀 Setup Instructions (Local Development)

Clone the repository
```bash
git clone https://github.com/NouniTheodora/uom-cpn-simulator.git
```
Create and activate a Virtual Environment with venv

- For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

- For Windows:

```bash
python3 -m venv venv
venv\Scripts\activate
```

Install dependencies

```bash
pip3 install -r requirements.txt
```

Run the application

```bash
python3 main.py
```

Deactivate the Virtual Environment (when finished)

```bash
deactivate
```