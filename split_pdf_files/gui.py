import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import logging
from pdf_splitter import PDFSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # Variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.split_size = tk.StringVar(value="2")
        self.status_text = tk.StringVar(value="Ready")

        self._create_widgets()

    def _create_widgets(self):
        # Input file section
        input_frame = ttk.LabelFrame(self.root, text="Input PDF", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Entry(input_frame, textvariable=self.input_path, width=50).pack(side="left", padx=5)
        ttk.Button(input_frame, text="Browse", command=self._browse_input).pack(side="left")

        # Output directory section
        output_frame = ttk.LabelFrame(self.root, text="Output Directory (Optional)", padding=10)
        output_frame.pack(fill="x", padx=10, pady=5)

        ttk.Entry(output_frame, textvariable=self.output_path, width=50).pack(side="left", padx=5)
        ttk.Button(output_frame, text="Browse", command=self._browse_output).pack(side="left")

        # Split options
        options_frame = ttk.LabelFrame(self.root, text="Split Options", padding=10)
        options_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(options_frame, text="Number of parts:").pack(side="left", padx=5)
        ttk.Entry(options_frame, textvariable=self.split_size, width=10).pack(side="left", padx=5)

        # Process button
        ttk.Button(self.root, text="Split PDF", command=self._process_pdf).pack(pady=20)

        # Status
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(status_frame, textvariable=self.status_text).pack()

    def _browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.input_path.set(filename)

    def _browse_output(self):
        dirname = filedialog.askdirectory(title="Select Output Directory")
        if dirname:
            self.output_path.set(dirname)

    def _process_pdf(self):
        input_file = self.input_path.get()
        if not input_file:
            messagebox.showerror("Error", "Please select an input PDF file")
            return

        try:
            # Update status
            self.status_text.set("Processing...")
            self.root.update()

            # Initialize splitter
            splitter = PDFSplitter(input_file)

            # Get output directory
            output_dir = self.output_path.get() or 'split_output'

            # Get number of parts
            num_parts = int(self.split_size.get())
            if num_parts < 2:
                raise ValueError("Number of parts must be at least 2")

            # Process PDF
            output_files = splitter.split_by_parts(output_dir, num_parts)

            # Validate
            input_pages, output_pages = splitter.validate_output(output_files)

            # Show success message
            success_msg = "PDF split successfully!\n\n"
            success_msg += f"Created {len(output_files)} files\n"
            success_msg += f"Total pages: {input_pages}\n"
            success_msg += f"Output directory: {Path(output_dir).resolve()}"

            messagebox.showinfo("Success", success_msg)
            self.status_text.set("Ready")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_text.set("Error occurred")
            logger.error(f"Error processing PDF: {str(e)}")


def main():
    root = tk.Tk()
    app = PDFSplitterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
