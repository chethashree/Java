# import os
# import sys
# from datetime import datetime
# from PIL import ImageGrab
# import xml.etree.ElementTree as ET

# from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
# from PyQt5.QtCore import Qt, QTimer, QPoint, QEvent

# # Configuration
# SAVE_DIR = "screenshots"
# XML_FILE = "screenshot_log.xml"
# CAPTURE_INTERVAL = 30  # seconds

# os.makedirs(SAVE_DIR, exist_ok=True)

# def init_xml():
#     if not os.path.exists(XML_FILE):
#         root = ET.Element("screenshots")
#         tree = ET.ElementTree(root)
#         tree.write(XML_FILE)
#     return ET.parse(XML_FILE)

# def log_screenshot(filename, timestamp):
#     tree = init_xml()
#     root = tree.getroot()
#     entry = ET.SubElement(root, "screenshot")
#     ET.SubElement(entry, "filename").text = filename
#     ET.SubElement(entry, "timestamp").text = timestamp
#     tree.write(XML_FILE)

# def take_screenshot():
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     filename = f"screenshot_{timestamp}.png"
#     path = os.path.join(SAVE_DIR, filename)
#     img = ImageGrab.grab()
#     img.save(path)
#     log_screenshot(filename, timestamp)
#     print(f"[✓] Screenshot saved: {filename}")

# class FloatingScreenshotButton(QWidget):
#     def _init_(self):
#         super()._init_()
#         self.drag_position = None
#         self.mouse_moved = False
#         self.initUI()
#         self.start_auto_capture()

#     def initUI(self):
#         self.setWindowTitle("Screenshot Tool")
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setFixedSize(130, 60)

#         self.button = QPushButton("📸 Capture", self)
#         self.button.setGeometry(15, 15, 100, 30)
#         self.button.setToolTip("Click to take a screenshot")
#         self.button.clicked.connect(take_screenshot)
#         self.button.setStyleSheet("""
#             QPushButton {
#                 background-color: #4CAF50;
#                 color: white;
#                 border-radius: 10px;
#                 font-weight: bold;
#             }
#             QPushButton:hover {
#                 background-color: #45a049;
#             }
#         """)

#         self.setStyleSheet("background-color: rgba(255, 255, 255, 0.85); border-radius: 15px;")
#         self.button.installEventFilter(self)
#         self.show()

#     def start_auto_capture(self):
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(take_screenshot)
#         self.timer.start(CAPTURE_INTERVAL * 1000)

#     def eventFilter(self, source, event):
#         if source == self.button:
#             if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
#                 self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
#                 self.mouse_moved = False
#                 return False  # let the button still respond to click

#             elif event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton:
#                 if self.drag_position:
#                     self.mouse_moved = True
#                     self.move(event.globalPos() - self.drag_position)
#                     return True  # prevent click while dragging

#             elif event.type() == QEvent.MouseButtonRelease:
#                 self.drag_position = None
#                 if self.mouse_moved:
#                     return True  # block click if it was a drag
#                 else:
#                     return False  # allow click

#         return super().eventFilter(source, event)

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
#             self.mouse_moved = False
#             event.accept()

#     def mouseMoveEvent(self, event):
#         if event.buttons() & Qt.LeftButton and self.drag_position:
#             self.mouse_moved = True
#             self.move(event.globalPos() - self.drag_position)
#             event.accept()

#     def mouseReleaseEvent(self, event):
#         self.drag_position = None

# if __name__ == "_main_":
#     app = QApplication(sys.argv)
#     window = FloatingScreenshotButton()
#     sys.exit(app.exec_())


import os
import time
from datetime import datetime
from PIL import ImageGrab
import xml.etree.ElementTree as ET

# Configuration
SAVE_DIR = "screenshots"
XML_FILE = "screenshot_log.xml"
CAPTURE_INTERVAL = 30  # seconds

# Create directory if it doesn't exist
os.makedirs(SAVE_DIR, exist_ok=True)

# Initialize XML if not present
def init_xml():
    if not os.path.exists(XML_FILE):
        root = ET.Element("screenshots")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)
    return ET.parse(XML_FILE)

# Log screenshot data to XML
def log_screenshot(filename, timestamp):
    tree = init_xml()
    root = tree.getroot()
    entry = ET.SubElement(root, "screenshot")
    ET.SubElement(entry, "filename").text = filename
    ET.SubElement(entry, "timestamp").text = timestamp
    tree.write(XML_FILE)

# Take screenshot and save it
def take_screenshot():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    path = os.path.join(SAVE_DIR, filename)
    img = ImageGrab.grab()
    img.save(path)
    log_screenshot(filename, timestamp)
    print(f"[✓] Screenshot saved: {filename}")

# Main loop
def main():
    print(f"[INFO] Starting automatic screenshot capture every {CAPTURE_INTERVAL} seconds...")
    while True:
        take_screenshot()
        time.sleep(CAPTURE_INTERVAL)

if __name__ == "__main__":
    main()
