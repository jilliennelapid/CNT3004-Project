# Main
# Initiates the main app call and starts all essential parts of the program
from view import View, InitView
from controller import Controller

import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        # Initializes the GUI main window
        super().__init__()

        # Sets the title of the main window
        self.title("Server File Share Application")

        view = View(self)
        self.controller = Controller(view)

        self.geometry("860x720")
        self.resizable(False,False)
        view.grid(sticky='nsew')

        self.attributes('-alpha', 0.0)
        self.attributes('-alpha', 1.0)
        self.update_idletasks()

        View.set_controller(view, self.controller)

        initView = InitView(view)
        InitView.set_controller(initView, self.controller)
        self.update_idletasks()

        InitView.connect_to_server(initView)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.controller.disconnect()
        self.destroy()

if __name__ == '__main__':
    # Creates an object from class App, which also creates the window using tkinter module
    app = App()
    app.mainloop()