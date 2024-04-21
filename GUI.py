#
# Solver for a single loop magnetic core or a branched core consisting of a central part and two parallel branches
#
# Algorithm: Dr. Dmitriy Makhnovskiy, City College Plymouth, England
# GUI: ChatGPT 4.0 under guidance of Dr. Yujie Zhao, University of St. Andrews, Scotland
# 21.04.2024
#

import tkinter as tk
from tkinter import ttk

# Constants defined globally
pi = 3.1415926535897932384626433832795
mu0 = 4.0 * pi * 1.0e-7  # vacuum magnetic permeability (H/m)

def run_calculations():
    global mu0, pi

    mu = float(mu_entry.get())
    g = float(g_entry.get()) * 1.0e-3  # gap length in m
    N = int(N_entry.get())
    I = float(I_entry.get())  # current (A) through the coil
    branch = int(branch_var.get())

    results_text.delete('1.0', tk.END)  # Clear existing results

    if branch == 1:
        l1 = float(l1_entry.get()) * 1.0e-3
        A1 = float(A1_entry.get()) * 1.0e-6
        R1 = (l1 - g) / (mu * mu0 * A1) + g / (mu0 * A1)
        Flux1 = I * N / R1
        B1 = Flux1 / A1
        L1 = N ** 2 / R1
        mue1 = l1 / (mu0 * A1 * R1)

        results = f"""SINGLE LOOP CORE:
Reluctance R = {R1:.3e} 1/H
Inductance factor AL =  {1/R1:.3e} H (Inductance = AL x N^2)
Magnetic flux Ф = {Flux1:.3e} Wb
Magnetic induction B = {B1:.3e} T
Coil inductance L = {L1:.3e} H
Effective permeability mu_e = {round(mue1, 3)}"""
    elif branch == 2:
        lc = float(lc_entry.get()) * 1.0e-3
        lb = float(lb_entry.get()) * 1.0e-3
        Ac = float(Ac_entry.get()) * 1.0e-6
        Ab = float(Ab_entry.get()) * 1.0e-6
        Rc = (lc - g) / (mu * mu0 * Ac) + g / (mu0 * Ac)
        Rb = lb / (mu * mu0 * Ab)
        R2 = Rc + Rb / 2.0
        Flux2 = I * N / R2
        Bc = Flux2 / Ac
        Bb = Flux2 / (2.0 * Ab)
        L2 = N ** 2 / R2
        mue2 = (lc / Ac + lb / (2.0 * Ab)) / (mu0 * R2)

        results = f"""BRANCHED CORE:
Total reluctance R = {R2:.3e} 1/H
Inductance factor AL =  {1/R2:.3e} H (Inductance = AL x N^2)
Reluctance of the central part Rc = {Rc:.3e} 1/H
Reluctance of the branch part Rb = {Rb:.3e} 1/H
Magnetic flux in the central part Фc = {Flux2:.3e} Wb
Magnetic induction in the central part Bc = {Bc:.3e} T
Magnetic induction in the branch part Bb = {Bb:.3e} T
Coil inductance L = {L2:.3e} H
Effective permeability mu_e = {round(mue2, 3)}"""

    results_text.insert(tk.END, results)
    calculate_textbox_height(results_text, results, width=50)

def update_fields(*args):
    branch = branch_var.get()
    if branch == '1':
        l1_label.grid()
        l1_entry.grid()
        A1_label.grid()
        A1_entry.grid()
        lc_label.grid_remove()
        lc_entry.grid_remove()
        Ac_label.grid_remove()
        Ac_entry.grid_remove()
        lb_label.grid_remove()
        lb_entry.grid_remove()
        Ab_label.grid_remove()
        Ab_entry.grid_remove()
        A1_entry.grid_configure(pady=(0, 20))  # Add padding to the bottom of the last element
    elif branch == '2':
        lc_label.grid()
        lc_entry.grid()
        Ac_label.grid()
        Ac_entry.grid()
        lb_label.grid()
        lb_entry.grid()
        Ab_label.grid()
        Ab_entry.grid()
        l1_label.grid_remove()
        l1_entry.grid_remove()
        A1_label.grid_remove()
        A1_entry.grid_remove()
        Ab_entry.grid_configure(pady=(0, 20))  # Add padding to the bottom of the last element


# This function updates the height of the text box to fit the results
def calculate_textbox_height(text_widget, text, width):
    lines = text.split('\n')
    total_lines = 0
    for line in lines:
        # Calculate the number of lines this will occupy in the Text widget
        line_length = len(line)
        total_lines += -(-line_length // width)  # Ceiling division to account for partial lines

    # Update the height of the textbox
    text_widget.config(height=total_lines)


app = tk.Tk()
app.title("Magnetic Core Calculator")


# Entry widgets for parameters
mu_label = ttk.Label(app, text="μ (relative permeability)")
mu_label.grid(row=0, column=0, sticky="w")
mu_entry = ttk.Entry(app)
mu_entry.grid(row=0, column=1, sticky="w")

g_label = ttk.Label(app, text="g (Gap) [mm]")
g_label.grid(row=1, column=0, sticky="w")
g_entry = ttk.Entry(app)
g_entry.grid(row=1, column=1, sticky="w")

N_label = ttk.Label(app, text="N (number of turns)")
N_label.grid(row=2, column=0, sticky="w")
N_entry = ttk.Entry(app)
N_entry.grid(row=2, column=1, sticky="w")

I_label = ttk.Label(app, text="I (current) [A]")
I_label.grid(row=3, column=0, sticky="w")
I_entry = ttk.Entry(app)
I_entry.grid(row=3, column=1, sticky="w")

# Dropdown for branch selection
branch_label = ttk.Label(app, text="branch")
branch_label.grid(row=4, column=0, sticky="w")
branch_var = tk.StringVar()
branch_combobox = ttk.Combobox(app, textvariable=branch_var, values=('1', '2'))
branch_combobox.grid(row=4, column=1, sticky="w")
branch_var.set('1')  # Default value
branch_var.trace('w', update_fields)

# Fields for single loop core
l1_label = ttk.Label(app, text="l1 (length of core) [mm]")
l1_entry = ttk.Entry(app)
A1_label = ttk.Label(app, text="A1 (cross-section of core) [mm^2]")
A1_entry = ttk.Entry(app)

# Fields for branched core
lc_label = ttk.Label(app, text="lc (length of central part) [mm]")
lc_entry = ttk.Entry(app)
Ac_label = ttk.Label(app, text="Ac (cross-section of central part) [mm^2]")
Ac_entry = ttk.Entry(app)
lb_label = ttk.Label(app, text="lb (length of each branch) [mm]")
lb_entry = ttk.Entry(app)
Ab_label = ttk.Label(app, text="Ab (cross-section of branch part) [mm^2]")
Ab_entry = ttk.Entry(app)

# Text widget for displaying results
# Instead of a fixed height, set the initial height to some minimum value
results_text = tk.Text(app, height=5, width=50)  # Start with a height of 5 lines
results_text.grid(row=11, column=0, columnspan=2, pady=10)  # Adjust the row number as needed

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, pad=20)  # Add padding to the second column if needed
app.grid_rowconfigure(20, pad=20)  # Add padding to the bottom

# Run button
run_button = ttk.Button(app, text="Run", command=run_calculations)
# Place the 'Run' button below all the parameter fields
run_button.grid(row=15, column=0, columnspan=3, pady=5)

update_fields()  # Initialize fields visibility based on default branch selection

app.mainloop()