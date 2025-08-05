An autoclicker where you can set a range of times to click in between (1ms - 100ms). This is made with ChatGPT. If you're worried about malware, upload it to VirusTotal. Made this for testing an autoclicker ac im making just posting this because most of the ones online are malware.



---

# AutoClicker — Build Instructions

This is a Python auto clicker with a GUI using `tkinter`, `pyautogui`, and `keyboard`.
Follow these steps to build a standalone Windows executable (`.exe`) from the source code.

---

## Requirements

* Python 3.x installed (download from [python.org](https://www.python.org/downloads/))
  Make sure to check **"Add Python to PATH"** during installation.

* The following Python packages:
  `pyautogui` and `keyboard`
  (will be installed via `pip`)

* `pyinstaller` for building the `.exe`

---

## Building the Executable

1. Open a command prompt and navigate to the folder containing the source code:

   ```bash
   cd path\to\your\project
   ```

2. Install required libraries:

   ```bash
   pip install pyautogui keyboard pyinstaller
   ```

3. Build the executable with PyInstaller:

   ```bash
   pyinstaller --onefile --noconsole --hidden-import=pyautogui --hidden-import=keyboard auto_clicker.py
   ```

   * `--onefile`: Package everything into a single `.exe` file.
   * `--noconsole`: Hide the console window when running the GUI.
   * `--hidden-import`: Ensure these libraries are included correctly.

4. After the build completes, find the standalone executable in the `dist` folder:

   ```
   dist\auto_clicker.exe
   ```

5. Run `auto_clicker.exe` to launch the program. You can now share this `.exe` file — it does **not** require Python or any libraries to be installed on the target machine.

---

## Notes

* This `.exe` works only on Windows systems.

* If you want to see the console window (for debugging), remove the `--noconsole` option from the build command.

---

Feel free to open issues if you run into any problems!
