import tkinter as tk
import customtkinter as ctk
import Sigup_window
import requests
from tkinter import messagebox
import bcrypt  # Library for password hashing


def validate_credentials(username, password):
    """
    Validates the username and password against a .txt file hosted remotely.
    Each line in the file should have the format: username,hashed_password
    """
    # URL to the remote file
    url = "/home/jillienne_lapid/passwords.txt"  # Replace with actual URL

    try:
        # Fetch the remote file
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the file contents
            credentials_data = response.text.splitlines()
            for line in credentials_data:
                stored_username, stored_hashed_password = line.strip().split(",")
                if username == stored_username:
                    # Check if the entered password matches the stored hashed password
                    if bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
                        return True
        else:
            print(f"Error fetching credentials file. HTTP Status: {response.status_code}")
            messagebox.showerror("Error", "Failed to access credentials file on the server.")
    except requests.RequestException as e:
        print(f"An error occurred while fetching credentials: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

    return False


def open_signup_window():
    """Opens the signup window."""
    app.destroy()  # Properly close the current window
    Sigup_window.Signup().mainloop()


class InitView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login Screen")
        self.geometry("400x300")

        # Frame
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Title Label
        title_label = ctk.CTkLabel(frame, text="Login", font=("Helvetica", 20))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Username Label and Entry
        username_label = ctk.CTkLabel(frame, text="Username:")
        username_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Enter your username")
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Password Label and Entry
        password_label = ctk.CTkLabel(frame, text="Password:")
        password_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Enter your password", show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Signup Button
        signup_button = ctk.CTkButton(frame, text="Signup", command=open_signup_window)
        signup_button.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Login Button
        login_button = ctk.CTkButton(frame, text="Login", command=self.handle_login)
        login_button.grid(row=3, column=1, padx=10, pady=10, sticky='e')

    def handle_login(self):
        """Handles login logic."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            success = validate_credentials(username, password)
            if success:
                print("Login successful!")
                self.destroy()  # Close the login window
                messagebox.showinfo("Login Status", "Login successful!")
            else:
                raise ValueError("Invalid username or password.")
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Login Status", str(e))


# Run the app
if __name__ == "__main__":
    app = InitView()
    app.mainloop()

