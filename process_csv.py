import os
import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime

def export_csv():
    filter_date = date_entry.get()
    
    if not filter_date:
        result_label.config(text="Please enter a date.", fg="red")
        return
    
    try:
        # Convert the input date to the desired format
        datetime.strptime(filter_date, "%Y-%m-%d")
    except ValueError:
        result_label.config(text="Invalid date format. Use YYYY-MM-DD.", fg="red")
        return
    
    # Read the CSV file without specifying column names
    df = pd.read_csv('recognized_fingerprints.csv', header=None)

    # Convert the second column to datetime for accurate filtering
    df[1] = pd.to_datetime(df[1], errors='coerce')

    # Filter based on date
    filtered_df = df[df[1] == filter_date]

    # Extract the first column
    result_df = filtered_df[[0]]

    # Sort the data based on the first column
    result_df = result_df.sort_values(by=[0])

    # Extract the date in the desired format (without special characters)
    filtered_date_str = filter_date.replace('-', '')

    # Create the "filtered" folder if it doesn't exist
    filtered_folder = 'filtered'
    if not os.path.exists(filtered_folder):
        os.makedirs(filtered_folder)

    # Save the result to a new CSV file inside the "filtered" folder
    output_csv_path = os.path.join(filtered_folder, f'{filtered_date_str}_filtered.csv')
    result_df.to_csv(output_csv_path, index=False, header=False)

    # Display the result
    result_label.config(text=f"Filtered and sorted CSV saved to: {output_csv_path}", fg="green")

    # Open the CSV file
    os.startfile(output_csv_path)

root = tk.Tk()
root.title("CSV Export App")  # Set the title

# Adjust the size of the window
window_width = 400
window_height = 150

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create a themed style for the buttons
style = ttk.Style()

# Configure the style for the buttons
style.configure('TButton', padding=5, relief="flat", font=('Helvetica', 12), background='#3498db', foreground='black')

# Entry widget for the user to input the date
date_label = tk.Label(root, text="Enter Date (YYYY-MM-DD):")
date_label.pack()
date_entry = tk.Entry(root)
date_entry.pack(pady=5)

# Button to export CSV
export_csv_button = ttk.Button(root, text="Export CSV", command=export_csv, style='TButton')
export_csv_button.pack(pady=10)

# Label to display the result of the CSV export
result_label = tk.Label(root, text="")
result_label.pack()

# Run the GUI
root.mainloop()
