import subprocess
import platform
import os 
from datetime import datetime

class ScreenRecorder:
    @staticmethod
    def start(settings):
        s = settings 

        filters = []
        t = float(s.get("crop_t", 0))/100
        b = float(s.get("crop_b", 0))/100
        l = float(s.get("crop_l", 0))/100
        r = float(s.get("crop_r", 0))/100
        
        if t > 0 or b > 0 or l > 0 or r > 0:
            filters.append(f"crop=in_w*{1-l-r}:in_h*{1-t-b}:in_w*{l}:in_h*{t}")
            
        w_px = int(s["width_px"])
        filters.append(f"scale={w_px}:trunc(ih*{w_px}/iw/2)*2")
            
        if s["color"] == "Grayscale":
            filters.append("format=gray")
        elif s["color"] == "8-Shade Gray":
            filters.append("format=gray,lut=y='bitand(val,224)'")

        filter_str = ",".join(filters)

        os_name = platform.system()
        if os_name == "Windows": capture_args = ["-f", "gdigrab", "-i", "desktop"]
        elif os_name == "Darwin": capture_args = ["-f", "avfoundation", "-i", "1:0"]
        else: capture_args = ["-f", "x11grab", "-i", ":0.0"]

        datestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"Capture_{datestamp}"
        mode = s.get("capture_mode", "Video Only")
        save_dir = s.get("save_dir", "")
        
        # --- BASE COMMAND & INPUT ---
        command = ["ffmpeg", "-y", "-framerate", s["fps"]] + capture_args
        
        primary_output = None

        # --- OUTPUT 1: VIDEO ---
        if mode in ["Video Only", "Video & Picture"]:
            video_filename = f"{base_name}{s.get('ext', '.mp4')}"
            video_output = os.path.join(save_dir, video_filename) if save_dir else video_filename
            primary_output = video_output
            
            if filter_str: 
                command.extend(["-vf", filter_str])
            
            command.extend(["-c:v", "libx264", "-crf", str(s["crf"]), "-preset", s["preset"]])
            if s["tune"] != "none": 
                command.extend(["-tune", s["tune"]])
                
            command.append(video_output)

        # --- OUTPUT 2: SCREENSHOTS ---
        if mode in ["Picture Only", "Video & Picture"]:
            img_folder_name = f"{base_name}_Images"
            img_folder_path = os.path.join(save_dir, img_folder_name) if save_dir else img_folder_name
            os.makedirs(img_folder_path, exist_ok=True)

            img_ext = s.get("img_ext", ".jpg")
            screenshot_filename = f"{base_name}_%04d{img_ext}"
            screenshot_output = os.path.join(img_folder_path, screenshot_filename)

            interval = int(s.get("screenshot_interval", 60))
            fps_filter = f"fps=1/{interval}"
            screenshot_filters = f"{filter_str},{fps_filter}" if filter_str else fps_filter
            
            if primary_output is None:
                primary_output = img_folder_path
                
            # Apply filters
            command.extend(["-vf", screenshot_filters])
            
            # Apply Image Compression (Only really effective for lossy formats like JPG)
            if img_ext in [".jpg", ".jpeg"]:
                command.extend(["-q:v", str(s.get("img_q", "5"))])
                
            command.append(screenshot_output)

        # --- SILENT EXECUTION ---
        creation_flags = subprocess.CREATE_NO_WINDOW if os_name == "Windows" else 0
        
        process = subprocess.Popen(
            command, 
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL, 
            creationflags=creation_flags
        )
        return process, primary_output

    @staticmethod
    def stop(process):
        """Safely shuts down the FFmpeg process."""
        if process:
            try:
                process.stdin.write(b'q\n')
                process.stdin.flush()
            except Exception:
                pass
            finally:
                try:
                    process.stdin.close()
                except Exception:
                    pass