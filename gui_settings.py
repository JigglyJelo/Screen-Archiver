import json
import customtkinter as ctk
from customtkinter import filedialog

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Settings")
        self.geometry("550x750") 
        self.attributes("-topmost", True)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- 1. CAPTURE MODE ---
        ctk.CTkLabel(self.scroll_frame, text="1. Capture Mode", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        
        self.mode_menu = ctk.CTkOptionMenu(self.scroll_frame, values=["Video Only", "Picture Only", "Video & Picture"])
        self.mode_menu.set(master.settings.get("capture_mode", "Video Only"))
        self.mode_menu.pack(pady=(0, 15))


        # --- 2. GLOBAL SETTINGS (Video & Image) ---
        ctk.CTkLabel(self.scroll_frame, text="2. Global Settings", font=("Arial", 16, "bold")).pack(pady=(15, 5))

        # Color Mode
        ctk.CTkLabel(self.scroll_frame, text="Color Mode:").pack()
        self.color_menu = ctk.CTkOptionMenu(self.scroll_frame, values=["Full Color", "Grayscale", "8-Shade Gray"])
        self.color_menu.set(master.settings.get("color", "Full Color"))
        self.color_menu.pack(pady=(0, 10))

        # Resolution Width
        ctk.CTkLabel(self.scroll_frame, text="Resolution Width (Pixels):").pack()
        self.width_entry = ctk.CTkEntry(self.scroll_frame, width=100)
        self.width_entry.insert(0, str(master.settings.get("width_px", "1280")))
        self.width_entry.pack(pady=(0, 10))

        # Crop Margins
        ctk.CTkLabel(self.scroll_frame, text="Crop Margins (% to remove - T/B/L/R):").pack()
        self.crop_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.crop_frame.pack(pady=(0, 15))
        
        self.crop_t = ctk.CTkEntry(self.crop_frame, width=50); self.crop_t.insert(0, master.settings.get("crop_t", "0"))
        self.crop_b = ctk.CTkEntry(self.crop_frame, width=50); self.crop_b.insert(0, master.settings.get("crop_b", "0"))
        self.crop_l = ctk.CTkEntry(self.crop_frame, width=50); self.crop_l.insert(0, master.settings.get("crop_l", "0"))
        self.crop_r = ctk.CTkEntry(self.crop_frame, width=50); self.crop_r.insert(0, master.settings.get("crop_r", "0"))
        
        for w in [self.crop_t, self.crop_b, self.crop_l, self.crop_r]:
            w.pack(side="left", padx=2)


        # --- 3. VIDEO SETTINGS ---
        ctk.CTkLabel(self.scroll_frame, text="3. Video Settings", font=("Arial", 16, "bold")).pack(pady=(15, 5))

        # Row 1: Format & FPS
        self.vid_row1 = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.vid_row1.pack(pady=(0, 10))
        
        ctk.CTkLabel(self.vid_row1, text="Format:").pack(side="left", padx=(0, 5))
        self.format_menu = ctk.CTkOptionMenu(self.vid_row1, values=[".mp4", ".mkv", ".mov", ".avi"], width=80)
        self.format_menu.set(master.settings.get("ext", ".mp4"))
        self.format_menu.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(self.vid_row1, text="FPS:").pack(side="left", padx=(0, 5))
        self.fps_entry = ctk.CTkEntry(self.vid_row1, width=70)
        self.fps_entry.insert(0, master.settings.get("fps", "30"))
        self.fps_entry.pack(side="left")

        # Row 2: CRF, Preset, Tune
        self.vid_row2 = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.vid_row2.pack(pady=(0, 15))
        
        ctk.CTkLabel(self.vid_row2, text="CRF:").pack(side="left", padx=(0, 5))
        self.crf_entry = ctk.CTkEntry(self.vid_row2, width=40)
        self.crf_entry.insert(0, str(master.settings.get("crf", "28")))
        self.crf_entry.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(self.vid_row2, text="Preset:").pack(side="left", padx=(0, 5))
        self.preset_menu = ctk.CTkOptionMenu(self.vid_row2, values=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"], width=100)
        self.preset_menu.set(master.settings.get("preset", "ultrafast"))
        self.preset_menu.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(self.vid_row2, text="Tune:").pack(side="left", padx=(0, 5))
        self.tune_menu = ctk.CTkOptionMenu(self.vid_row2, values=["none", "film", "animation", "stillimage", "zerolatency"], width=100)
        self.tune_menu.set(master.settings.get("tune", "zerolatency"))
        self.tune_menu.pack(side="left")


        # --- 4. IMAGE SETTINGS ---
        ctk.CTkLabel(self.scroll_frame, text="4. Image Settings", font=("Arial", 16, "bold")).pack(pady=(15, 5))

        # Row 1: Format, Interval, Comp
        self.img_row1 = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.img_row1.pack(pady=(0, 15))

        ctk.CTkLabel(self.img_row1, text="Format:").pack(side="left", padx=(0, 5))
        self.img_format_menu = ctk.CTkOptionMenu(self.img_row1, values=[".jpg", ".png", ".bmp"], width=70)
        self.img_format_menu.set(master.settings.get("img_ext", ".jpg"))
        self.img_format_menu.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(self.img_row1, text="Interval (s):").pack(side="left", padx=(0, 5))
        self.ss_interval = ctk.CTkEntry(self.img_row1, width=50)
        self.ss_interval.insert(0, str(master.settings.get("screenshot_interval", "60")))
        self.ss_interval.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(self.img_row1, text="JPG Comp:").pack(side="left", padx=(0, 5))
        self.img_q_entry = ctk.CTkEntry(self.img_row1, width=40)
        self.img_q_entry.insert(0, str(master.settings.get("img_q", "5")))
        self.img_q_entry.pack(side="left")


        # --- 5. SAVE DIRECTORY ---
        ctk.CTkLabel(self.scroll_frame, text="5. Save Directory", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        
        self.dir_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.dir_frame.pack(pady=(0, 15))

        self.dir_entry = ctk.CTkEntry(self.dir_frame, width=250)
        self.dir_entry.insert(0, master.settings.get("save_dir", ""))
        self.dir_entry.pack(side="left", padx=(0, 5))

        self.browse_btn = ctk.CTkButton(self.dir_frame, text="Browse", width=60, command=self.browse_directory)
        self.browse_btn.pack(side="left")


        # --- SAVE BUTTON ---
        self.save_btn = ctk.CTkButton(self.scroll_frame, text="Save & Close", command=self.save_and_close)
        self.save_btn.pack(pady=30)


    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory: 
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
            "img_ext": self.img_format_menu.get(),
            "img_q": self.img_q_entry.get(),
            "color": self.color_menu.get(),
            "preset": self.preset_menu.get(),
            "tune": self.tune_menu.get(),
            "save_dir": self.dir_entry.get(),
            "capture_mode": self.mode_menu.get(),
            "screenshot_interval": self.ss_interval.get()
        })
        try:
            with open(self.master.settings_file, "w") as f:
                json.dump(self.master.settings, f, indent=4)
        except Exception as e:
            #print(f"Could not save settings file: {e}")
            pass
        self.destroy()