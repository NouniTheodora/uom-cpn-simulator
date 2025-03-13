# Simple Petri Nets Simulator - Desktop Application

## Description
The Petri Net Simulator App is a software tool designed to facilitate the modeling, simulation, and visualization of Petri Nets. The app provides an interactive environment where users can define places and transitions, specify token distributions, and establish relationships between components. After setting up the Petri Net, users can simulate the system by executing transitions and observing how the tokens move between places in real time.

## Technology Stack
 - Python – Core programming language for logic and simulation.
 - Tkinter – For the graphical user interface.
 - NetworkX & Matplotlib – For visualizing the Petri Net.

## Future improvements
Currently, the app does not support Colored Petri Nets (CPNs), but this feature is planned for future development.

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
