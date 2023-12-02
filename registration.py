import os
import tkinter as tk
from tkinter import filedialog
import csv
from PIL import Image, ImageTk
import pandas as pd

def register():
    roll_number = roll_number_entry.get()
    name = name_entry.get()
    fingerprint_path = fingerprint_entry.get()

    # Check if all fields are filled
    if roll_number and name and fingerprint_path:
        # Read existing data from the CSV file
        existing_data = []
        with open("registration_data.csv", mode="r") as file:
            reader = csv.reader(file)
            existing_data = list(reader)

        # Check for duplicate Roll Number
        roll_numbers = [row[0] for row in existing_data]
        if roll_number in roll_numbers:
            status_label.config(text=f"Error: Roll Number {roll_number} already exists. Please choose a different roll number.", fg="red")
            return

        # Append the registration details to the CSV file
        with open("registration_data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([roll_number, name, fingerprint_path])

        # Create a new folder for fingerprint images if it doesn't exist
        folder_path = "fingerprint_images"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save the fingerprint image to the folder with the filename "rollno_name.jpg"
        new_filename = f"{roll_number}_{name}.jpg"
        new_filepath = os.path.join(folder_path, new_filename)
        save_image(fingerprint_path, new_filepath)

        # Clear the entry fields
        roll_number_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        fingerprint_entry.delete(0, tk.END)

        # Inform the user about successful registration
        status_label.config(text="Registration successful!", fg="green")

    else:
        # Inform the user to fill in all fields
        status_label.config(text="Error: Please fill in all fields.", fg="red")

def browse_file():
    # Open a file dialog to select a fingerprint image in jpg format
    file_path = filedialog.askopenfilename(title="Select Fingerprint Image", filetypes=[("Image files", "*.jpg;*.jpeg;*.bmp")])
    fingerprint_entry.delete(0, tk.END)
    fingerprint_entry.insert(0, file_path)

    # Display the selected image on the GUI
    display_image(file_path)

def save_image(src_path, dest_path):
    # Open and convert the image to RGB mode
    img = Image.open(src_path).convert("RGB")

    # Save the image to the specified destination path
    img.save(dest_path)

def display_image(file_path):
    # Open and display the image in the GUI
    img = Image.open(file_path)
    img = img.resize((200, 200), Image.ANTIALIAS)  # Resize the image
    img = ImageTk.PhotoImage(img)

    # Update the image label
    image_label.config(image=img)
    image_label.image = img

def display_all_entries():
    # Read all entries from the CSV file into a DataFrame
    df = pd.read_csv("registration_data.csv", header=None, names=['Roll Number', 'Name', 'Fingerprint Path'])

    # Create a temporary CSV file
    temp_csv_path = "all_entries.csv"

    # Export the DataFrame to the temporary CSV file
    df.to_csv(temp_csv_path, index=False, header=False)

    # Open the temporary CSV file using the default associated program
    os.startfile(temp_csv_path)

    # Inform the user about the CSV display
    status_label.config(text="CSV file opened.", fg="green")

# Create the main window
root = tk.Tk()
root.title("Fingerprint Registration")

# Calculate screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the initial size and position of the window
window_width = 500
window_height = 600
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.configure(bg='#2E3B4E')  # Set background color

# Create and place widgets centered in the window
font_size = 14

tk.Label(root, text="Roll Number:", bg='#2E3B4E', fg='white', font=("Helvetica", font_size)).pack(anchor=tk.CENTER)
roll_number_entry = tk.Entry(root, bg='#445566', fg='white', insertbackground='white', relief='flat', font=("Helvetica", font_size))
roll_number_entry.pack(pady=5, anchor=tk.CENTER)

tk.Label(root, text="Name:", bg='#2E3B4E', fg='white', font=("Helvetica", font_size)).pack(anchor=tk.CENTER)
name_entry = tk.Entry(root, bg='#445566', fg='white', insertbackground='white', relief='flat', font=("Helvetica", font_size))
name_entry.pack(pady=5, anchor=tk.CENTER)

tk.Label(root, text="Fingerprint Image:", bg='#2E3B4E', fg='white', font=("Helvetica", font_size)).pack(anchor=tk.CENTER)

# Entry field for the fingerprint path
fingerprint_entry = tk.Entry(root, bg='#445566', fg='white', insertbackground='white', relief='flat', font=("Helvetica", font_size))
fingerprint_entry.pack(pady=5, anchor=tk.CENTER)

# Button to browse and select a fingerprint image
browse_button = tk.Button(root, text="Browse", command=browse_file, bg='#4CAF50', fg='white', relief='flat', font=("Helvetica", font_size))
browse_button.pack(pady=10, anchor=tk.CENTER)

# Image label to display the selected fingerprint image
image_label = tk.Label(root, bg='#2E3B4E')
image_label.pack(anchor=tk.CENTER)

# Button to register the user
register_button = tk.Button(root, text="Register", command=register, bg='#3498db', fg='white', relief='flat', font=("Helvetica", font_size))
register_button.pack(pady=10, anchor=tk.CENTER)

# Button to display all registered entries
display_entries_button = tk.Button(root, text="Display All Entries", command=display_all_entries, bg='#3498db', fg='white', relief='flat', font=("Helvetica", font_size))
display_entries_button.pack(pady=10, anchor=tk.CENTER)

# Status label to show registration status
status_label = tk.Label(root, text="", bg='#2E3B4E', fg='white', font=("Helvetica", font_size))
status_label.pack(anchor=tk.CENTER)

# Start the GUI event loop
root.mainloop()