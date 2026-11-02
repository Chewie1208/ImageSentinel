import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
import scanner_engine
from datetime import datetime
import threading
import os
import json
import sys
from pathlib import Path

from pathlib import Path
import json

def resource_path(relative_path):

    try:
        base_path = Path(sys._MEIPASS)

    except Exception:
        base_path = Path(__file__).parent

    return base_path / relative_path



class ImageSentinelApp:

    def __init__(self):

        settings_file = "settings.json"

        self.app = ctk.CTk()
        self.app.title("Image Sentinel v0.1 (Alpha)")
        self.app.geometry("600x920")
        self.app.resizable(
            False,
            False
        )

# Create main frame, colum configuration and row configuration
        self.main_frame = ctk.CTkFrame(
            self.app,
            fg_color="transparent"
        )
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )
        self.main_frame.grid_columnconfigure(
            0,
            weight=1
        )
        self.main_frame.grid_rowconfigure(
            0,
            weight=0
        )
        self.main_frame.grid_rowconfigure(
            1,
            weight=0
        )
        self.main_frame.grid_rowconfigure(
            2,
            weight=0
        )
        self.main_frame.grid_rowconfigure(
            3,
            weight=0
        )

# Create folders frame and configure columns
        self.folders_frame = ctk.CTkFrame(
            self.main_frame
        )
        self.folders_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0,3)
        )
        self.folders_frame.grid_columnconfigure(
            0,
            weight=1
        )
        self.folders_frame.grid_columnconfigure(
            1,
            weight=1
        )
        self.source_frame = ctk.CTkFrame(
            self.folders_frame
        )
        self.source_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10,5),
            pady=10
        )
        self.results_frame = ctk.CTkFrame(
            self.folders_frame
        )
        self.results_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5,10),
            pady=10
        )

        # Source folder label
        self.source_label = ctk.CTkLabel(
            self.source_frame,
            text="Source Folder"
        )
        self.source_label.pack()
        self.source_row = ctk.CTkFrame(
            self.source_frame
        )
        # Browse button
        self.source_browse_button = ctk.CTkButton(
            self.source_row,
            text="Browse",
            width=10,
            command=self.select_source_folder
        )
        self.source_browse_button.pack(
            side="right"
        )
        self.source_entry = ctk.CTkEntry(
            self.source_row,
            width=500
        )
        self.source_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0,10)
        )
        self.source_row.pack(
            fill="x",
            padx=10,
            pady=5
        )


        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="Results Folder"
        )
        self.results_label.pack()
        self.results_row = ctk.CTkFrame(
            self.results_frame
        )
        # Browse button
        self.results_browse_button = ctk.CTkButton(
            self.results_row,
            text="Browse",
            width=10,
            command=self.select_results_folder
        )
        self.results_browse_button.pack(
            side="right"
        )
        self.results_entry = ctk.CTkEntry(
            self.results_row,
            width=500
        )
        self.results_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )
        self.results_row.pack(
            fill="x",
            padx=10,
            pady=5
        )



# Action Frame for filters and actions
        self.filters_actions_frame = ctk.CTkFrame(
            self.main_frame
        )
        self.filters_actions_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0,3)
        )
        self.filters_actions_frame.grid_columnconfigure(
            0,
            weight=2
        )
        self.filters_actions_frame.grid_columnconfigure(
            1,
            weight=1
        )
        self.filters_frame = ctk.CTkFrame(
            self.filters_actions_frame
        )
        self.filters_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10,5),
            pady=10
        )
        self.actions_frame = ctk.CTkFrame(
            self.filters_actions_frame
        )
        self.actions_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5,10),
            pady=10
        )

        # Threshold row
        self.threshold_row = ctk.CTkFrame(
            self.filters_frame,
            fg_color="transparent"
        )
        self.threshold_row.pack(
            anchor="w",
            padx=20,
            pady=(15, 0)
        )

        self.threshold_label = ctk.CTkLabel(
            self.threshold_row,
            text="Matching Threshold:"
        )
        self.threshold_label.pack(
            side="left"
        )

        self.threshold_entry = ctk.CTkEntry(
            self.threshold_row,
            width=80
        )
        self.threshold_entry.pack(
            side="left",
            padx=(10,0)
        )

        self.copy_options_label = ctk.CTkLabel(
            self.filters_frame,
            text="Select NSFW categories to review"
        )
        self.copy_options_label.pack(
            anchor="w",
            padx=20,
            pady=(20,5)
        )
 
        self.copy_very_high_var = ctk.BooleanVar(
            value=True
        )
        self.copy_high_var = ctk.BooleanVar(
            value=True
        )
        self.copy_medium_var = ctk.BooleanVar(
            value=True
        )
        self.copy_low_var = ctk.BooleanVar(
            value=True
        )

        self.copy_very_high_checkbox = ctk.CTkCheckBox(
            self.filters_frame,
            text="Explicit Images",
            variable=self.copy_very_high_var
        )
        self.copy_very_high_checkbox.pack(
            anchor="w",
            padx=20
        )
        self.copy_high_checkbox = ctk.CTkCheckBox(
        self.filters_frame,
            text="Inappropriate Images",
            variable=self.copy_high_var
        )
        self.copy_high_checkbox.pack(
            anchor="w",
            padx=20
        )
        self.copy_medium_checkbox = ctk.CTkCheckBox(
            self.filters_frame,
            text="Borderline Images",
            variable=self.copy_medium_var
        )
        self.copy_medium_checkbox.pack(
            anchor="w",
            padx=20
        )
        self.copy_low_checkbox = ctk.CTkCheckBox(
            self.filters_frame,
            text="Mild matches",
            variable=self.copy_low_var
        )
        self.copy_low_checkbox.pack(
            anchor="w",
            padx=20
        )

# Actions frame
        self.actions_label = ctk.CTkLabel(
            self.actions_frame,
            text="Actions"
        )
        self.actions_start_scan_button = ctk.CTkButton(
            self.actions_frame,
            text="Start Scan",
            fg_color="#2E8B57",
            hover_color="#256F47",
            width=15,
            command=self.start_scan
        )
        self.actions_start_scan_button.pack(
#            fill="x",
            padx=20,
            pady=(0,10)
        )
        self.actions_stop_scan_button = ctk.CTkButton(
            self.actions_frame,
            text="Stop Scan",
            fg_color="#D13438",
            hover_color="#A7282B",  
            command=self.stop_scan
        )
        self.actions_stop_scan_button.pack(
            fill="x",
            padx=20,
            pady=(0,10)
        )
        self.open_results_button = ctk.CTkButton(
            self.actions_frame,
            text="Open Results",
            fg_color="#2D7FF9",
            hover_color="#2567CA",
            command=self.open_results_folder 
        )
        self.open_results_button.pack(
            fill="x",
            padx=20,
            pady=(0,10)
        )
        
# Status frame
        self.summary_frame = ctk.CTkFrame(
            self.main_frame
        )
        self.summary_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0,3)
        )
        self.summary_frame.grid_columnconfigure(
            0,
            weight=1
        )
        self.summary_frame.grid_columnconfigure(
            1,
            weight=1
        )
        self.summary_left = ctk.CTkFrame(
            self.summary_frame
        )
        self.summary_left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10,5),
            pady=10
        )
        self.summary_right = ctk.CTkFrame(
            self.summary_frame
        )
        self.summary_right.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5,10),
            pady=10
        )
 
        self.summary_left_label = ctk.CTkLabel(
            self.summary_left,
            text="Scan Progress"
        )

        self.summary_left_label.pack(
            pady=(1,1)
        )
        # Status label
        self.status_label = ctk.CTkLabel(
            self.summary_left,
            text="Status: Ready"
        )       
        self.status_label.pack(
            padx=1,
            pady=1,
            anchor="w"
        )
         # Status output
        self.total_images_label = ctk.CTkLabel(
            self.summary_left,
            text="Total Images: 0"
        )
        self.total_images_label.pack(
            padx=1,
            pady=1,
            anchor="w"
        )
        self.number_scanned_label = ctk.CTkLabel(
            self.summary_left,
            text="Files Scanned: 0"
        )
        self.number_scanned_label.pack(
            padx=1,
            pady=1,
            anchor="w"
        )

         # Status output
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.summary_left,
            width=200,
            height=30,
            fg_color="#B4D5C0",
            progress_color="#076B30"
        )
        self.progress_bar.pack(
            padx=1,
            pady=20
        )
        self.progress_bar.set(0)
        self.progress_label = ctk.CTkLabel(
            self.summary_left,
            text="Progress: 0%"
        )
        self.progress_label.pack(
            padx=1,
            pady=1
        )


        self.summary_right_label = ctk.CTkLabel(
            self.summary_right,
            text="Scan Statistics"
        )

        self.summary_right_label.pack(
            pady=(1,1)
        )
        self.started_label = ctk.CTkLabel(
            self.summary_right,
            text="Started Time:"
        )
        self.started_label.pack(
            padx=1,
            pady=1,
            anchor="w"
        )
        self.finished_label = ctk.CTkLabel(
            self.summary_right,
            text="Finished Time:"
        )
        self.finished_label.pack(
            padx=1,
            pady=1,
            anchor="w"
        )
        self.duration_label = ctk.CTkLabel(
            self.summary_right,
            text="Duration:"
        )
        self.duration_label.pack(
            padx=1,
            pady=1,
            anchor="w"
        )
        self.number_flagged_label = ctk.CTkLabel(
            self.summary_right,
            text="Files Flagged:"
        )
        self.number_flagged_label.pack(
            padx=1,
            pady=1,
            anchor="w"
        )

# Activity frame
        self.activity_frame = ctk.CTkFrame(
            self.main_frame
        )

        self.activity_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0,3)
        )

        self.activity_frame.grid_columnconfigure(
            0,
            weight=3
        )
        self.activity_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.activity_left = ctk.CTkFrame(
            self.activity_frame
        )
        self.activity_left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10,5),
            pady=10
        )

        # Activity label
        self.activity_label = ctk.CTkLabel(
            self.activity_left,
            text="Activity Log"
        )
        self.activity_label.pack(
            padx=20,
            pady=5
        )

        # Activity textbox
        self.activity_log = ctk.CTkTextbox(
            self.activity_left,
            height=260
        )
        self.activity_log.configure(
            state="disabled"
        )
        self.activity_log.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(10,20)
        )

        self.info_frame = ctk.CTkFrame(
            self.activity_frame
        )

        self.info_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5,10),
            pady=10
        )
        self.info_title = ctk.CTkLabel(
            self.info_frame,
            text="Image Sentinel",
            font=("Segoe UI", 18, "bold")
        )

        self.info_title.pack(
            pady=(5,5)
        )
        self.version_label = ctk.CTkLabel(
            self.info_frame,
            text="Version 0.1 Alpha"
        )

        self.version_label.pack(
            pady=5
        )

        logo_image = Image.open(
            resource_path(
                "assets/logo.png"
            )
        )

        self.logo = ctk.CTkImage(
            light_image=logo_image,
            dark_image=logo_image,
            size=(120, 120)
        )
        self.logo_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            image=self.logo
        )

        self.logo_label.pack(
            pady=(10, 10)
        )

        self.description_label = ctk.CTkLabel(
            self.info_frame,
            text=(
                "Safe image discovery,\n"
                "classification and review."
            ),
            justify="center"
        )

        self.description_label.pack(
            padx=20,
            pady=(0, 5)
        )

        self.divider = ctk.CTkLabel(
            self.info_frame,
            text="────────────"
        )

        self.divider.pack(
            pady=(0, 5)
        )

        self.powered_by_label = ctk.CTkLabel(
            self.info_frame,
            text="Powered by NudeNet"
        )

        self.powered_by_label.pack(
            pady=(0, 20)
        )


        self.stop_requested = False

        # Load saved values
        self.load_settings()

        # Initial messages
        self.log_message(
            "Image Sentinel started"
        )

        self.log_message(
            "Waiting for scan"
        )


    def update_total_images(
        self,
        count
    ):

        self.total_images_label.configure(
            text=f"Total Images: {count:,}"
        )

    def update_progress(
        self,
        scanned,
        total
    ):

        if total == 0:
            return

        percentage = (
            scanned / total
        )

        self.progress_bar.set(
            percentage
        )

        self.progress_label.configure(
            text=f"Progress: {percentage * 100:.1f}%"
        )

    def save_settings(self):

        settings = {
            "source_folder":
                self.source_entry.get(),

            "results_folder":
                self.results_entry.get(),

            "threshold":
                self.threshold_entry.get(),

            "copy_very_high":
                self.copy_very_high_var.get(),

            "copy_high":
                self.copy_high_var.get(),

            "copy_medium":
                self.copy_medium_var.get(),

            "copy_low":
                self.copy_low_var.get()
        }

        with open(
            "settings.json",
            "w"
        ) as f:

            json.dump(
                settings,
                f,
                indent=4
            )

    def load_settings(self):

        settings_file = "settings.json"

        default_source = (
            Path.home() / "Pictures"
        )

        default_results = Path(
            "C:/Temp/ImageSentinelResults"
        )

        default_results.mkdir(
            parents=True,
            exist_ok=True
        )

        settings = {

            "source_folder": str(
                default_source
            ),

            "results_folder": str(
                default_results
            ),

            "threshold": "0.70"

        }

        try:

            if Path(settings_file).exists():

                with open(
                    settings_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    settings.update(
                        json.load(f)
                    )

        except Exception:

            pass

        self.source_entry.delete(
            0,
            "end"
        )

        self.source_entry.insert(
            0,
            settings["source_folder"]
        )

        self.results_entry.delete(
            0,
            "end"
        )

        self.results_entry.insert(
            0,
            settings["results_folder"]
        )

        self.threshold_entry.delete(
            0,
            "end"
        )

        self.threshold_entry.insert(
            0,
            str(
                settings.get(
                    "threshold",
                    "0.70"
                )
            )
        )
            
    def open_results_folder(self):

        folder = self.results_entry.get()

        if not folder:

            self.log_message(
                "No results folder selected"
            )

            return

        if not os.path.exists(folder):

            self.log_message(
                "Results folder does not exist"
            )

            return

        os.startfile(folder)
        
    def run(self):
        self.app.mainloop()
  
        self.app.mainloop()

    def select_results_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.results_entry.delete(0, "end")

            self.results_entry.insert(
                0,
                folder
            )
            self.save_settings()

    def select_source_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.source_entry.delete(0, "end")

            self.source_entry.insert(
                0,
                folder
            )
            self.save_settings()

    def start_scan(self):
        self.stop_requested = False
        self.reset_scan_ui()
        self.save_settings()
        self.log_message(
            "Start Scan clicked"
        )

        source_folder = self.source_entry.get()

        results_folder = self.results_entry.get()

        threshold = float(
            self.threshold_entry.get()
        )
        self.status_label.configure(
            text="Status: Running"
        )
        self.scan_start_time = datetime.now()
        self.started_label.configure(
            text=f"Started: {self.scan_start_time:%H:%M:%S}"
        )
        copy_very_high = self.copy_very_high_var.get()
        copy_high = self.copy_high_var.get()
        copy_medium = self.copy_medium_var.get()
        copy_low = self.copy_low_var.get()

        scan_thread = threading.Thread(
            target=scanner_engine.run_scan,
            args=(
                source_folder,
                results_folder,
                threshold,
                copy_very_high,
                copy_high,
                copy_medium,
                copy_low,
                self.log_message,
                self.update_scan_count,
                self.update_flagged_count,
                self.update_total_images,
                self.update_progress,
                lambda: self.stop_requested
            )
        )

        scan_thread.start()

    def update_scan_count(self, count):
        self.number_scanned_label.configure(
            text=f"Files Scanned: {count:,}"
        )
    
    def update_flagged_count(self, count):
        self.number_flagged_label.configure(
            text=f"Files Flagged: {count:,}"
        )

    def log_message(self, message):

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        if message == "__SCAN_COMPLETE__":

            finish_time = datetime.now()

            self.finished_label.configure(
                text=f"NSFW Scanning Finished: {finish_time:%H:%M:%S}"
            )

            self.status_label.configure(
                text="Status: Finished"
            )
            duration = finish_time - self.scan_start_time

            duration_text = str(duration).split(".")[0]

            self.duration_label.configure(
                text=f"Duration: {duration_text}"
            )
            self.activity_log.configure(
                state="normal"
            )
            self.activity_log.insert(
                "end",
                f"{timestamp} - NSFW scanning finished\n"
            )
            self.activity_log.configure(
                state="disabled"
            )
            return

        if message == "__SCAN_STOPPED__":

            finish_time = datetime.now()

            self.finished_label.configure(
                text=f"NSFW Scanning stopped: {finish_time:%H:%M:%S}"
            )
            self.status_label.configure(
                text="Status: Stopped"
            )
            duration = finish_time - self.scan_start_time

            duration_text = str(duration).split(".")[0]

            self.duration_label.configure(
                text=f"Duration: {duration_text}"
            )
            self.activity_log.configure(
                state="normal"
            )
            self.activity_log.insert(
                "end",
                f"{timestamp} - NSFW Scanning stopped\n"
            )
            self.activity_log.configure(
                state="disabled"
            )

            return

        self.activity_log.configure(
            state="normal"
        )
        self.activity_log.insert(
            "end",
            f"{timestamp} - {message}\n"
        )
        self.activity_log.configure(
            state="disabled"
        )

        self.activity_log.see("end")

        # self.app.update_idletasks()

    def stop_scan(self):
        self.stop_requested = True
        self.status_label.configure(
            text="Status: Stopping..."
        )
    
    def reset_scan_ui(self):

        self.status_label.configure(
            text="Status: Ready"
        )

        self.total_images_label.configure(
            text="Total Images: 0"
        )

        self.number_scanned_label.configure(
            text="Files Scanned: 0"
        )

        self.number_flagged_label.configure(
            text="Files Flagged: 0"
        )

        self.progress_bar.set(0)

        self.progress_label.configure(
            text="Progress: 0%"
        )

        self.started_label.configure(
            text="Started:"
        )

        self.finished_label.configure(
            text="Finished:"
        )

        self.duration_label.configure(
            text="Duration:"
        )

        self.activity_log.delete(
            "1.0",
            "end"
        )     

app = ImageSentinelApp()
app.run()