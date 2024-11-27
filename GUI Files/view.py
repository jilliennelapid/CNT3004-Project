# View
# Contains all code for drawing the GUI window and aiding its functionality
import tkinter as tk
import bcrypt  # Library for password hashing
import customtkinter as ctk
from tkinter import font, filedialog,  messagebox
import os
import threading
import time
import json
import requests
import asyncio

FORMAT = "utf-8"
FILE_STORAGE_DIR = "/home/jillienne_lapid/server_files"

# Server path will be created in google cloud VM instance.
FS_DIR = os.path.expanduser("~/passwords.txt")

class View(tk.Frame):
    task_complete = False

    def __init__(self, parent):
        super().__init__(parent)

        # Initialize the controller to None
        self.controller = None
        self.files = None

        # Sets the title of the main window
        parent.title("Server File Share Application")
        parent.geometry("860x720")
        parent.resizable(False, False)
        self.grid(sticky='nsew')

        parent.attributes('-alpha', 0.0)
        parent.attributes('-alpha', 1.0)

        """attributes pertaining to the whole window"""
        globalFont = font.Font(family='Helvetica')
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        """Frame containing Top Left and Top Right Frames"""
        self.window_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.window_frame.grid(sticky='nsew')

        self.window_frame.grid_rowconfigure(0, weight=1)
        self.window_frame.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand
        self.window_frame.grid_columnconfigure(1, weight=0)  # Column 1 does not expand

        """Top Left Frame"""
        self.top_frame_left = ctk.CTkFrame(self.window_frame, fg_color='transparent')
        self.top_frame_left.grid(row=0, column=0, sticky='w', padx=10)

        self.label_FS = ctk.CTkLabel(self.top_frame_left, text='File Share', font=(globalFont, 45, 'bold'))
        self.label_FS.grid(row=0, column=0, sticky='w', padx=20, pady=10)

        #self.label_SCS = ctk.CTkLabel(self.top_frame_left, text='Server Connection Status', font=(globalFont, 11))
        #self.label_SCS.grid(row=2, column=0, sticky='w', padx=20)

        """Top Right Frame"""
        self.top_frame_right = ctk.CTkFrame(self.window_frame, fg_color='transparent')
        self.top_frame_right.grid(row=0, column=1, sticky='se', padx=10)

        self.server_dir_button = ctk.CTkButton(self.top_frame_right, corner_radius=5, text='View Server Directory',
                                               font=(globalFont, 18, 'bold'), fg_color='#59b1f0', hover_color='#3977e3',
                                               text_color='#fafcff', border_spacing=10, height=50, command=self.open_server_dir_edit)

        self.server_dir_button.grid(row=0, column=1, rowspan=2, sticky='e', padx=20, pady=10)

        """Upload Widgets Frame"""
        self.upload_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.upload_frame.grid(row=2, column=0, sticky='nsew', padx=30, pady=(30, 0))

        self.upload_frame.grid_columnconfigure(0, weight=0)
        self.upload_frame.grid_columnconfigure(1, weight=1)

        self.upload_frame.grid_rowconfigure(0, weight=0)
        self.upload_frame.grid_rowconfigure(1, weight=1)
        self.upload_frame.grid_rowconfigure(2, weight=1)

        self.server_dir_button = ctk.CTkButton(self.upload_frame, corner_radius=5, text='Upload File',
                                               font=(globalFont, 25, 'bold'), fg_color='#59b1f0', hover_color='#3977e3',
                                               text_color='#fafcff', border_spacing=10, width=270, height=60,
                                               command=self.open_file_dialog)

        self.server_dir_button.grid(row=0, column=0, sticky='w')

        ## Current File Upload Statistics Frame
        self.upload_current_frame = ctk.CTkFrame(self.upload_frame, border_width=2, width=270, border_color='#59b1f0',
                                                 fg_color='transparent')
        self.upload_current_frame.grid_propagate(False)
        self.upload_current_frame.grid(row=1, column=0, rowspan=2, sticky='nsew', pady=(20, 0))

        self.upload_current_frame.grid_columnconfigure(0, weight=1)
        self.upload_current_frame.grid_columnconfigure(1, weight=0)

        self.label_US = ctk.CTkLabel(self.upload_current_frame, text='Current Upload Statistics',
                                  font=(globalFont, 17, 'bold'))
        self.label_US.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=(10,0))

        ### Upload Statistics Labels
        self.label_US_FN = ctk.CTkLabel(self.upload_current_frame, text='File Name', font=(globalFont, 14))
        self.label_US_FN.grid(row=1, column=0, sticky='w', padx=20, pady=5)

        self.label_US_UDR = ctk.CTkLabel(self.upload_current_frame, text='Upload Data Rate', font=(globalFont, 14))
        self.label_US_UDR.grid(row=2, column=0, sticky='w', padx=20, pady=5)

        self.label_US_FUT = ctk.CTkLabel(self.upload_current_frame, text='File Upload Time', font=(globalFont, 14))
        self.label_US_FUT.grid(row=3, column=0, sticky='w', padx=20, pady=5)

        self.label_US_SRT = ctk.CTkLabel(self.upload_current_frame, text='System Response Time', font=(globalFont, 14))
        self.label_US_SRT.grid(row=4, column=0, sticky='w', padx=20, pady=5)

        ### Upload Statistics Values
        self.label_US_FN_val = ctk.CTkLabel(self.upload_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_US_FN_val.grid(row=1, column=1, sticky='e', padx=(0, 30), pady=5)

        self.label_US_UDR_val = ctk.CTkLabel(self.upload_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_US_UDR_val.grid(row=2, column=1, sticky='e', padx=(0, 30), pady=5)

        self.label_US_FUT_val = ctk.CTkLabel(self.upload_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_US_FUT_val.grid(row=3, column=1, sticky='e', padx=(0, 30), pady=5)

        self.label_US_SRT_val = ctk.CTkLabel(self.upload_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_US_SRT_val.grid(row=4, column=1, sticky='e', padx=(0, 30), pady=5)

        ## Upload History Box (Frame)
        self.upload_history_frame = ctk.CTkFrame(self.upload_frame, border_width=2, width=230, border_color='#59b1f0',
                                                 fg_color='transparent')
        self.upload_history_frame.grid(row=0, column=1, rowspan=3, sticky='nsew', padx=(20, 0))

        self.upload_history_frame.grid_columnconfigure(0, weight=1)
        self.upload_history_frame.grid_columnconfigure(1, weight=0)
        self.upload_history_frame.grid_columnconfigure(2, weight=0)
        self.upload_history_frame.grid_columnconfigure(3, weight=0)

        self.label_UH = ctk.CTkLabel(self.upload_history_frame, text='Upload History', font=(globalFont, 18))
        # self.label_UH.bind("<Button-1", #)
        self.label_UH.grid(row=0, column=0, sticky='w', padx=10, pady=(10, 0))

        ### Column Labels
        self.label_UH_FN = ctk.CTkLabel(self.upload_history_frame, text='File Name', font=(globalFont, 12))
        self.label_UH_FN.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(5, 0))

        self.label_UH_ST = ctk.CTkLabel(self.upload_history_frame, text='Start Time', font=(globalFont, 12))
        self.label_UH_ST.grid(row=1, column=1, sticky='w', padx=(12, 20), pady=(5, 0))

        self.label_UH_CT = ctk.CTkLabel(self.upload_history_frame, text='Complete Time', font=(globalFont, 12))
        self.label_UH_CT.grid(row=1, column=2, sticky='w', padx=(0, 20), pady=(5, 0))

        self.label_UH_status = ctk.CTkLabel(self.upload_history_frame, text='Status', font=(globalFont, 12))
        self.label_UH_status.grid(row=1, column=3, sticky='w', padx=(7, 10), pady=(5, 0))

        ### Textboxes for adding new upload history
        self.textbox_UH_FN = ctk.CTkTextbox(self.upload_history_frame, width=210)
        self.textbox_UH_FN.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(5, 0))
        self.textbox_UH_FN.configure(state="disabled")

        self.textbox_UH_ST = ctk.CTkTextbox(self.upload_history_frame, width=80)
        self.textbox_UH_ST.grid(row=2, column=1, padx=(0, 20), pady=(5, 0))
        self.textbox_UH_ST.configure(state="disabled")

        self.textbox_UH_CT = ctk.CTkTextbox(self.upload_history_frame, width=80)
        self.textbox_UH_CT.grid(row=2, column=2, sticky='w', padx=(0, 0), pady=(5, 0))
        self.textbox_UH_CT.configure(state="disabled")

        self.textbox_UH_status = ctk.CTkTextbox(self.upload_history_frame, width=50)
        self.textbox_UH_status.grid(row=2, column=3, sticky='e', padx=(0, 10), pady=(5, 0))
        self.textbox_UH_status.configure(state="disabled")

        """Download Widgets Frame"""
        self.download_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.download_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=30)

        self.download_frame.grid_columnconfigure(0, weight=0)
        self.download_frame.grid_columnconfigure(1, weight=1)

        self.server_dir_button = ctk.CTkButton(self.download_frame, corner_radius=5, text='Download File',
                                               font=(globalFont, 25, 'bold'), fg_color='#59b1f0', hover_color='#3977e3',
                                               text_color='#fafcff', border_spacing=10, width=270, height=60,
                                               command=self.open_server_dir_download)

        self.server_dir_button.grid(row=0, column=0, sticky='w', padx=20)

        ## Current File Download Statistics Frame
        self.download_current_frame = ctk.CTkFrame(self.download_frame, width=270, border_width=2,
                                                   border_color='#59b1f0',
                                                   fg_color='transparent')
        self.download_current_frame.grid_propagate(False)
        self.download_current_frame.grid(row=2, column=0, sticky='nsew', padx=20, pady=(20, 0))

        self.download_current_frame.grid_columnconfigure(0, weight=1)
        self.download_current_frame.grid_columnconfigure(1, weight=0)

        self.label_DS = ctk.CTkLabel(self.download_current_frame, text='Current Download Statistics',
                                  font=(globalFont, 17, 'bold'))
        self.label_DS.grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=(10,0))

        ### Download Statistics Labels
        self.label_DS_FN = ctk.CTkLabel(self.download_current_frame, text='File Name', font=(globalFont, 14))
        self.label_DS_FN.grid(row=1, column=0, sticky='w', padx=20, pady=5)

        self.label_DS_DDR = ctk.CTkLabel(self.download_current_frame, text='Download Data Rate', font=(globalFont, 14))
        self.label_DS_DDR.grid(row=2, column=0, sticky='w', padx=20, pady=5)

        self.label_DS_FDT = ctk.CTkLabel(self.download_current_frame, text='File Download Time', font=(globalFont, 14))
        self.label_DS_FDT.grid(row=3, column=0, sticky='w', padx=20, pady=5)

        self.label_DS_SRT = ctk.CTkLabel(self.download_current_frame, text='System Response Time', font=(globalFont, 14))
        self.label_DS_SRT.grid(row=4, column=0, sticky='w', padx=20, pady=5)

        ### Download Statistics Values
        self.label_DS_FN_val = ctk.CTkLabel(self.download_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_DS_FN_val.grid(row=1, column=1, sticky='e', padx=(0, 30), pady=5)

        self.label_DS_DDR_val = ctk.CTkLabel(self.download_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_DS_DDR_val.grid(row=2, column=1, sticky='e', padx=(0, 30), pady=5)

        self.label_DS_FDT_val = ctk.CTkLabel(self.download_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_DS_FDT_val.grid(row=3, column=1, sticky='e', padx=(0, 30), pady=5)

        self.label_DS_SRT_val = ctk.CTkLabel(self.download_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_DS_SRT_val.grid(row=4, column=1, sticky='e', padx=(0, 30), pady=5)

        ## Download History Box (Frame)
        self.download_history_frame = ctk.CTkFrame(self.download_frame, border_width=2, width=230,
                                                   border_color='#59b1f0',
                                                   fg_color='transparent')
        self.download_history_frame.grid(row=0, column=1, rowspan=3, sticky='nsew', padx=(0, 20))

        self.download_history_frame.grid_columnconfigure(0, weight=1)
        self.download_history_frame.grid_columnconfigure(1, weight=0)
        self.download_history_frame.grid_columnconfigure(2, weight=0)
        self.download_history_frame.grid_columnconfigure(3, weight=0)

        self.label_DH = ctk.CTkLabel(self.download_history_frame, text='Download History', font=(globalFont, 18))
        self.label_DH.grid(row=0, column=0, sticky='w', padx=10, pady=(10, 0))

        ### Column Labels
        self.label_DH_FN = ctk.CTkLabel(self.download_history_frame, text='File Name', font=(globalFont, 12))
        self.label_DH_FN.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(5, 0))

        self.label_DH_ST = ctk.CTkLabel(self.download_history_frame, text='Start Time', font=(globalFont, 12))
        self.label_DH_ST.grid(row=1, column=1, sticky='w', padx=(12, 20), pady=(5, 0))

        self.label_DH_CT = ctk.CTkLabel(self.download_history_frame, text='Complete Time', font=(globalFont, 12))
        self.label_DH_CT.grid(row=1, column=2, sticky='w', padx=(0, 20), pady=(5, 0))

        self.label_DH_status = ctk.CTkLabel(self.download_history_frame, text='Status', font=(globalFont, 12))
        self.label_DH_status.grid(row=1, column=3, sticky='w', padx=(7, 10), pady=(5, 0))

        ### Textboxes for adding new upload history
        self.textbox_DH_FN = ctk.CTkTextbox(self.download_history_frame, width=210)
        self.textbox_DH_FN.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(5, 0))
        self.textbox_DH_FN.configure("disabled")

        self.textbox_DH_ST = ctk.CTkTextbox(self.download_history_frame, width=80)
        self.textbox_DH_ST.grid(row=2, column=1, padx=(0, 20), pady=(5, 0))
        self.textbox_DH_ST.configure("disabled")

        self.textbox_DH_CT = ctk.CTkTextbox(self.download_history_frame, width=80)
        self.textbox_DH_CT.grid(row=2, column=2, sticky='w', padx=(0, 0), pady=(5, 0))
        self.textbox_DH_CT.configure("disabled")

        self.textbox_DH_status = ctk.CTkTextbox(self.download_history_frame, width=50)
        self.textbox_DH_status.grid(row=2, column=3, sticky='e', padx=(0, 10), pady=(5, 0))
        self.textbox_DH_status.configure("disabled")

        self.update_idletasks()

    # Sets the controller that view is connected to
    def set_controller(self, controller):
        self.controller = controller

    # Opens the user's file directory for file searching
    def open_file_dialog(self):
        filepaths = filedialog.askopenfilenames(
            title="Select a File to Upload to Server",
            filetypes=(
                ("Text Files", "*.txt"),
                ("MP3 Audio Files", "*.mp3"),
                ("MP4 Video Files", "*.mp4")
            )

        )

        if filepaths and self.controller:
            for filepath in filepaths:
                # Get the name of the file
                name = os.path.basename(filepath)

                # Send the file data to the controller
                self.controller.upload(name, filepath)

    # Opens the server's files and displays them
    def open_server_dir_download(self):
        self.controller.get_files()
        time.sleep(1)

        directory = DirView(self)

        label1 = ctk.CTkLabel(directory.content_frame, text="Select a File to Download", font=('Helvetica', 22))
        label1.grid(row=0, column=0, sticky='nsew')

        download_dir = ctk.CTkScrollableFrame(directory.content_frame, width=580, height=360)
        download_dir.grid(row=1, column=0, sticky='nsew')

        # Initialize a dictionary to track selected files
        selected_files = {}

        # Function to enable/disable the Select button
        def update_select_button():
            if any(var.get() for var in selected_files.values()):  # Check if any checkbox is selected
                select_button.configure(state="normal")
            else:
                select_button.configure(state="disabled")

        # Function to handle Select button click
        def select_file():
            # Get the selected file (only one file is allowed for download)
            for file, var in selected_files.items():
                if var.get():  # If checkbox is checked
                    selected_file = file
                    break
            else:
                selected_file = None  # No file selected

            if selected_file:
                self.controller.download(selected_file)
                directory.server_directory_window.destroy()

        select_button = ctk.CTkButton(directory.content_frame, text="Select", font=('Helvetica', 12),
                                      command=select_file)
        select_button.configure(state="disabled")  # Initially disabled
        select_button.grid(row=2, column=0, sticky='e', padx=(0, 10), pady=(0, 10))

        try:
            files = self.files
            for i, file in enumerate(files):
                # Create a Boolean variable for each checkbox
                var = ctk.BooleanVar()
                selected_files[file] = var

                # Create a checkbox for each file
                if '.' in file:
                    item_label = ctk.CTkCheckBox(download_dir, text=f"📄 {file}", variable=var,
                                                 command=update_select_button)
                else:
                    item_label = ctk.CTkCheckBox(download_dir, text=f"📁 {file}", variable=var,
                                                 command=update_select_button)

                item_label.grid(row=i, column=0, sticky='w')

        except Exception as e:
            error_label = ctk.CTkLabel(download_dir, text=f"Error: {e}")
            error_label.grid(row=0, column=0)

    def open_server_dir_edit(self):
        self.controller.get_files()
        time.sleep(1)

        directory = DirView(self)

        label1 = ctk.CTkLabel(directory.content_frame, text="Edit and View Server Directory", font=('Helvetica', 22))
        label1.grid(row=0, column=0, sticky='nsew')

        download_dir = ctk.CTkScrollableFrame(directory.content_frame, width=580, height=360)
        download_dir.grid(row=1, column=0, sticky='nsew')

        # Initialize a dictionary to track selected files
        selected_files = {}

        # Function to enable/disable the Select button
        def update_select_button():
            if any(var.get() for var in selected_files.values()):  # Check if any checkbox is selected
                delete_button.configure(state="normal")
            else:
                delete_button.configure(state="disabled")

        def create_file_folder():
            def confirm_file():
                self.controller.makedir(path.get())
                confirm_window.confirm_window.destroy()

            # Get the selected file (only one file is allowed for download)
            for file, var in selected_files.items():
                if var.get():  # If checkbox is checked
                    selected_file = file
                    break
            else:
                selected_file = None  # No file selected

            confirm_window = ConfirmView(directory)
            confirm_window.confirm_window.attributes("-topmost", True)
            confirm_window.window_label.configure(text="Confirm File Path where Folder will be created:")
            confirm_window.confirm_button.configure(command=confirm_file)

            path = ctk.StringVar()
            file_path_check = ctk.CTkEntry(confirm_window.content_frame, textvariable=path, width=500)
            file_path_check.grid(row=1, column=0, sticky="nsew")

            if selected_file:
                filepath = FILE_STORAGE_DIR + "/" + selected_file
                path.set(filepath)
            else:
                path.set(FILE_STORAGE_DIR)

        # Function to handle Select button click
        def delete_file():
            def confirm_file():
                self.controller.delete(selected_file)
                delete_window.confirm_window.destroy()

            # Get the selected file (only one file is allowed for download)
            for file, var in selected_files.items():
                if var.get():  # If checkbox is checked
                    selected_file = file
                    break
            else:
                selected_file = None  # No file selected

            delete_window = ConfirmView(directory)
            delete_window.confirm_window.attributes("-topmost", True)
            delete_window.window_label.configure(text=f"Confirm Deletion of {selected_file}")
            delete_window.confirm_button.configure(text="Delete", command=confirm_file)


        create_button = ctk.CTkButton(directory.content_frame, text="Create a Folder", font=('Helvetica', 12),
                                      command=create_file_folder)
        create_button.grid(row=2, column=0, sticky='w', padx=(0, 10), pady=(0, 10))

        delete_button = ctk.CTkButton(directory.content_frame, text="Delete Selected File", font=('Helvetica', 12),
                                      command=delete_file)
        delete_button.configure(state="disabled")  # Initially disabled
        delete_button.grid(row=2, column=0, sticky='e', padx=(0,0), pady=(0, 10))

        try:
            files = self.files
            for i, file in enumerate(files):
                # Create a Boolean variable for each checkbox
                var = ctk.BooleanVar()
                selected_files[file] = var

                # Create a checkbox for each file
                if '.' in file:
                    item_label = ctk.CTkCheckBox(download_dir, text=f"📄 {file}", variable=var,
                                                 command=update_select_button)
                else:
                    item_label = ctk.CTkCheckBox(download_dir, text=f"📁 {file}", variable=var,
                                                 command=update_select_button)

                item_label.grid(row=i, column=0, sticky='w')

        except Exception as e:
            error_label = ctk.CTkLabel(download_dir, text=f"Error: {e}")
            error_label.grid(row=0, column=0)

    def return_files(self, files):
        json_files = json.loads(files)
        self.files = json_files

    # Displays the File Upload Statistics
    def display_upload_stats(self, up_data):
        json_up_data = json.loads(up_data)
        # will most likely pass in some parameter that contains the stat data
        filename = json_up_data["filename"]
        upload_rate = json_up_data["uploadRate"]
        upload_time = json_up_data["time"]
        sys_res_time = ""

        self.label_US_FN_val.configure(text=filename)
        self.label_US_UDR_val.configure(text=upload_rate)
        self.label_US_FUT_val.configure(text=upload_time)
        self.label_US_SRT_val.configure(text=sys_res_time)
        print("displayed upload stats")

    # Displays the File Download Statistics
    def display_download_stats(self, down_data):
        json_down_data = json.loads(down_data)

        filename = json_down_data["filename"]
        download_rate = json_down_data["downloadRate"]
        download_time = json_down_data["time"]
        sys_res_time = ""

        self.label_DS_FN_val.configure(text=filename)
        self.label_DS_DDR_val.configure(text=download_rate)
        self.label_DS_FDT_val.configure(text=download_time)
        self.label_DS_SRT_val.configure(text=sys_res_time)

    def update_upload_history(self, file_data):
        json_file_data = json.loads(file_data)

        filename = json_file_data["filename"]
        start_time = json_file_data["stime"]
        complete_time = json_file_data["ctime"]
        status = json_file_data["status"]

        self.textbox_UH_FN.configure(state="normal")
        self.textbox_UH_ST.configure(state="normal")
        self.textbox_UH_CT.configure(state="normal")
        self.textbox_UH_status.configure(state="normal")

        self.textbox_UH_FN.insert("end", filename)
        self.textbox_UH_ST.insert("end", start_time)
        self.textbox_UH_CT.insert("end", complete_time)
        self.textbox_UH_status.insert("end", status)

        self.textbox_UH_FN.configure(state="disabled")
        self.textbox_UH_ST.configure(state="disabled")
        self.textbox_UH_CT.configure(state="disabled")
        self.textbox_UH_status.configure(state="disabled")


    def update_download_history(self, file_data):
        print("view received, attempting to print")
        json_file_data = json.loads(file_data)

        print(file_data)

        filename = json_file_data["filename"]
        start_time = json_file_data["stime"]
        complete_time = json_file_data["ctime"]
        status = json_file_data["status"]

        self.textbox_DH_FN.configure(state="normal")
        self.textbox_DH_ST.configure(state="normal")
        self.textbox_DH_CT.configure(state="normal")
        self.textbox_DH_status.configure(state="normal")

        self.textbox_DH_FN.insert("end", filename)
        self.textbox_DH_ST.insert("end", start_time)
        self.textbox_DH_CT.insert("end", complete_time)
        self.textbox_DH_status.insert("end", status)

        self.textbox_DH_FN.configure(state="disabled")
        self.textbox_DH_ST.configure(state="disabled")
        self.textbox_DH_CT.configure(state="disabled")
        self.textbox_DH_status.configure(state="disabled")

class InitView(tk.Frame):
    task_complete = False

    def __init__(self, parent):
        super().__init__(parent)

        self.controller = None
        self.sys_res_time = None

        # Draw the top level window
        self.server_connect_window = ctk.CTkToplevel(parent)
        self.server_connect_window.geometry("400x120")
        self.server_connect_window.resizable(False,False)
        self.server_connect_window.title("Server Connection")
        self.server_connect_window.transient()
        self.server_connect_window.grab_set()

        self.server_connect_window.columnconfigure(0, weight=1)

        self.connection_label = ctk.CTkLabel(self.server_connect_window, text="Connecting to Server...", font=('Helvetica', 18))
        self.connection_label.grid(row=0, column=0, sticky='n', pady=(20,0))

        self.connection_label2 = ctk.CTkLabel(self.server_connect_window, text="",
                                             font=('Helvetica', 18))
        self.connection_label2.grid(row=1, column=0, sticky='n', pady=(20, 0))

        self.connection_label3 = ctk.CTkLabel(self.server_connect_window, text="",
                                              font=('Helvetica', 18))
        self.connection_label3.grid(row=2, column=0, sticky='n', pady=(20, 0))

        # Bind the close button action to on_close() function
        self.server_connect_window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_idletasks()

    def set_controller(self, controller):
        self.controller = controller

    # Function to override the close button action
    def on_close(self):
        if self.task_complete:
            self.server_connect_window.destroy()  # Allow closing if the task is complete
        else:
            self.connection_label3.configure(text="Cannot Proceed Yet, Attempting to Connect")
            print("Task not complete. Cannot close yet.")  # Notify user

    def connect_to_server(self):
        # Run the connection logic in a separate thread
        threading.Thread(target=self._connect_to_server_thread, daemon=True).start()

    def _connect_to_server_thread(self):
        # Perform the connection logic in the thread
        if self.controller.connect():
            # Update the label on the main thread
            time.sleep(2)
            self.connection_label.after(0, lambda: self.connection_label.configure(text="Successfully Connected to Server!", text_color="green"))
            self.connection_label2.configure(text=f"System Response Time: {self.controller.sys_res_time}s")
            self.connection_label3.configure(text="Close Window to Proceed")
            self.task_complete = True
        else:
            time.sleep(2)
            self.connection_label.after(0, lambda: self.connection_label.configure(text="Connection Failed. Check Host IP and Port Number"))
            self.task_complete = False

    def set_sys_res_time(self, res_time):
        self.sys_res_time = res_time

# Class that draws a top level window for displaying the server directory
class DirView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.server_directory_window = ctk.CTkToplevel(parent)
        self.server_directory_window.geometry("600x460")
        self.server_directory_window.attributes("-topmost", True)
        self.server_directory_window.resizable(False, False)
        self.server_directory_window.title("Browse Server Directory")

        # Add a container frame for the content
        self.content_frame = ctk.CTkFrame(self.server_directory_window)
        self.content_frame.grid(row=0, column=0, sticky='nsew')

        # Configure grid to allow expansion
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

# Class that draws a top level window for displaying confirmation windows.
class ConfirmView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.confirm_window = ctk.CTkToplevel(parent)
        self.confirm_window.geometry("500x200")
        self.confirm_window.resizable(False, False)
        self.confirm_window.title("Confirm Action")

        # Configure confirm_window to expand content_frame
        self.confirm_window.grid_rowconfigure(0, weight=1)
        self.confirm_window.grid_columnconfigure(0, weight=1)

        # Add a container frame for the content
        self.content_frame = ctk.CTkFrame(self.confirm_window)
        self.content_frame.grid(sticky='nsew')

        self.content_frame.grid_columnconfigure(0, weight=1)

        self.window_label = ctk.CTkLabel(self.content_frame, text="", font=('Helvetica', 14))
        self.window_label.grid(row=0, column=0, sticky="nsew")

        self.cancel_button = ctk.CTkButton(self.content_frame, text="Cancel", font=('Helvetica', 12))
        self.cancel_button.grid(row=2, column=0, sticky="w")

        self.confirm_button = ctk.CTkButton(self.content_frame, text="Confirm", font=('Helvetica', 12))
        self.confirm_button.grid(row=2, column=0, sticky="e")

class LoginView(tk.Frame):
    task_complete = False

    def __init__(self, parent):
        super().__init__(parent)

        self.login_window = ctk.CTkToplevel(parent)
        self.login_window.geometry("400x300")
        self.login_window.attributes("-topmost", True)
        self.login_window.resizable(False, False)
        self.login_window.title("Login Screen")
        self.login_window.transient()

        self.login_window.grid_columnconfigure(0, weight=1)

        # Frame
        self.frame = ctk.CTkFrame(self.login_window, fg_color="transparent")
        self.frame.grid(column=0, sticky="nsew")

        # Title Label
        self.title_label = ctk.CTkLabel(self.frame, text="Login", font=("Helvetica", 20))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Username Label and Entry
        self.username_label = ctk.CTkLabel(self.frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter your username")
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Password Label and Entry
        self.password_label = ctk.CTkLabel(self.frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')

        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter your password", show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Signup Button
        self.signup_button = ctk.CTkButton(self.frame, text="Signup", command=self.open_signup_window)
        self.signup_button.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Login Button
        self.login_button = ctk.CTkButton(self.frame, text="Login", command=self.handle_login)
        self.login_button.grid(row=3, column=1, padx=10, pady=10, sticky='e')

        # Bind the close button action to our custom function
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_close)

    # Function to override the close button action
    def on_close(self):
        if self.task_complete:
            self.login_window.destroy()  # Allow closing if the task is complete
        else:
            print("Task not complete. Cannot close yet.")  # Notify user


    def handle_login(self):
        """Handles login logic."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            success = self.validate_credentials(username, password)
            if success:
                print("Login successful!")
                self.login_window.destroy()
                self.task_complete = True
                messagebox.showinfo("Login Status", "Login successful!")
                return True
            else:
                raise ValueError("Invalid username or password.")
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Login Status", str(e))

    def open_signup_window(self):
        """Opens the signup window."""
        self.login_window.destroy()  # Properly close the current window
        signupView = SignupView(self)

    def validate_credentials(self, username, password):
        """
        Validates the username and password against a .txt file hosted remotely.
        Each line in the file should have the format: username,hashed_password
        """
        # File path to the remote file
        filepath = "/home/jillienne_lapid/passwords.txt"

        try:
            with open(FS_DIR, "r") as file:
                credentials_data = file.readlines()

            for line in credentials_data:
                stored_username, stored_hashed_password = line.strip().split(",")
                if username == stored_username:
                    # Check if the entered password matches the stored hashed password
                    if bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
                        return True
        except FileNotFoundError:
            print(f"Credentials file not found at {filepath}")
            messagebox.showerror("Error", "Credentials file not found.")
        except ValueError:
            print("Credentials file is not formatted correctly.")
            messagebox.showerror("Error", "The credentials file is not formatted correctly.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

        return False

class SignupView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.signup_window = ctk.CTkToplevel(parent)
        self.signup_window.geometry("400x300")
        self.signup_window.attributes("-topmost", True)
        self.signup_window.resizable(False, False)
        self.signup_window.title("Save Credentials")

        self.signup_window.grid_columnconfigure(0, weight=1)

        # Handle close button
        self.signup_window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Frame
        self.frame = ctk.CTkFrame(self.signup_window, fg_color="transparent")
        self.frame.grid(column=0, sticky="nsew")

        # Title Label
        self.title_label = ctk.CTkLabel(self.frame, text="Register Credentials", font=("Helvetica", 20))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Username Label and Entry
        self.username_label = ctk.CTkLabel(self.frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter your username")
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Password Label and Entry
        self.password_label = ctk.CTkLabel(self.frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')

        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter your password", show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Save Button
        self.save_button = ctk.CTkButton(self.frame, text="Save", command=self.save_credentials)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=10)

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
            filepath = "/home/jillienne_lapid/passwords.txt"

            if not os.path.exists(FS_DIR):
                open(FS_DIR, "w").close()

            # Save the hashed password
            with open(FS_DIR, "a") as file:
                file.write(credentials)

            print("Credentials saved securely!")
            tk.messagebox.showinfo("Success", "Credentials saved securely!")
            self.signup_window.destroy()
            loginView = LoginView(self)

        else:
            print("Both fields must be filled.")
            tk.messagebox.showerror("Error", "Both fields must be filled.")

    def on_close(self):
        """
        Handles the close button (X) event.
        """
        self.signup_window.destroy()  # Close the current window