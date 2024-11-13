import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, font, filedialog

class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

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
                                               text_color='#fafcff', border_spacing=10, height=50)

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
        self.label_US.grid(row=0, column=0, sticky='w', padx=10, pady=(10,0))

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
        self.label_US_FN_val.grid(row=1, column=1, sticky='e', padx=(0,20), pady=5)

        self.label_US_UDR_val = ctk.CTkLabel(self.upload_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_US_UDR_val.grid(row=2, column=1, sticky='e', padx=(0,20), pady=5)

        self.label_US_FUT_val = ctk.CTkLabel(self.upload_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_US_FUT_val.grid(row=3, column=1, sticky='e', padx=(0,20), pady=5)

        self.label_US_SRT_val = ctk.CTkLabel(self.upload_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_US_SRT_val.grid(row=4, column=1, sticky='e', padx=(0,20), pady=5)

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

        self.label_UH_FN = ctk.CTkLabel(self.upload_history_frame, text='File Name', font=(globalFont, 12))
        self.label_UH_FN.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(5, 0))

        self.label_UH_ST = ctk.CTkLabel(self.upload_history_frame, text='Start Time', font=(globalFont, 12))
        self.label_UH_ST.grid(row=1, column=1, sticky='w', padx=(0, 20), pady=(5, 0))

        self.label_UH_CT = ctk.CTkLabel(self.upload_history_frame, text='Complete Time', font=(globalFont, 12))
        self.label_UH_CT.grid(row=1, column=2, sticky='w', padx=(0, 20), pady=(5, 0))

        self.label_UH_status = ctk.CTkLabel(self.upload_history_frame, text='Status', font=(globalFont, 12))
        self.label_UH_status.grid(row=1, column=3, sticky='w', padx=(0, 20), pady=(5, 0))

        """Download Widgets Frame"""
        self.download_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.download_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=30)

        self.download_frame.grid_columnconfigure(0, weight=0)
        self.download_frame.grid_columnconfigure(1, weight=1)

        self.server_dir_button = ctk.CTkButton(self.download_frame, corner_radius=5, text='Download File',
                                               font=(globalFont, 25, 'bold'), fg_color='#59b1f0', hover_color='#3977e3',
                                               text_color='#fafcff', border_spacing=10, width=270, height=60)

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
        self.label_DS.grid(row=0, column=0, sticky='w', padx=10, pady=(10,0))

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
        self.label_DS_FN_val.grid(row=1, column=1, sticky='e', padx=(0, 20), pady=5)

        self.label_DS_DDR_val = ctk.CTkLabel(self.download_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_DS_DDR_val.grid(row=2, column=1, sticky='e', padx=(0, 20), pady=5)

        self.label_DS_FDT_val = ctk.CTkLabel(self.download_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_DS_FDT_val.grid(row=3, column=1, sticky='e', padx=(0, 20), pady=5)

        self.label_DS_SRT_val = ctk.CTkLabel(self.download_current_frame, text='-', font=(globalFont, 14, 'bold'))
        self.label_DS_SRT_val.grid(row=4, column=1, sticky='e', padx=(0, 20), pady=5)

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

        self.label_DH_FN = ctk.CTkLabel(self.download_history_frame, text='File Name', font=(globalFont, 12))
        self.label_DH_FN.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(5, 0))

        self.label_DH_ST = ctk.CTkLabel(self.download_history_frame, text='Start Time', font=(globalFont, 12))
        self.label_DH_ST.grid(row=1, column=1, sticky='w', padx=(0, 20), pady=(5, 0))

        self.label_DH_CT = ctk.CTkLabel(self.download_history_frame, text='Complete Time', font=(globalFont, 12))
        self.label_DH_CT.grid(row=1, column=2, sticky='w', padx=(0, 20), pady=(5, 0))

        self.label_DH_status = ctk.CTkLabel(self.download_history_frame, text='Status', font=(globalFont, 12))
        self.label_DH_status.grid(row=1, column=3, sticky='w', padx=(0, 20), pady=(5, 0))

        # Initialize the controller to None
        self.controller = None

        self.create_server_connect_dialog()

    def set_controller(self, controller):
        self.controller = controller

    def open_file_dialog(self):
        filenames = filedialog.askopenfilenames(
            title="Select a File to Upload to Server",
            filetypes=(
                ("Text Files", "*.txt"),
                ("MP3 Audio Files", "*.mp3"),
                ("MP4 Video Files", "*.mp4")
            )

        )

        if filenames:
            print("Selected files:")
            for filename in filenames:
                print(filename)

    def expand_upload_history(self):
        print("upload history")

    def create_server_connect_dialog(self):
        self.server_connect_window = ctk.CTkToplevel(self)
        self.server_connect_window.geometry("400x300")
        self.server_connect_window.title("Server Connection")