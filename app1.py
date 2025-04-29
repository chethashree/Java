from flask import Flask, jsonify, render_template, send_file, request
from PIL import ImageGrab
import os
import datetime
import base64
import xml.etree.ElementTree as ET

app = Flask(__name__)
SCREENSHOT_DIR = "screenshots"
XML_FILE = "screenshots.xml"

# === Helper: Take screenshot ===
def take_screenshot_and_save():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'screenshot_{timestamp}.png'
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    ImageGrab.grab().save(filepath)
    save_to_xml(filepath)
    return filename

# === Helper: Save base64 screenshot in XML ===
def save_to_xml(image_path):
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
    except (FileNotFoundError, ET.ParseError):
        root = ET.Element('Screenshots')
        tree = ET.ElementTree(root)

    with open(image_path, 'rb') as img:
        b64 = base64.b64encode(img.read()).decode('utf-8')

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = ET.SubElement(root, 'Screenshot', attrib={'timestamp': timestamp})
    ET.SubElement(entry, 'Image').text = b64
    tree.write(XML_FILE)

# === Routes ===
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/take_screenshot', methods=['POST'])
def take_screenshot():
    filename = take_screenshot_and_save()
    return jsonify({"filename": filename})

@app.route('/gallery')
def gallery():
    files = sorted(os.listdir(SCREENSHOT_DIR), reverse=True)
    return jsonify([f for f in files if f.endswith(".png")])

@app.route('/image/<filename>')
def get_image(filename):
    return send_file(os.path.join(SCREENSHOT_DIR, filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
