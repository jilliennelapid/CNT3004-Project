import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import bcrypt # Library for encryption
import os


class Signup(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Save Credentials")
        self.geometry("400x300")

        # Handle close button
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Frame
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Title Label
        title_label = ctk.CTkLabel(frame, text="Register Credentials", font=("Helvetica", 20))
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

        # Save Button
        save_button = ctk.CTkButton(frame, text="Save", command=self.save_credentials)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_credentials(self):
        """
        Saves the inputted username and hashed password to passwords.txt.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:  # Ensure fields are not empty
            # Ensures passwords are not safe in plain text on the credentials txt
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            credentials = f"{username},{hashed_password.decode()}\n"

            # Ensure the file exists
            if not os.path.exists("passwords.txt"):
                open("passwords.txt", "w").close()

            # Save the hashed password
            with open("passwords.txt", "a") as file:
                file.write(credentials)

            print("Credentials saved securely!")
            tk.messagebox.showinfo("Success", "Credentials saved securely!")
            self.destroy()
        else:
            print("Both fields must be filled.")
            tk.messagebox.showerror("Error", "Both fields must be filled.")

    def on_close(self):
        """
        Handles the close button (X) event.
        """
        self.destroy()  # Close the current window


# Run the Signup view if this file is executed directly
if __name__ == "__main__":
    app = Signup()
    app.mainloop()
