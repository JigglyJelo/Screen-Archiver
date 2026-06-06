# Screen Archiver

A lightweight, robust screen recording and screenshot utility built with Python and FFmpeg. Featuring a modern GUI, persistent settings, and system tray integration, Screen Archiver is designed to run silently in the background while capturing your desktop.

## Features

* **Modern GUI:** Simple and intuitive interface powered by `customtkinter`.
* **Dual-Process Capture:** Records video and captures periodic screenshots simultaneously.
* **Persistent Settings:** Automatically saves your configurations (resolution, FPS, formatting, save paths) to a `settings.json` file for your next session.
* **System Tray Integration:** Minimizes to the system tray (`pystray`) while recording to keep your taskbar clean.
* **Silent Execution:** Runs natively as a `.pyw` file to prevent unsightly command prompt windows from appearing.
* **Highly Customizable:** Tweak FFmpeg parameters including CRF, encoder presets, tunes, crop margins, and color spaces directly from the UI.

## Prerequisites

Before running the application, ensure you have the following installed:

1. **Python 3.x**
2. **FFmpeg:** Must be installed and added to your system's environmental `PATH`.
   * *Verify by opening a terminal and typing `ffmpeg -version`.*

## Installation

1. Clone or download this repository.
22. Install the required dependencies using pip:
   `pip install -r requirements.txt`

## Usage

Since this app is designed to run silently without a console, the main script should be run as a `.pyw` file.

1. Double-click the main Python file (e.g., `gui_main.pyw`).
2. Click **⚙️ Settings** to configure your output directory, format, and capture options.
3. Click **▶ Record** to start capturing. The app will minimize to your system tray.
4. To stop recording, click the red recording icon in your system tray and select **Show App**, then click **■ Stop**.

## License

This project is licensed under the GNU General Public License v3.0 or later. See the [LICENSE](LICENSE) file for details.