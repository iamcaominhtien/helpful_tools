# PDF Splitter

A Python application that allows you to split PDF files into multiple parts with both GUI and command-line interfaces.

## Features

- **User-friendly GUI**: Easy-to-use graphical interface for splitting PDFs
- **Command-line Support**: Command-line interface for automation and scripting
- **Two Splitting Methods**:
  - Split by number of parts (divides PDF into equal parts)
  - Split by page ranges (specify custom page ranges)
- **Validation**: Ensures all pages from input are present in output files
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd split_pdf_files
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode

Run the application with graphical interface:

```bash
python gui.py
```

### Command Line Mode

Split PDF by number of parts:
```bash
python main.py input.pdf --split-size 2 --output-dir output_folder
```

Split PDF by page ranges:
```bash
python main.py input.pdf --ranges "1-3" "4-6" --output-dir output_folder
```

## Build

To create a standalone executable:

<!-- ### macOS -->
<!-- ```bash
python setup.py py2app
``` -->

<!-- ### Windows/Linux -->
```bash
pyinstaller --windowed --name "PDF Splitter" --add-data "$(python -c 'import tkinter; print(tkinter.__file__)'):./tkinter" --hidden-import PyPDF2 --hidden-import tkinter --hidden-import tkinter.ttk --hidden-import tkinter.filedialog gui.py
```

## Requirements

- Python 3.6+
- PyPDF2 >= 3.0.0
- tkinter (included with Python)
- pyinstaller >= 5.0.0 (for building executables)

## Project Structure

- `gui.py`: GUI implementation using tkinter
- `main.py`: Command-line interface implementation
- `pdf_splitter.py`: Core PDF splitting functionality
- `setup.py`: Build configuration for creating standalone executables
- `requirements.txt`: Required Python packages