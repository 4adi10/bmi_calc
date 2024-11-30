import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime


bmi_history = {"Metric": [], "Imperial": []}


def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        
        if unit_var.get() == "Metric":
            height = float(height_entry.get()) / 100  
            bmi = weight / (height ** 2)
        else:
            feet = float(feet_entry.get())
            inches = float(inches_entry.get())
            height = (feet * 12 + inches) * 0.0254  
            bmi = (weight * 0.453592) / (height ** 2)  

        
        if bmi < 18.5:
            category = "Underweight"
            result_label.config(fg="blue", text=f"Your BMI is {bmi:.2f} ({category})")
            motivational_label.config(text="You might need to eat a bit more!")
        elif 18.5 <= bmi < 24.9:
            category = "Healthy"
            result_label.config(fg="green", text=f"Your BMI is {bmi:.2f} ({category})")
            motivational_label.config(text="Great job maintaining your health!")
        elif 25 <= bmi < 29.9:
            category = "Overweight"
            result_label.config(fg="orange", text=f"Your BMI is {bmi:.2f} ({category})")
            motivational_label.config(text="You're doing good, aim for more activity!")
        else:
            category = "Obese"
            result_label.config(fg="red", text=f"Your BMI is {bmi:.2f} ({category})")
            motivational_label.config(text="Small steps daily lead to great results!")

        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bmi_history[unit_var.get()].append((timestamp, bmi))
        update_log_and_graph()
    except ValueError:
        result_label.config(fg="red", text="Invalid input! Please enter valid numbers.")


def update_log_and_graph():
    
    log_text.delete("1.0", tk.END)
    for date, bmi in bmi_history[unit_var.get()]:
        log_text.insert(tk.END, f"{date}: BMI {bmi:.2f}\n")

    
    dates = [entry[0] for entry in bmi_history[unit_var.get()]]
    bmis = [entry[1] for entry in bmi_history[unit_var.get()]]
    ax.clear()
    ax.plot(dates, bmis, marker='o', linestyle='-', color='purple')
    ax.set_title(f"BMI History ({unit_var.get()})")
    ax.set_xlabel("Date & Time")
    ax.set_ylabel("BMI")
    ax.tick_params(axis='x', rotation=45)
    canvas.draw()


def toggle_unit():
    if unit_var.get() == "Metric":
        height_label.grid(row=2, column=0, sticky="w")
        height_entry.grid(row=2, column=1)
        feet_label.grid_forget()
        feet_entry.grid_forget()
        inches_label.grid_forget()
        inches_entry.grid_forget()
        weight_label.config(text="Weight (kg):")
    else:
        height_label.grid_forget()
        height_entry.grid_forget()
        feet_label.grid(row=2, column=0, sticky="w")
        feet_entry.grid(row=2, column=1)
        inches_label.grid(row=2, column=2, sticky="w")
        inches_entry.grid(row=2, column=3)
        weight_label.config(text="Weight (lbs):")
    
    bmi_history[unit_var.get()].clear()
    update_log_and_graph()


root = tk.Tk()
root.title("BMI Calculator")
root.geometry("900x600")


welcome_label = tk.Label(root, text="Welcome to the BMI Calculator!", font=("Arial", 16), pady=10)
welcome_label.pack()


frame = tk.Frame(root, padx=20, pady=10)
frame.pack(fill="x")

unit_var = tk.StringVar(value="Metric")


tk.Label(frame, text="Select Units:").grid(row=0, column=0, sticky="w")
tk.Radiobutton(frame, text="Metric (kg, cm)", variable=unit_var, value="Metric", command=toggle_unit).grid(row=0, column=1)
tk.Radiobutton(frame, text="Imperial (lbs, ft/in)", variable=unit_var, value="Imperial", command=toggle_unit).grid(row=0, column=2)


weight_label = tk.Label(frame, text="Weight (kg):")
weight_label.grid(row=1, column=0, sticky="w")
weight_entry = tk.Entry(frame)
weight_entry.grid(row=1, column=1)

height_label = tk.Label(frame, text="Height (cm):")
height_label.grid(row=2, column=0, sticky="w")
height_entry = tk.Entry(frame)
height_entry.grid(row=2, column=1)

feet_label = tk.Label(frame, text="Height (ft):")
feet_entry = tk.Entry(frame)
inches_label = tk.Label(frame, text="Height (in):")
inches_entry = tk.Entry(frame)


calc_button = tk.Button(frame, text="Calculate BMI", command=calculate_bmi)
calc_button.grid(row=3, columnspan=4, pady=10)


result_label = tk.Label(frame, text="", font=("Arial", 12), pady=10)
result_label.grid(row=4, columnspan=4)


motivational_label = tk.Label(frame, text="", font=("Arial", 10, "italic"))
motivational_label.grid(row=5, columnspan=4)


history_frame = tk.Frame(root, padx=20, pady=10)
history_frame.pack(fill="both", expand=True)


log_label = tk.Label(history_frame, text="BMI Log:", font=("Arial", 12, "bold"))
log_label.pack(anchor="w")

log_text = tk.Text(history_frame, height=10, wrap="word")
log_text.pack(fill="x", pady=5)


fig, ax = plt.subplots(figsize=(6, 3))
canvas = FigureCanvasTkAgg(fig, master=history_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)


toggle_unit()


root.mainloop()
