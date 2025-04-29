import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab
import base64
import datetime
import os
import xml.etree.ElementTree as ET
import threading
import time  # <-- Import time module here

from flask import Flask, send_file

# === Screenshot + XML Logic ===
def take_screenshot_and_save():
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'screenshot_{timestamp}.png'
    filepath = os.path.join('screenshots', filename)

    os.makedirs('screenshots', exist_ok=True)
    ImageGrab.grab().save(filepath)  # ← Using Pillow here

    save_to_xml(filepath)
    return filepath

def save_to_xml(image_path):
    xml_file = 'screenshots.xml'
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except (FileNotFoundError, ET.ParseError):
        root = ET.Element('Screenshots')
        tree = ET.ElementTree(root)

    with open(image_path, 'rb') as img:
        b64 = base64.b64encode(img.read()).decode('utf-8')

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = ET.SubElement(root, 'Screenshot', attrib={'timestamp': timestamp})
    ET.SubElement(entry, 'Image').text = b64
    tree.write(xml_file)

# === Floating Button UI ===
def create_floating_button():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.geometry('100x50+100+100')

    def move(event):
        root.geometry(f'+{event.x_root}+{event.y_root}')

    def capture():
        take_screenshot_and_save()

    btn = ttk.Button(root, text="📸", command=capture)
    btn.pack(expand=True, fill='both')
    btn.bind('<B1-Motion>', move)

    root.mainloop()

# === Flask Web App ===
app = Flask(__name__)

@app.route('/')
def index():
    files = sorted(os.listdir('screenshots'), reverse=True)
    gallery_html = """
    <html>
      <head>
        <title>Screenshot Gallery</title>
        <meta http-equiv="refresh" content="2">
        <style>
          body { font-family: sans-serif; padding: 20px; background: #f4f4f4; }
          .grid { display: flex; flex-wrap: wrap; gap: 15px; }
          .card { background: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
          .card img { max-width: 300px; height: auto; display: block; }
          .card p { margin: 5px 0 0; font-size: 0.9em; color: #555; }
        </style>
      </head>
      <body>
        <h1>📸 Screenshot Gallery</h1>
        <p>Auto-refreshes every 10 seconds</p>
        <div class="grid">
    """
    for f in files:
        if f.lower().endswith('.png'):
            timestamp = f.replace("screenshot_", "").replace(".png", "")
            gallery_html += f"""
              <div class="card">
                <img src="/image/{f}" alt="{f}">
                <p>{timestamp}</p>
              </div>
            """

    gallery_html += """
        </div>
      </body>
    </html>
    """
    return gallery_html

@app.route('/image/<filename>')
def serve_specific_image(filename):
    return send_file(os.path.join('screenshots', filename), mimetype='image/png')

def run_flask():
    app.run(port=5001)

# === Auto Screenshot Every 10 Seconds ===
def auto_screenshot():
    while True:
        take_screenshot_and_save()
        time.sleep(10)  # Take screenshot every 10 seconds

# === Run Both ===
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()  # Start Flask
    threading.Thread(target=auto_screenshot, daemon=True).start()  # Start auto screenshot
    create_floating_button()  # Start floating button