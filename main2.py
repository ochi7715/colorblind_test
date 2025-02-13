import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

ishihara_test = {
    r"C:\Users\ochi7\OneDrive\Documents\colorblind test\plate_1.jpg": "12",  # Normal vision (Control Plate)
    r"C:\Users\ochi7\OneDrive\Documents\colorblind test\plate_2.jpg": "6",   # Protanomaly (Red-Green Weakness)
    r"C:\Users\ochi7\OneDrive\Documents\colorblind test\plate_3.jpg": "2",   # Deuteranomaly (Red-Green Weakness)
    r"C:\Users\ochi7\OneDrive\Documents\colorblind test\plate_4.jpg": "42",  # Tritanomaly (Blue-Yellow Weakness)
}

responses = {}

def show_plate(image_path, root, label, entry, button, panel, no_number_button):
    img = Image.open(image_path)
    img = img.resize((300, 300), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img
    
    label.config(text=f"What number do you see in the picture above?")
    entry.delete(0, tk.END)
    
    button.config(command=lambda: save_response(image_path, entry.get(), root))
    no_number_button.config(command=lambda: save_response(image_path, "No number", root))

def save_response(image_path, response, root):
    responses[image_path] = response
    plates = list(ishihara_test.keys())
    next_index = plates.index(image_path) + 1
    
    if next_index < len(plates):
        show_plate(plates[next_index], root, label, entry, button, panel, no_number_button)
    else:
        root.destroy()
        analyze_results()

def analyze_results():
    issues = []
    
    for plate, expected in ishihara_test.items():
        user_response = responses.get(plate, "")
        if user_response != expected:
            if plate.endswith("plate_2.jpg"):
                issues.append("Protanomaly")
            elif plate.endswith("plate_3.jpg"):
                issues.append("Deuteranomaly")
            elif plate.endswith("plate_4.jpg"):
                issues.append("Tritanomaly")
    
    if not issues:
        result = "No signs of color blindness detected."
    else:
        result = f"Potential color blindness detected: {', '.join(set(issues))}"  
    
    messagebox.showinfo("Test Results", result)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Ishihara Color Blindness Test")

panel = tk.Label(root)
panel.pack()

label = tk.Label(root, text="", font=("Arial", 14))
label.pack()

entry = tk.Entry(root, font=("Arial", 14))
entry.pack()

button = tk.Button(root, text="Submit", font=("Arial", 14))
button.pack()

no_number_button = tk.Button(root, text="No Number", font=("Arial", 14))
no_number_button.pack()

show_plate(list(ishihara_test.keys())[0], root, label, entry, button, panel, no_number_button)

root.mainloop()
