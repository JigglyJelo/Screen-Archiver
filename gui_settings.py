import customtkinter as ctk
from customtkinter import filedialog

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Settings")
        self.geometry("500x750")
        self.attributes("-topmost", True)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 1. FPS
        ctk.CTkLabel(self.scroll_frame, text="FPS (e.g., '30' or '1/5'):").pack()
        self.fps_entry = ctk.CTkEntry(self.scroll_frame, width=100)
        self.fps_entry.insert(0, master.settings["fps"])
        self.fps_entry.pack(pady=(0, 15))

        # 2. CRF
        ctk.CTkLabel(self.scroll_frame, text="CRF Quality (Range: 0-51, Lower is better):").pack()
        self.crf_entry = ctk.CTkEntry(self.scroll_frame, width=100)
        self.crf_entry.insert(0, str(master.settings["crf"]))
        self.crf_entry.pack(pady=(0, 15))

        # 3. Width
        ctk.CTkLabel(self.scroll_frame, text="Resolution Width (Pixels, e.g., 960 or 1920):").pack()
        self.width_entry = ctk.CTkEntry(self.scroll_frame, width=100)
        self.width_entry.insert(0, str(master.settings["width_px"]))
        self.width_entry.pack(pady=(0, 15))

        # 4. Cropping
        ctk.CTkLabel(self.scroll_frame, text="Crop Margins (% to remove - T/B/L/R):").pack()
        self.crop_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.crop_frame.pack(pady=(0, 15))
        
        self.crop_t = ctk.CTkEntry(self.crop_frame, width=50); self.crop_t.insert(0, master.settings["crop_t"])
        self.crop_b = ctk.CTkEntry(self.crop_frame, width=50); self.crop_b.insert(0, master.settings["crop_b"])
        self.crop_l = ctk.CTkEntry(self.crop_frame, width=50); self.crop_l.insert(0, master.settings["crop_l"])
        self.crop_r = ctk.CTkEntry(self.crop_frame, width=50); self.crop_r.insert(0, master.settings["crop_r"])
        
        for w in [self.crop_t, self.crop_b, self.crop_l, self.crop_r]:
            w.pack(side="left", padx=2)

        # 5. Format & Color Mode
        ctk.CTkLabel(self.scroll_frame, text="Output Format & Color:").pack()
        self.fc_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.fc_frame.pack(pady=(0, 15))
        
        self.format_menu = ctk.CTkOptionMenu(self.fc_frame, values=[".mp4", ".mkv", ".mov", ".avi"])
        self.format_menu.set(master.settings["ext"])
        self.format_menu.pack(side="left", padx=5)
        
        self.color_menu = ctk.CTkOptionMenu(self.fc_frame, values=["Full Color", "Grayscale", "8-Shade Gray"])
        self.color_menu.set(master.settings["color"])
        self.color_menu.pack(side="left", padx=5)

        # 6. Encoder Settings
        ctk.CTkLabel(self.scroll_frame, text="Encoder Settings:").pack()
        self.enc_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.enc_frame.pack(pady=(0, 25))

        self.preset_menu = ctk.CTkOptionMenu(self.enc_frame, values=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"])
        self.preset_menu.set(master.settings["preset"])
        self.preset_menu.pack(side="left", padx=5)

        self.tune_menu = ctk.CTkOptionMenu(self.enc_frame, values=["none", "film", "animation", "stillimage", "zerolatency"])
        self.tune_menu.set(master.settings["tune"])
        self.tune_menu.pack(side="left", padx=5)

        # 7. Save Directory (NEW)
        ctk.CTkLabel(self.scroll_frame, text="Save Directory:").pack()
        self.dir_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.dir_frame.pack(pady=(0, 15))

        self.dir_entry = ctk.CTkEntry(self.dir_frame, width=200)
        self.dir_entry.insert(0, master.settings.get("save_dir", ""))
        self.dir_entry.pack(side="left", padx=(0, 5))

        self.browse_btn = ctk.CTkButton(self.dir_frame, text="Browse", width=60, command=self.browse_directory)
        self.browse_btn.pack(side="left")

        # Save Button
        self.save_btn = ctk.CTkButton(self.scroll_frame, text="Save & Close", command=self.save_and_close)
        self.save_btn.pack(pady=20)

    def browse_directory(self):
        """Opens a file dialog to pick a folder."""
        directory = filedialog.askdirectory()
        if directory: # If the user didn't hit cancel
            self.dir_entry.delete(0, 'end')
            self.dir_entry.insert(0, directory)

    def save_and_close(self):
        self.master.settings.update({
            "fps": self.fps_entry.get(),
            "crf": self.crf_entry.get(),
            "width_px": self.width_entry.get(),
            "crop_t": self.crop_t.get() or "0",
            "crop_b": self.crop_b.get() or "0",
            "crop_l": self.crop_l.get() or "0",
            "crop_r": self.crop_r.get() or "0",
            "ext": self.format_menu.get(),
            "color": self.color_menu.get(),
            "preset": self.preset_menu.get(),
            "tune": self.tune_menu.get(),
            "save_dir": self.dir_entry.get()
        })
        self.destroy()