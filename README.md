An autoclicker where you can set a range of times to click in between (1ms - 100ms). This is made with ChatGPT. If you're worried about malware, upload it to VirusTotal (some security venders will flag it because it messes with clicking stuff). Made this for testing an autoclicker ac im making just posting this because most of the ones online are malware.


---

## 🛠 Build Instructions

Follow these steps to build the Auto Clicker into a standalone **Windows `.exe`** file with a custom icon.

### 1. Install Requirements

Make sure you have **Python 3.9+** installed, then install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Install PyInstaller

```bash
pip install pyinstaller
```

### 3. Prepare an Icon (Optional)

If you want a custom app icon:

1. Create or download an image (256×256 recommended).
2. Convert it to `.ico` format using a free tool like [icoconvert.com](https://icoconvert.com).
3. Save it in the project folder as `autoclicker.ico`.

### 4. Build the `.exe`

Run the following command from the project root (replace `autoclicker.py` with your file name):

```bash
pyinstaller --onefile --windowed --icon=autoclicker.ico autoclicker.py
```

**Flags explained:**

* `--onefile` → Single `.exe` file.
* `--windowed` → Prevents a console window from appearing (GUI mode).
* `--icon=autoclicker.ico` → Sets the program’s icon.

### 5. Locate Your Executable

After building, your compiled file will be in:

```
dist/autoclicker.exe
```

You can now run it on any Windows machine — **no Python required**.

---

✅ **Tip:** To reduce `.exe` size and remove temporary files, you can use:

```bash
pyinstaller --onefile --windowed --clean --noconfirm --icon=autoclicker.ico autoclicker.py
```

---

Feel free to open issues if you run into any problems!
