import json
import os
def enable_autostart():
    """Enable auto-start on login using a macOS LaunchAgent plist."""
    plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hapticapp.autostart</string>
    <key>ProgramArguments</key>
    <array>
        <string>{os.path.abspath(__file__)}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
'''
    launch_agents_dir = os.path.expanduser('~/Library/LaunchAgents')
    if not os.path.exists(launch_agents_dir):
        os.makedirs(launch_agents_dir)
    plist_path = os.path.join(launch_agents_dir, 'com.hapticapp.autostart.plist')
    with open(plist_path, 'w') as f:
        f.write(plist_content)
    os.system(f'launchctl load -w "{plist_path}"')
    print(f"Auto-start enabled. Plist created at {plist_path}")

def disable_autostart():
    """Disable auto-start on login by removing the LaunchAgent plist."""
    plist_path = os.path.expanduser('~/Library/LaunchAgents/com.hapticapp.autostart.plist')
    if os.path.exists(plist_path):
        os.system(f'launchctl unload -w "{plist_path}"')
        os.remove(plist_path)
        print("Auto-start disabled.")
    else:
        print("Auto-start was not enabled.")
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
# New: Haptic intensity (0-100)
haptic_intensity = 50  # Default intensity

# Haptic event statistics
haptic_event_count = 0
haptic_event_times = []  # List of timestamps

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

last_mouse_pos = None
last_haptic_time = None
listener = None

def perform_haptic_feedback():
    global haptic_event_count, haptic_event_times
    try:
        # If your haptic library supports intensity, pass haptic_intensity here.
        # For now, just print it for demonstration.
        print(f"Haptic feedback performed. Intensity: {haptic_intensity}")
        Haptic.perform(Pattern.generic, Time.now)
        haptic_event_count += 1
        haptic_event_times.append(time.strftime('%Y-%m-%d %H:%M:%S'))
        if hasattr(HapticApp, 'update_stats_label_instance') and HapticApp.update_stats_label_instance:
            HapticApp.update_stats_label_instance()
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
    def add_profiles_ui(self, layout):
        self.profiles_label = QtWidgets.QLabel('Preset Profiles:')
        layout.addWidget(self.profiles_label)
        self.profiles_combo = QtWidgets.QComboBox()
        self.load_profiles()
        self.profiles_combo.currentIndexChanged.connect(self.profile_selected)
        layout.addWidget(self.profiles_combo)
        self.save_profile_button = QtWidgets.QPushButton('Save Profile')
        self.save_profile_button.clicked.connect(self.save_profile)
        layout.addWidget(self.save_profile_button)
        self.delete_profile_button = QtWidgets.QPushButton('Delete Profile')
        self.delete_profile_button.clicked.connect(self.delete_profile)
        layout.addWidget(self.delete_profile_button)

    def get_profiles_path(self):
        return os.path.expanduser('~/.haptic_app_profiles.json')

    def load_profiles(self):
        self.profiles = {}
        path = self.get_profiles_path()
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    self.profiles = json.load(f)
            except Exception as e:
                print(f'Error loading profiles: {e}')
        self.profiles_combo.clear()
        self.profiles_combo.addItem('Select Profile')
        for name in self.profiles:
            self.profiles_combo.addItem(name)

    def save_profile(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Save Profile', 'Enter profile name:')
        if ok and name:
            self.profiles[name] = {
                'cooldown': self.cooldown_entry.text(),
                'distance': self.distance_entry.text(),
                'duration': self.duration_entry.text(),
                'frequency': self.frequency_entry.text(),
                'intensity': self.intensity_slider.value()
            }
            try:
                with open(self.get_profiles_path(), 'w') as f:
                    json.dump(self.profiles, f)
                print(f'Profile "{name}" saved.')
                self.load_profiles()
            except Exception as e:
                print(f'Error saving profile: {e}')

    def profile_selected(self, idx):
        if idx <= 0:
            return
        name = self.profiles_combo.currentText()
        if name in self.profiles:
            p = self.profiles[name]
            self.cooldown_entry.setText(p.get('cooldown', str(haptic_cooldown)))
            self.distance_entry.setText(p.get('distance', str(haptic_min_pixel_distance)))
            self.duration_entry.setText(p.get('duration', str(haptic_duration)))
            self.frequency_entry.setText(p.get('frequency', str(haptic_frequency)))
            self.intensity_slider.setValue(int(p.get('intensity', haptic_intensity)))
            print(f'Profile "{name}" loaded.')

    def delete_profile(self):
        idx = self.profiles_combo.currentIndex()
        if idx <= 0:
            return
        name = self.profiles_combo.currentText()
        if name in self.profiles:
            confirm = QtWidgets.QMessageBox.question(self, 'Delete Profile', f'Delete profile "{name}"?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if confirm == QtWidgets.QMessageBox.Yes:
                del self.profiles[name]
                try:
                    with open(self.get_profiles_path(), 'w') as f:
                        json.dump(self.profiles, f)
                    print(f'Profile "{name}" deleted.')
                    self.load_profiles()
                except Exception as e:
                    print(f'Error deleting profile: {e}')
    def add_autostart_ui(self, layout):
        self.autostart_checkbox = QtWidgets.QCheckBox('Auto-start on Login')
        self.autostart_checkbox.setChecked(self.is_autostart_enabled())
        self.autostart_checkbox.stateChanged.connect(self.toggle_autostart)
        layout.addWidget(self.autostart_checkbox)

    def is_autostart_enabled(self):
        plist_path = os.path.expanduser('~/Library/LaunchAgents/com.hapticapp.autostart.plist')
        return os.path.exists(plist_path)

    def toggle_autostart(self, state):
        if state == QtCore.Qt.Checked:
            enable_autostart()
        else:
            disable_autostart()
    def update_stats_label(self):
        global haptic_event_count, haptic_event_times
        self.stats_label.setText(f"Haptic Events: {haptic_event_count}\nLast: {haptic_event_times[-1] if haptic_event_times else 'N/A'}")

    def add_custom_pattern_ui(self, layout):
        # Section for custom haptic pattern
        self.pattern_label = QtWidgets.QLabel('Custom Haptic Pattern (ms, comma-separated):')
        layout.addWidget(self.pattern_label)
        self.pattern_entry = QtWidgets.QLineEdit()
        self.pattern_entry.setPlaceholderText('e.g. 30,60,30')
        layout.addWidget(self.pattern_entry)
        self.pattern_button = QtWidgets.QPushButton('Play Custom Pattern')
        self.pattern_button.clicked.connect(self.play_custom_pattern)
        layout.addWidget(self.pattern_button)

    def play_custom_pattern(self):
        pattern_text = self.pattern_entry.text()
        try:
            durations = [int(x.strip()) for x in pattern_text.split(',') if x.strip()]
            if not durations:
                print('No valid pattern entered.')
                return
            print(f'Playing custom haptic pattern: {durations}')
            for duration in durations:
                # If your haptic library supports custom durations, use it here
                # For demonstration, we use the global haptic_intensity and sleep
                print(f'Haptic: {duration}ms, Intensity: {haptic_intensity}')
                Haptic.perform(Pattern.generic, Time.now)
                QtCore.QThread.msleep(duration)
        except Exception as e:
            print(f'Error playing custom pattern: {e}')

    def keyPressEvent(self, event):
        # Hotkey: Ctrl+H triggers haptic feedback, Ctrl+L toggles listener
        if event.modifiers() & QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_H:
                print('Hotkey Ctrl+H: Trigger haptic feedback')
                perform_haptic_feedback()
            elif event.key() == QtCore.Qt.Key_L:
                if listener is None:
                    print('Hotkey Ctrl+L: Start listener')
                    start_listener()
                else:
                    print('Hotkey Ctrl+L: Stop listener')
                    stop_listener()
        super().keyPressEvent(event)
    def __init__(self):
        super().__init__()
        self.tray_icon = None
        self.show_in_menubar = True  # Default: show in menubar
        # For static callback from perform_haptic_feedback
        HapticApp.update_stats_label_instance = self.update_stats_label
        self.initUI()
        if self.show_in_menubar:
            self.initTray()
        # Start the haptic listener automatically when the app opens
        start_listener()


    def initUI(self):
        global haptic_cooldown, haptic_min_pixel_distance, haptic_duration, haptic_frequency, haptic_intensity

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

        # --- Intensity Slider ---
        self.intensity_label = QtWidgets.QLabel('Haptic Intensity (0-100):')
        layout.addWidget(self.intensity_label)
        self.intensity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.intensity_slider.setMinimum(0)
        self.intensity_slider.setMaximum(100)
        self.intensity_slider.setValue(haptic_intensity)
        self.intensity_slider.setTickInterval(10)
        self.intensity_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.intensity_slider.valueChanged.connect(self.update_intensity)
        layout.addWidget(self.intensity_slider)

        self.show_menubar_checkbox = QtWidgets.QCheckBox('Show in Menubar')
        self.show_menubar_checkbox.setChecked(self.show_in_menubar)
        self.show_menubar_checkbox.stateChanged.connect(self.toggle_menubar)
        layout.addWidget(self.show_menubar_checkbox)

        self.update_button = QtWidgets.QPushButton('Update Settings')
        self.update_button.clicked.connect(self.update_settings)
        layout.addWidget(self.update_button)

        self.start_button = QtWidgets.QPushButton('Start Listener')
        self.start_button.clicked.connect(start_listener)
        layout.addWidget(self.start_button)

        self.stop_button = QtWidgets.QPushButton('Stop Listener')
        self.stop_button.clicked.connect(stop_listener)
        layout.addWidget(self.stop_button)



        # Add profiles UI
        self.add_profiles_ui(layout)

        # Add custom pattern UI
        self.add_custom_pattern_ui(layout)

        # Add autostart UI
        self.add_autostart_ui(layout)

        # --- Haptic Event Statistics ---
        self.stats_label = QtWidgets.QLabel()
        self.update_stats_label()
        layout.addWidget(self.stats_label)

        self.setLayout(layout)
        self.setWindowTitle('Haptic Feedback Settings')
        self.resize(350, 420)

    def toggle_menubar(self, state):
        if state == QtCore.Qt.Checked:
            if not self.tray_icon:
                self.initTray()
            self.show_in_menubar = True
        else:
            if self.tray_icon:
                self.tray_icon.hide()
                self.tray_icon = None
            self.show_in_menubar = False

    def initTray(self):
        # Set up the system tray icon and menu
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        # Use a standard icon
        self.tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))

        tray_menu = QtWidgets.QMenu()

        show_action = tray_menu.addAction('Show/Hide Window')
        show_action.triggered.connect(self.toggle_window)

        start_action = tray_menu.addAction('Start Listener')
        start_action.triggered.connect(start_listener)

        stop_action = tray_menu.addAction('Stop Listener')
        stop_action.triggered.connect(stop_listener)

        quit_action = tray_menu.addAction('Quit')
        quit_action.triggered.connect(QtWidgets.QApplication.instance().quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Minimize to tray on close
        self.tray_icon.activated.connect(self.on_tray_activated)

    def on_tray_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.toggle_window()

    def toggle_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def closeEvent(self, event):
        # Override close event to minimize to tray instead of quitting
        event.ignore()
        self.hide()

    def update_intensity(self, value):
        global haptic_intensity
        haptic_intensity = value
        print(f"Updated intensity: {haptic_intensity}")

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
