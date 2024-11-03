from model import Model
from view import View
from controller import Controller

import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        # Initializes the GUI main window
        super().__init__()

        # Sets the title of the main window
        self.title("Server File Share Application")

        # Initializes instances of the Model, View, and Controller classes.
        # Passes the model and view to the controller
        model = Model()
        view = View(self)
        controller = Controller(model, view)

        self.geometry("860x760")
        view.grid(sticky='nsew')

        self.attributes('-alpha', 0.0)
        self.center_window()
        self.attributes('-alpha', 1.0)

        View.set_controller(view, controller)

    def center_window(self):
        self.update_idletasks()  # Ensure all widgets are rendered
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the geometry of the window
        self.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == '__main__':
    # Creates an object from class App, which also creates the window using tkinter module
    app = App()
    app.mainloop()
