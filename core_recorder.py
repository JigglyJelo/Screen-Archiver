import subprocess
import platform
import os 
from datetime import datetime

class ScreenRecorder:
    @staticmethod
    def start(settings):
        s = settings 

        filters = []
        t, b, l, r = float(s["crop_t"])/100, float(s["crop_b"])/100, float(s["crop_l"])/100, float(s["crop_r"])/100
        
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
        filename = f"Capture_{datestamp}{s['ext']}"
        
        if s.get("save_dir"):
            output_file = os.path.join(s["save_dir"], filename)
        else:
            output_file = filename 

        command = ["ffmpeg", "-y", "-framerate", s["fps"]] + capture_args
        if filter_str: command.extend(["-vf", filter_str])
        
        command.extend(["-c:v", "libx264", "-crf", str(s["crf"]), "-preset", s["preset"]])
        if s["tune"] != "none": command.extend(["-tune", s["tune"]])
            
        command.append(output_file)

        # --- SILENT EXECUTION ---
        creation_flags = subprocess.CREATE_NO_WINDOW if os_name == "Windows" else 0
        
        process = subprocess.Popen(
            command, 
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL, 
            creationflags=creation_flags
        )
        return process, output_file

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