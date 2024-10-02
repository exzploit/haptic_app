import math
import time
from PyQt5 import QtWidgets, QtCore
from pynput import mouse
import PyTouchBar.Haptic as Haptic
from PyTouchBar.Haptic import Pattern, Time

# Change these to change the haptics' "feel"
haptic_cooldown = 20  # Min cooldown between haptic bumps
haptic_min_pixel_distance = 10  # Minimum pixels moved before another haptic bump
haptic_duration = 50  # Duration of haptic feedback in milliseconds
haptic_frequency = 1  # Frequency of haptic feedback in Hz

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

last_mouse_pos = None
last_haptic_time = None
listener = None

def perform_haptic_feedback():
    try:
        Haptic.perform(Pattern.generic, Time.now)
        print("Haptic feedback performed.")
    except Exception as e:
        print(f"Error performing haptic feedback: {e}")

def on_move(x, y):
    global last_haptic_time
    global last_mouse_pos
    curr = time.time()
    print(f"Mouse moved to ({x}, {y})")
    if (
        last_mouse_pos is None
        or distance((x, y), last_mouse_pos) > haptic_min_pixel_distance
    ):
        last_mouse_pos = (x, y)
        if (
            last_haptic_time is None
            or (curr - last_haptic_time) * 1000 > haptic_cooldown
        ):
            perform_haptic_feedback()
            last_haptic_time = curr

def start_listener():
    global listener
    if listener is None:
        listener = mouse.Listener(on_move=on_move)
        listener.start()
        print("Mouse listener started.")

def stop_listener():
    global listener
    if listener is not None:
        listener.stop()
        listener = None
        print("Mouse listener stopped.")

class HapticApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global haptic_cooldown, haptic_min_pixel_distance, haptic_duration, haptic_frequency

        layout = QtWidgets.QVBoxLayout()

        self.cooldown_label = QtWidgets.QLabel('Haptic Cooldown (ms):')
        layout.addWidget(self.cooldown_label)
        self.cooldown_entry = QtWidgets.QLineEdit(str(haptic_cooldown))
        layout.addWidget(self.cooldown_entry)

        self.distance_label = QtWidgets.QLabel('Min Pixel Distance:')
        layout.addWidget(self.distance_label)
        self.distance_entry = QtWidgets.QLineEdit(str(haptic_min_pixel_distance))
        layout.addWidget(self.distance_entry)

        self.duration_label = QtWidgets.QLabel('Haptic Duration (ms):')
        layout.addWidget(self.duration_label)
        self.duration_entry = QtWidgets.QLineEdit(str(haptic_duration))
        layout.addWidget(self.duration_entry)

        self.frequency_label = QtWidgets.QLabel('Haptic Frequency (Hz):')
        layout.addWidget(self.frequency_label)
        self.frequency_entry = QtWidgets.QLineEdit(str(haptic_frequency))
        layout.addWidget(self.frequency_entry)

        self.update_button = QtWidgets.QPushButton('Update Settings')
        self.update_button.clicked.connect(self.update_settings)
        layout.addWidget(self.update_button)

        self.start_button = QtWidgets.QPushButton('Start Listener')
        self.start_button.clicked.connect(start_listener)
        layout.addWidget(self.start_button)

        self.stop_button = QtWidgets.QPushButton('Stop Listener')
        self.stop_button.clicked.connect(stop_listener)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)
        self.setWindowTitle('Haptic Feedback Settings')
        self.show()

    def update_settings(self):
        global haptic_cooldown, haptic_min_pixel_distance, haptic_duration, haptic_frequency
        haptic_cooldown = int(self.cooldown_entry.text())
        haptic_min_pixel_distance = int(self.distance_entry.text())
        haptic_duration = int(self.duration_entry.text())
        haptic_frequency = int(self.frequency_entry.text())
        print(f"Updated settings: Cooldown={haptic_cooldown}, Min Distance={haptic_min_pixel_distance}, Duration={haptic_duration}, Frequency={haptic_frequency}")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ex = HapticApp()
    app.exec_()
