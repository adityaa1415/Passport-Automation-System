import tkinter as tk
import sqlite3
import random
from tkinter import messagebox

# Function to create a database and table if not exists
def create_table():
    conn = sqlite3.connect('passport_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passports
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  age INTEGER,
                  gender TEXT,
                  country TEXT,
                  uid TEXT,
                  status TEXT,
                  expiration_date TEXT)''')
    conn.commit()
    conn.close()

# Function to apply for passport
def apply_passport():
    # Create a new window for entering details
    apply_window = tk.Toplevel(root)
    apply_window.title("Apply for Passport")

    # Labels and Entry fields for details
    labels = ["Name:", "Age:", "Gender:", "Country:", "UID:"]
    entries = []
    for i, label_text in enumerate(labels):
        tk.Label(apply_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(apply_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    # Function to save details to the database
    def save_details():
        name = entries[0].get()
        age = int(entries[1].get())
        gender = entries[2].get()
        country = entries[3].get()
        uid = entries[4].get()

        # Generate a random expiration date in 2026
        expiration_date = f"{random.randint(2026, 2026)}-{random.randint(1, 12)}-{random.randint(1, 28)}"

        # Insert details into the database
        conn = sqlite3.connect('passport_database.db')
        c = conn.cursor()
        c.execute("INSERT INTO passports (name, age, gender, country, uid, status, expiration_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (name, age, gender, country, uid, "active", expiration_date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Passport application saved successfully!")
        apply_window.destroy()

    # Button to save details
    tk.Button(apply_window, text="Save", command=save_details).grid(row=len(labels), columnspan=2, padx=10, pady=10)

# Function to renew passport
def renew_passport():
    # Create a new window for entering UID
    renew_window = tk.Toplevel(root)
    renew_window.title("Renew Passport")

    tk.Label(renew_window, text="Enter UID:").grid(row=0, column=0, padx=10, pady=5)
    uid_entry = tk.Entry(renew_window)
    uid_entry.grid(row=0, column=1, padx=10, pady=5)

    # Function to update expiration date and status
    def update_expiration():
        uid = uid_entry.get()

        # Check if UID exists in the database
        conn = sqlite3.connect('passport_database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM passports WHERE uid=?", (uid,))
        data = c.fetchone()
        if data:
            if data[6] == "active":
                messagebox.showinfo("Status", "Passport is already active.")
                renew_window.destroy()
            elif data[6] == "pending":
                new_expiration_date = f"{int(data[7].split('-')[0]) + 2}-{data[7].split('-')[1]}-{data[7].split('-')[2]}"
                c.execute("UPDATE passports SET expiration_date=?, status=? WHERE uid=?", (new_expiration_date, "active", uid))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Passport renewed successfully!")
                renew_window.destroy()
        else:
            messagebox.showerror("Error", "UID not found in the database.")

    # Button to update expiration date
    tk.Button(renew_window, text="Renew", command=update_expiration).grid(row=1, columnspan=2, padx=10, pady=10)

# Function to check status
def check_status():
    # Create a new window for entering UID
    status_window = tk.Toplevel(root)
    status_window.title("Check Application Status")

    tk.Label(status_window, text="Enter UID:").grid(row=0, column=0, padx=10, pady=5)
    uid_entry = tk.Entry(status_window)
    uid_entry.grid(row=0, column=1, padx=10, pady=5)

    # Function to display status
    def display_status():
        uid = uid_entry.get()

        # Check if UID exists in the database
        conn = sqlite3.connect('passport_database.db')
        c = conn.cursor()
        c.execute("SELECT status FROM passports WHERE uid=?", (uid,))
        data = c.fetchone()
        if data:
            messagebox.showinfo("Status", f"Status for UID {uid}: {data[0]}")
            status_window.destroy()
        else:
            messagebox.showerror("Error", "UID not found in the database.")

    # Button to display status
    tk.Button(status_window, text="Check Status", command=display_status).grid(row=1, columnspan=2, padx=10, pady=10)

# Function to check details
def check_details():
    # Create a new window for entering UID
    details_window = tk.Toplevel(root)
    details_window.title("Check Details")

    tk.Label(details_window, text="Enter UID:").grid(row=0, column=0, padx=10, pady=5)
    uid_entry = tk.Entry(details_window)
    uid_entry.grid(row=0, column=1, padx=10, pady=5)

    # Function to display details
    def display_details():
        uid = uid_entry.get()

        # Check if UID exists in the database
        conn = sqlite3.connect('passport_database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM passports WHERE uid=?", (uid,))
        data = c.fetchone()
        if data:
            details_text = f"Name: {data[1]}\n"
            details_text += f"Age: {data[2]}\n"
            details_text += f"Gender: {data[3]}\n"
            details_text += f"Country: {data[4]}\n"
            details_text += f"UID: {data[5]}\n"
            details_text += f"Status: {data[6]}\n"
            details_text += f"Expiration Date: {data[7]}\n"
            tk.Label(details_window, text=details_text).grid(row=1, columnspan=2, padx=10, pady=10)
        else:
            messagebox.showerror("Error", "UID not found in the database.")

    # Button to display details
    tk.Button(details_window, text="Check Details", command=display_details).grid(row=1, columnspan=2, padx=10, pady=10)

# Main window
root = tk.Tk()
root.title("Passport Application")
root.geometry("400x300")

# Center the window on the screen
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth()/2 - window_width/2)
position_down = int(root.winfo_screenheight()/2 - window_height/2)
root.geometry("+{}+{}".format(position_right, position_down))

# Create database table
create_table()

# Buttons
button_apply = tk.Button(root, text="Apply for Passport", command=apply_passport)
button_apply.pack(pady=10)
button_renew = tk.Button(root, text="Renew Passport", command=renew_passport)
button_renew.pack(pady=10)
button_status = tk.Button(root, text="Check Application Status", command=check_status)
button_status.pack(pady=10)
button_details = tk.Button(root, text="Check Details", command=check_details)
button_details.pack(pady=10)
button_exit = tk.Button(root, text="Exit", command=root.destroy)
button_exit.pack(pady=10)

root.mainloop()
