# 🦋 Silksong Mod Manager (BepInEx)

A lightweight and modern mod manager for Hollow Knight: Silksong, built with Python and CustomTkinter.

## Features

* **Dark Design:** Clean and modern interface using CustomTkinter.
* **Quick Enable/Disable:** Instantly move mods between the `plugins/` and `disableds/` folders.
* **Automatic Organization:** Loose DLL files are automatically wrapped into a folder when enabled or disabled.
* **Fast Search:** Real-time mod filtering for large mod lists.
* **Portable:** Distributed as a single executable file (`.exe`).

## Download & Usage

The easiest way to get started is to download the ready-to-use executable from the **[Releases]** tab.

### Windows Executable (.exe)

1. Go to the **[Releases]** tab in this repository.  
2. Download the file `SilksongModManager.exe` under the latest *release*.  
3. Run the `.exe` and set your base `BepInEx` path.  

## For Developers (Run from Source)

If you want to run or modify the code, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/OsHK00/Silksong-Mod-Manager.git
    cd Silksong-Mod-Manager
    ```
2. **Install dependencies:** (Requires Python 3.x)
    ```bash
    pip install -r requirements.txt
    ```
3. **Run:**
    ```bash
    python mod_manager_gui.py
    ```

