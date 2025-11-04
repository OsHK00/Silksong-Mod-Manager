# 🦋 Silksong Mod Manager (BepInEx)

A lightweight and modern mod manager for Hollow Knight: Silksong (and other BepInEx games), built with Python and CustomTkinter.

---

## 🛡️ Antivirus Warning (False Positive)

🚨 **Your antivirus software may flag the executable (`.exe`) as suspicious or malicious.**

This is almost always a **False Positive** caused by the packing process (`--onefile`) used by PyInstaller. The generic or heuristic analysis engines in some antivirus programs mistake the way the executable unpacks binaries into memory for common malware behavior.

For your peace of mind:

* **VirusTotal Analysis:** You can verify the latest scan results here: **[https://www.virustotal.com/gui/file/391362e4a872927bbfdd83aa41810a879f2a93bc3f5065c78393ac98fbef6bc8/behavior]**
* **Recommendation:** If your antivirus blocks the application, we recommend adding `SilksongModManager.exe` to your program's **whitelist** (or exclusions).
* **Transparency:** The full source code is available below, allowing you to **inspect the code** and **compile your own executable** to verify its safety.

---

## ✨ Features

* **Dark Design:** Clean and modern interface using CustomTkinter.
* **Quick Enable/Disable:** Instantly move mods between the `plugins/` and `disableds/` folders.
* **Automatic Organization:** Loose DLL files are automatically wrapped into a folder when enabled or disabled.
* **Fast Search:** Real-time mod filtering for large mod lists.
* **Portable:** Distributed as a single executable file (`.exe`).

---

## ⬇️ Download & Usage

The easiest way to get started is to download the ready-to-use executable from the **[Releases]** tab.

### 💻 Windows Executable (.exe)

1.  Go to the **[Releases]** tab in this repository.
2.  Download the **`.zip`** file containing `SilksongModManager.exe` under the latest *release*.
3.  Unzip the file and run the `.exe` to set your base `BepInEx` path.

---

## ⚙️ For Developers (Run from Source)

If you want to run, modify the code, or **compile your own version of the executable**, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/OsHK00/Silksong-Mod-Manager.git
    cd Silksong-Mod-Manager
    ```
2.  **Install dependencies:** (Requires Python 3.x)
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run:**
    ```bash
    python mod_manager_gui.py
    ```
4.  **Compile (PyInstaller):**
    ```bash
    pip install pyinstaller
    pyinstaller --onefile --name "SilksongModManager" --windowed mod_manager_gui.py
    ```
