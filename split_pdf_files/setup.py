from setuptools import setup

APP = ['gui.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyPDF2', 'tkinter'],
    'plist': {
        'CFBundleName': 'PDF Splitter',
        'CFBundleDisplayName': 'PDF Splitter',
        'CFBundleIdentifier': 'com.pdfsplitter.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.10.0'
    }
}

setup(
    app=APP,
    name='PDF Splitter',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

# Build with:
# pyinstaller --windowed --name "PDF Splitter" --add-data "$(python -c 'import tkinter; print(tkinter.__file__)'):./tkinter" --hidden-import PyPDF2 --hidden-import tkinter --hidden-import tkinter.ttk --hidden-import tkinter.filedialog gui.py