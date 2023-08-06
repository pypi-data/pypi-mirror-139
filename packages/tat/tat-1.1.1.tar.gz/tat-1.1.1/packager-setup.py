import sys
from cx_Freeze import setup, Executable

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

version = ""
with open("version.txt") as f:
    version = f.read().rstrip("\n")

sys.path.insert(0, "src")

shortcut_table = [
    ("DesktopShortcut",             # Shortcut
     "DesktopFolder",               # Directory_
     "Tomography Analysis Tool",    # Name
     "TARGETDIR",                   # Component_
     "[TARGETDIR]tat.exe",          # Target
     None,                          # Arguments
     None,                          # Description
     None,                          # Hotkey
     None,                          # Icon
     None,                          # IconIndex
     None,                          # ShowCmd
     'TARGETDIR'                    # WkDir
     )
]

msi_data = {
    "Shortcut": shortcut_table
}

bdist_msi_options = {
    "summary_data": {
        "author": "Hugo Haldi",
        "comments": "Tomography Analysis Tool",
        "keywords": "TAT Tomography Analysis Tool"
    },
    "data": msi_data,
    "upgrade_code": "{22872b66-f52b-40fd-b973-951a9cac3620}"
}

build_exe_options = {
    "packages": [
        "PySide6",
        "cv2",
        "skimage",
        "tat"
    ],
    "excludes": [
        "tkinter"
    ],
    "path": sys.path
}

executables = [
    Executable("src/tat/__main__.py",
               copyright="Copyright (C) 2022 TAT",
               base=base,
               target_name="tat",
               shortcut_name="Tomography Analysis Tool")
]

setup(
    name="tat",
    version=version,
    description="Tomography Analysis Tool",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=executables
)
