import re
import tkinter as tk
from tkinter import messagebox

def calculate_password_strength(password):
    # Define a dictionary to hold the strength criteria and their weights
    criteria = {
        'length': {'regex': r'.{8,}', 'weight': 2},
        'uppercase': {'regex': r'[A-Z]', 'weight': 2},
        'lowercase': {'regex': r'[a-z]', 'weight': 2},
        'digit': {'regex': r'[0-9]', 'weight': 2},
        'special_char': {'regex': r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', 'weight': 3},
    }

    # Initialize the total score
    total_score = 0

    # Initialize a list to store suggestions for improvement
    suggestions = []

    for criterion, data in criteria.items():
        if re.search(data['regex'], password):
            total_score += data['weight']
        else:
            suggestions.append(f"Add {criterion} characters")

    # Check if the password is not in a list of common passwords (you can customize this list)
    common_passwords = ["password", "123456", "qwerty", "letmein"]
    if password.lower() in common_passwords:
        suggestions.append("Avoid using common passwords")

    # Determine the overall strength based on the total score
    if total_score >= 8:
        strength = "Strong"
    elif total_score >= 5:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, suggestions

def clear_placeholder(event):
    if password_entry.get() == "Password":
        password_entry.delete(0, tk.END)
        password_entry.config(fg="black")  # Set text color to black when input is active

def restore_placeholder(event):
    if not password_entry.get():
        password_entry.insert(0, "Password")
        password_entry.config(fg="gray")  # Set text color to gray when input is not active

def check_password_strength():
    password = password_entry.get()
    if password == "Password":
        return  # Don't process the placeholder text
    
    strength, suggestions = calculate_password_strength(password)
    
    result_label.config(text=f"Password Strength: {strength}")
    
    if suggestions:
        suggestions_label.config(text="Suggestions for Improvement:")
        suggestions_text.config(state=tk.NORMAL)
        suggestions_text.delete(1.0, tk.END)
        for suggestion in suggestions:
            suggestions_text.insert(tk.END, f"- {suggestion}\n")
        suggestions_text.config(state=tk.DISABLED)
    else:
        suggestions_label.config(text="")
        suggestions_text.config(state=tk.NORMAL)
        suggestions_text.delete(1.0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x250")  # Slightly increased the height for the watermark
root.resizable(False, False)

# Configure grid rows and columns
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)  # Added an extra row for the watermark label

# Create and configure widgets
watermark_label = tk.Label(root, text="Created by Denis Dimov", fg="gray")
watermark_label.grid(row=2, column=0, columnspan=3, pady=5)

password_label = tk.Label(root, text="Enter a password:")
password_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

password_entry = tk.Entry(root, show="", fg="gray")
password_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
password_entry.insert(0, "Password")  # Add a placeholder for the password field
password_entry.bind("<FocusIn>", clear_placeholder)  # Clear the placeholder when focused
password_entry.bind("<FocusOut>", restore_placeholder)  # Restore the placeholder when focus is lost

check_button = tk.Button(root, text="Check Strength", command=check_password_strength)
check_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

result_label = tk.Label(root, text="")
result_label.grid(row=1, column=0, columnspan=3, pady=10)

suggestions_label = tk.Label(root, text="")
suggestions_label.grid(row=3, column=0, columnspan=3)  # Adjusted row position for suggestions

suggestions_text = tk.Text(root, height=5, width=40, state=tk.DISABLED)
suggestions_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")  # Adjusted row position for suggestions

# Start the GUI main loop
root.mainloop()
