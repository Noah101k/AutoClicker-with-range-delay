import sys
import threading
import time
import random
import ctypes
from PyQt5 import QtWidgets, QtCore, QtGui
import keyboard  # pip install keyboard

# Windows API click function
SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", ctypes.c_ulonglong)]

def click_mouse(mouse_button="left"):
    if mouse_button == "left":
        down = 0x0002  # MOUSEEVENTF_LEFTDOWN
        up = 0x0004    # MOUSEEVENTF_LEFTUP
    elif mouse_button == "right":
        down = 0x0008  # MOUSEEVENTF_RIGHTDOWN
        up = 0x0010    # MOUSEEVENTF_RIGHTUP
    else:
        down = 0x0020  # MOUSEEVENTF_MIDDLEDOWN
        up = 0x0040    # MOUSEEVENTF_MIDDLEUP
    ctypes.windll.user32.mouse_event(down, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(up, 0, 0, 0, 0)


class AutoClicker(QtWidgets.QWidget):
    hotkeyPressed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Clicker - Dark Mode")
        self.resize(600, 400)

        self.clicking = False
        self.hotkey = "f6"

        self.build_ui()
        self.apply_dark_style()

        self.hotkeyPressed.connect(self.toggle_clicking)

        threading.Thread(target=self.listen_hotkey, daemon=True).start()

    def build_ui(self):
        main_layout = QtWidgets.QVBoxLayout()

        # Click Interval
        interval_group = QtWidgets.QGroupBox("Click interval")
        ig_layout = QtWidgets.QHBoxLayout()
        self.fixed_interval = QtWidgets.QSpinBox()
        self.fixed_interval.setRange(1, 10000)
        self.fixed_interval.setSuffix(" ms")
        self.fixed_interval.setValue(100)
        ig_layout.addWidget(QtWidgets.QLabel("Fixed:"))
        ig_layout.addWidget(self.fixed_interval)

        self.random_checkbox = QtWidgets.QCheckBox("Use Random Interval")
        self.random_min = QtWidgets.QSpinBox()
        self.random_min.setRange(1, 10000)
        self.random_min.setSuffix(" ms")
        self.random_min.setValue(1)
        self.random_max = QtWidgets.QSpinBox()
        self.random_max.setRange(1, 10000)
        self.random_max.setSuffix(" ms")
        self.random_max.setValue(100)

        ig_layout.addWidget(self.random_checkbox)
        ig_layout.addWidget(self.random_min)
        ig_layout.addWidget(QtWidgets.QLabel("and"))
        ig_layout.addWidget(self.random_max)

        interval_group.setLayout(ig_layout)
        main_layout.addWidget(interval_group)

        # Click Options
        click_group = QtWidgets.QGroupBox("Click options")
        cg_layout = QtWidgets.QFormLayout()
        self.mouse_button = QtWidgets.QComboBox()
        self.mouse_button.addItems(["Left", "Right", "Middle"])
        self.click_type = QtWidgets.QComboBox()
        self.click_type.addItems(["Single", "Double"])
        cg_layout.addRow("Mouse button:", self.mouse_button)
        cg_layout.addRow("Click type:", self.click_type)
        click_group.setLayout(cg_layout)
        main_layout.addWidget(click_group)

        # Cursor Position
        pos_group = QtWidgets.QGroupBox("Cursor position")
        pg_layout = QtWidgets.QHBoxLayout()
        self.current_pos = QtWidgets.QRadioButton("Current location")
        self.current_pos.setChecked(True)
        self.fixed_pos = QtWidgets.QRadioButton("Fixed location")
        self.pos_x = QtWidgets.QSpinBox()
        self.pos_x.setRange(0, 9999)
        self.pos_y = QtWidgets.QSpinBox()
        self.pos_y.setRange(0, 9999)
        pg_layout.addWidget(self.current_pos)
        pg_layout.addWidget(self.fixed_pos)
        pg_layout.addWidget(QtWidgets.QLabel("X:"))
        pg_layout.addWidget(self.pos_x)
        pg_layout.addWidget(QtWidgets.QLabel("Y:"))
        pg_layout.addWidget(self.pos_y)
        pos_group.setLayout(pg_layout)
        main_layout.addWidget(pos_group)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.start_btn = QtWidgets.QPushButton(f"Start ({self.hotkey.upper()})")
        self.start_btn.clicked.connect(self.start_clicking)
        self.stop_btn = QtWidgets.QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_clicking)
        self.hotkey_btn = QtWidgets.QPushButton("Set Hotkey")
        self.hotkey_btn.clicked.connect(self.set_hotkey)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.hotkey_btn)

        main_layout.addLayout(btn_layout)

        self.status_label = QtWidgets.QLabel("Stopped")
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def apply_dark_style(self):
        self.setStyleSheet("""
            QWidget { background-color: #1E1E1E; color: #E0E0E0; font-size: 10pt; }
            QGroupBox { background-color: #2A2A2A; border: 1px solid #444; border-radius: 6px; margin-top: 8px; padding-top: 10px; font-weight: bold; color: #CCCCCC; }
            QSpinBox, QComboBox, QLineEdit { background-color: #3A3A3A; border: 1px solid #555; padding: 3px; color: #FFFFFF; selection-background-color: #5555FF; }
            QPushButton { background-color: #3A3A3A; border: 1px solid #555; padding: 5px 10px; border-radius: 4px; }
            QPushButton:hover { background-color: #555555; }
            QPushButton:disabled { background-color: #2A2A2A; color: #777777; }
            QLabel { color: #DDDDDD; }
            QRadioButton { color: #CCCCCC; }
        """)

    def listen_hotkey(self):
        while True:
            keyboard.wait(self.hotkey)
            self.hotkeyPressed.emit()

    def set_hotkey(self):
        self.status_label.setText("Press a new hotkey...")
        self.repaint()
        new_key = keyboard.read_event().name
        self.hotkey = new_key
        self.start_btn.setText(f"Start ({self.hotkey.upper()})")
        self.status_label.setText(f"Hotkey set to {self.hotkey.upper()}")

    @QtCore.pyqtSlot()
    def toggle_clicking(self):
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    @QtCore.pyqtSlot()
    def start_clicking(self):
        if self.clicking:
            return
        self.clicking = True
        self.status_label.setText("Clicking...")
        threading.Thread(target=self.click_loop, daemon=True).start()

    @QtCore.pyqtSlot()
    def stop_clicking(self):
        self.clicking = False
        self.status_label.setText("Stopped")

    def click_loop(self):
        while self.clicking:
            if self.current_pos.isChecked() is False:
                ctypes.windll.user32.SetCursorPos(self.pos_x.value(), self.pos_y.value())

            clicks = 1 if self.click_type.currentText() == "Single" else 2
            for _ in range(clicks):
                click_mouse(self.mouse_button.currentText().lower())

            if self.random_checkbox.isChecked():
                interval = random.uniform(self.random_min.value() / 1000, self.random_max.value() / 1000)
            else:
                interval = self.fixed_interval.value() / 1000
            time.sleep(interval)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AutoClicker()
    window.show()
    sys.exit(app.exec_())
