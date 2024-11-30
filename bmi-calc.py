import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from datetime import datetime

bmi_records = {"Metric": [], "Imperial": []}

def calculate_bmi():
    try:
        unit_system = unit_var.get()
        if unit_system == "Metric":
            weight = float(weight_entry.get())
            height_cm = float(height_entry.get())
            height_m = height_cm / 100  
            bmi = weight / (height_m ** 2)
        elif unit_system == "Imperial":
            weight = float(weight_entry.get())
            height_ft = float(height_ft_entry.get())
            height_in = float(height_in_entry.get())
            total_height_in = (height_ft * 12) + height_in
            bmi = (weight / (total_height_in ** 2)) * 703  
        else:
            raise ValueError("Invalid unit system")
        
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bmi_records[unit_system].append((timestamp, bmi))

        
        result_label.config(text=f"Your BMI is: {bmi:.2f}\nCategory: {category}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

def switch_unit_system():
    unit_system = unit_var.get()
    if unit_system == "Metric":
        weight_label.config(text="Weight (kg):")
        height_label.config(text="Height (cm):")
        height_entry.grid(row=2, column=1, padx=10, pady=5)
        height_ft_label.grid_forget()
        height_ft_entry.grid_forget()
        height_in_label.grid_forget()
        height_in_entry.grid_forget()
    elif unit_system == "Imperial":
        weight_label.config(text="Weight (lbs):")
        height_label.config(text="Height (ft and in):")
        height_entry.grid_forget()
        height_ft_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        height_ft_entry.grid(row=2, column=1, padx=80, pady=5, sticky="w")
        height_in_label.grid(row=2, column=1, padx=160, pady=5, sticky="w")
        height_in_entry.grid(row=2, column=1, padx=230, pady=5, sticky="w")

def plot_bmi_trend():
    unit_system = unit_var.get()
    if not bmi_records[unit_system]:
        messagebox.showinfo("No Data", f"No BMI records available for {unit_system} system.")
        return

    timestamps, bmi_values = zip(*bmi_records[unit_system])

    plt.figure(figsize=(8, 5))
    plt.plot(timestamps, bmi_values, marker="o", label=f"BMI ({unit_system})")
    plt.xlabel("Time")
    plt.ylabel("BMI")
    plt.title("BMI Trend Over Time")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.legend()
    plt.show()

root = tk.Tk()
root.title("BMI Calculator")

unit_var = tk.StringVar(value="Metric")
metric_rb = ttk.Radiobutton(root, text="Metric (kg, cm)", variable=unit_var, value="Metric", command=switch_unit_system)
imperial_rb = ttk.Radiobutton(root, text="Imperial (lbs, ft, in)", variable=unit_var, value="Imperial", command=switch_unit_system)
metric_rb.grid(row=0, column=0, padx=10, pady=5, sticky="w")
imperial_rb.grid(row=0, column=1, padx=10, pady=5, sticky="w")

weight_label = ttk.Label(root, text="Weight (kg):")
weight_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
weight_entry = ttk.Entry(root)
weight_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

height_label = ttk.Label(root, text="Height (cm):")
height_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
height_entry = ttk.Entry(root)
height_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

height_ft_label = ttk.Label(root, text="ft:")
height_ft_entry = ttk.Entry(root, width=5)
height_in_label = ttk.Label(root, text="in:")
height_in_entry = ttk.Entry(root, width=5)

calculate_button = ttk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

plot_button = ttk.Button(root, text="View BMI Trend", command=plot_bmi_trend)
plot_button.grid(row=4, column=0, columnspan=2, pady=10)

result_label = ttk.Label(root, text="", font=("Arial", 12))
result_label.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
