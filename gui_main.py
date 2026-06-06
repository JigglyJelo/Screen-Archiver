import sys
import os

# --- THE .PYW CRASH PREVENTER ---
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

import threading 
import subprocess 
import customtkinter as ctk
from datetime import datetime

import pystray
from PIL import Image, ImageDraw

from gui_settings import SettingsWindow
from core_recorder import ScreenRecorder

class RecorderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Screen Archiver") 
        self.geometry("300x180") 
        
        self.recording_process = None 
        self.settings_window = None
        self.current_output_file = None 
        self.tray_icon = None 
        
        self.start_time = None
        self.timer_id = None

        self.settings = {
            "fps": "1/5", "crf": "38", "width_px": "960",
            "crop_t": "0", "crop_b": "0", "crop_l": "0", "crop_r": "0",
            "ext": ".mkv", "img_ext": ".jpg", "img_q": "16", 
            "color": "8-Shade Gray", "preset": "veryslow", "tune": "stillimage",
            "capture_mode": "Video & Picture", "screenshot_interval": "5",
            "save_dir": os.path.join(os.path.expanduser("~"), "Videos")
        }

        self.start_btn = ctk.CTkButton(self, text="▶ Record", fg_color="green", hover_color="darkgreen", font=("Arial", 22, "bold"), height=60, command=self.toggle_recording)
        self.start_btn.pack(fill="x", padx=20, pady=(20, 10))

        self.settings_btn = ctk.CTkButton(self, text="⚙️ Settings", fg_color="gray", hover_color="darkgray", command=self.open_settings)
        self.settings_btn.pack(fill="x", padx=20)
        
        self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
        else:
            self.settings_window.focus() 

    def toggle_recording(self):
        if self.recording_process:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.settings_btn.configure(state="disabled")
        self.start_btn.configure(fg_color="red", hover_color="darkred")
        self.start_time = datetime.now()

        self.recording_process, self.current_output_file = ScreenRecorder.start(self.settings)
        self.update_timer()

    def update_timer(self):
        if self.recording_process:
            elapsed = datetime.now() - self.start_time
            total_seconds = int(elapsed.total_seconds())
            
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.start_btn.configure(text=f"■ Stop ({time_str})")
            self.timer_id = self.after(1000, self.update_timer)

    def stop_recording(self):
        if self.recording_process:
            ScreenRecorder.stop(self.recording_process)
            
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None
            
            self.start_btn.configure(text="⏳ Saving...", fg_color="gray", hover_color="gray", state="disabled")
            
            def wait_and_reset(proc):
                proc.wait() 
                try:
                    self.after(0, show_success)
                except Exception:
                    pass 

            def show_success():
                self.start_btn.configure(text="✅ Saved!", fg_color="#2b7a2b") 
                self.after(2000, reset_ui) 

            def reset_ui():
                self.start_btn.configure(text="▶ Record", fg_color="green", hover_color="darkgreen", state="normal")
                self.settings_btn.configure(state="normal")
                self.recording_process = None
                self.current_output_file = None

            threading.Thread(target=wait_and_reset, args=(self.recording_process,), daemon=True).start()

    # --- SYSTEM TRAY LOGIC ---

    def hide_window(self):
        """If recording, minimize to tray. Otherwise, actually close the app."""
        if self.recording_process:
            # --- RUNS ONLY IF RECORDING ---
            self.withdraw() # Makes the window invisible
            
            image = Image.new('RGB', (64, 64), color=(40, 40, 40))
            dc = ImageDraw.Draw(image)
            dc.ellipse((16, 16, 48, 48), fill=(220, 50, 50))
            
            menu = pystray.Menu(
                pystray.MenuItem('Show App', self.show_window, default=True),
                pystray.MenuItem('Quit', self.quit_app)
            )
            
            self.tray_icon = pystray.Icon("ScreenArchiver", image, "Screen Archiver", menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
        else:
            # --- RUNS IF NOT RECORDING ---
            self.destroy() # Completely shuts down the app

    def show_window(self, icon, item):
        self.tray_icon.stop()
        self.after(0, self.deiconify) 

    def quit_app(self, icon, item):
        self.tray_icon.stop()
        
        if self.recording_process:
            try:
                ScreenRecorder.stop(self.recording_process)
                self.recording_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.recording_process.terminate()
            except Exception:
                pass 
                
        self.after(0, self.destroy)