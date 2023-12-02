import os
import tkinter as tk
from tkinter import ttk
from subprocess import call

def register():
    call(["python", "registration.py"])

def detect():
    call(["python", "main.py"])

def export_csv():
    call(["python", "process_csv.py"])  # Replace "export_csv.py" with the actual script for exporting CSV

root = tk.Tk()
root.title("Biometric Attendance System")  # Set the title

# Adjust the size of the window
window_width = 600
window_height = 250  # Increased height to accommodate the third button

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Heading
heading_label = tk.Label(root, text="BIOMETRIC ATTENDANCE SYSTEM", font=('Helvetica', 16, 'bold'))
heading_label.pack(pady=10)

# Create a themed style for the buttons
style = ttk.Style()

# Configure the style for the buttons
style.configure('TButton', padding=5, relief="flat", font=('Helvetica', 12), background='#E0E0E0')

# Function to handle the registration button click
registration_button = ttk.Button(root, text="Registration", command=register, style='TButton')
registration_button.pack(pady=10)  # Add some padding

# Function to handle the detection button click
detection_button = ttk.Button(root, text="Detection", command=detect, style='TButton')
detection_button.pack(pady=10)  # Add some padding

# Function to handle the export CSV button click
export_csv_button = ttk.Button(root, text="Export CSV", command=export_csv, style='TButton')
export_csv_button.pack(pady=10)  # Add some padding

# Run the GUI
root.mainloop()
