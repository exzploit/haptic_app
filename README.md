
<div align="center">
  <img src="https://img.shields.io/badge/macos-supported-brightgreen" alt="macOS Supported"/>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+"/>
</div>

# 🖱️ haptic_app

> **A customizable haptic feedback app for macOS trackpads.**

---

## ✨ Features

- Haptic feedback on mouse movement
- Fully customizable settings (cooldown, distance, duration, frequency, intensity)
- Preset profiles: save, load, and delete your favorite configurations
- Custom haptic patterns (define your own vibration sequence)
- System tray (menu bar) integration
- Auto-start on login (optional)
- Hotkey support (Ctrl+H for haptic, Ctrl+L to toggle listener)
- Real-time statistics (event count, last event)
- Easy-to-use PyQt5 GUI

---

## 🚀 Getting Started

### Prerequisites
- macOS with a Force Touch trackpad or haptic engine
- Python 3.8+
- [PyQt5](https://pypi.org/project/PyQt5/), [pynput](https://pypi.org/project/pynput/), [PyTouchBar](https://github.com/olemb/pytouchbar) (for haptic)

### Installation
```zsh
# Clone the repository
git clone <your-repo-url>
cd haptic_app

# Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install PyQt5 pynput
# (Install PyTouchBar as needed)
```

### Running the App
```zsh
python haptic_app.py
```

---

## 🛠️ Customization

You can customize the haptic feedback settings through the GUI:

- **Haptic Cooldown (ms):** Minimum cooldown between haptic bumps
- **Min Pixel Distance:** Minimum pixels moved before another haptic bump
- **Haptic Duration (ms):** Duration of haptic feedback in milliseconds
- **Haptic Frequency (Hz):** Frequency of haptic feedback in Hz
- **Haptic Intensity (0-100):** Vibration strength
- **Preset Profiles:** Save/load/delete your favorite settings
- **Custom Pattern:** Enter comma-separated durations (e.g., `30,60,30`)
- **Auto-start on Login:** Enable/disable app launch at login
- **Show in Menubar:** Toggle system tray icon

---

## 🎹 Hotkeys
- **Ctrl+H:** Trigger haptic feedback
- **Ctrl+L:** Start/stop the mouse listener

---

## 📊 Statistics
- **Haptic Events:** Total number of haptic events triggered
- **Last:** Timestamp of the last haptic event

---


## 🙏 Credits
- [PyQt5](https://pypi.org/project/PyQt5/)
- [pynput](https://pypi.org/project/pynput/)
- [PyTouchBar](https://github.com/olemb/pytouchbar)

---

<div align="center">
  <sub>Made with ❤️ for macOS by dxnutzx</sub>
</div>
