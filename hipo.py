import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import random

def get_user_input(depth, T_superficiala, time_limit, neopren_type):
    try:
        depth = float(depth)
        T_superficiala = float(T_superficiala)
        time_limit = int(time_limit)
        
        if neopren_type == 'usor':
            R_neopren = 0.4
        elif neopren_type == 'mediu':
            R_neopren = 0.6
        elif neopren_type == 'greu':
            R_neopren = 0.8
        else:
            raise ValueError("Echipament invalid")
        return depth, T_superficiala, time_limit, R_neopren
    except ValueError as ve:
        messagebox.showerror("Eroare de input", f"Te rugăm să introduci valori valide: {ve}")
        return None

def T_apa(depth, T_superficiala, k):
    T_superficiala += random.uniform(-2, 2) 
    return T_superficiala - k * depth

def heat_loss(T_body, T_apa, A, h, R_neopren, R_air_layer):
    return h * A * (T_body - T_apa) + (T_body - T_apa) / R_neopren + (T_body - T_apa) / R_air_layer

def simulate_body_temperature(depth, time, T_body, T_superficiala, k, A, h, R_neopren, R_air_layer, fatigue_rate):
    T_apa_value = T_apa(depth, T_superficiala, k)
    body_temperature = np.zeros(len(time))
    body_temperature[0] = T_body
    
    for i in range(1, len(time)):
        Q = heat_loss(body_temperature[i-1], T_apa_value, A, h, R_neopren, R_air_layer)
        body_temperature[i] = body_temperature[i-1] - (Q * (time[i] - time[i-1]) / 1000) 
     
        body_temperature[i] -= fatigue_rate * (time[i] - time[i-1])
        
        time[i] = decompression(time[i], depth)
       
        if body_temperature[i] < 30:
            body_temperature[i] = 30  
      
        if body_temperature[i] < 32:
            print(f"Avertisment: Hipotermie la {time[i]} minute! Temperatura corpului este {body_temperature[i]:.2f} °C")

    return body_temperature

def decompression(time, depth):
    ascent_rate = 0.5  
    if depth > 10:
        return max(0, time - (depth / ascent_rate))  
    return time

def plot_graph(depth, T_superficiala, time_limit, R_neopren):
    T_body = 37  # Temperatura corpului in grade Celsius
    h = 50  # Coeficient de transfer de caldura (W/m^2K)
    A = 1.8  # Suprafata corpului expusa (m^2)
    R_air_layer = 0.7  # Rezistenta stratului de aer (m^2K/W)
    k = 0.05  # Coeficient de scadere a temperaturii (°C/m)
    fatigue_rate = 0.1  # Rata de oboseală a scufundătorului (scăderea temperaturii în timp)

    time = np.linspace(0, time_limit, time_limit + 1)

    T_body_results = simulate_body_temperature(depth, time, T_body, T_superficiala, k, A, h, R_neopren, R_air_layer, fatigue_rate)

    plt.plot(time, T_body_results, label=f'Depth = {depth}m')
    plt.xlabel('Timp (minute)')
    plt.ylabel('Temperatura corpului (°C)')
    plt.title('Evoluția temperaturii corpului în timpul scufundării')
    plt.grid(True)
    plt.legend()
    plt.show()

def start_simulation():
    depth = entry_depth.get()
    T_superficiala = entry_temp.get()
    time_limit = entry_time.get()
    neopren_type = var_neopren.get()

    user_input = get_user_input(depth, T_superficiala, time_limit, neopren_type)
    if user_input:
        depth, T_superficiala, time_limit, R_neopren = user_input
        plot_graph(depth, T_superficiala, time_limit, R_neopren)

root = tk.Tk()
root.title("Simulare Hipotermie în Scufundare")
root.geometry("400x400")

tk.Label(root, text="Adâncimea scufundării (m):").pack()
entry_depth = tk.Entry(root)
entry_depth.pack()

tk.Label(root, text="Temperatura apei la suprafață (°C):").pack()
entry_temp = tk.Entry(root)
entry_temp.pack()

tk.Label(root, text="Timpul scufundării (minute):").pack()
entry_time = tk.Entry(root)
entry_time.pack()

tk.Label(root, text="Alege echipamentul de scufundare:").pack()
var_neopren = tk.StringVar(value="mediu") 
neopren_options = ["usor", "mediu", "greu"]
for option in neopren_options:
    tk.Radiobutton(root, text=option.capitalize(), variable=var_neopren, value=option).pack()

btn_simulare = tk.Button(root, text="Începe simularea", command=start_simulation)
btn_simulare.pack()

root.mainloop()
