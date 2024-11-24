
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import requests  # For HTTP requests
import os  # For handling temporary file creation and deletion
import modified_view


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
        Saves the inputted username and password to a remote repository.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:  # Ensure fields are not empty
            temp_file_path = "passwords_temp.txt"
            
            # Save credentials temporarily to a file
            with open(temp_file_path, "w") as file:
                file.write(f"{username},{password}\n")

            # Upload the file to the remote repository
            try:
                url = "https://your-remote-repository.com/upload"  # Replace with your endpoint
                with open(temp_file_path, "rb") as file:
                    response = requests.post(url, files={"file": file})

                # Check the response
                if response.status_code == 200:
                    print("Credentials saved to remote repository successfully!")
                    tk.messagebox.showinfo("Success", "Credentials saved successfully!")
                else:
                    print(f"Failed to upload credentials. HTTP Status: {response.status_code}")
                    tk.messagebox.showerror("Error", "Failed to save credentials to remote repository.")

            except Exception as e:
                print(f"An error occurred: {e}")
                tk.messagebox.showerror("Error", f"An error occurred: {e}")

            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

            self.destroy()
            modified_view.InitView()  # Open the InitView window from modified_view

        else:
            print("Both fields must be filled.")
            tk.messagebox.showerror("Error", "Both fields must be filled.")

    def on_close(self):
        """
        Handles the close button (X) event.
        """
        self.destroy()  # Close the current window
        modified_view.InitView()  # Open the InitView window


# Run the Signup view if this file is executed directly
if __name__ == "__main__":
    app = Signup()
    app.mainloop()
