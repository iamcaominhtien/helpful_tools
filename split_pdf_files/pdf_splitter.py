import PyPDF2
from pathlib import Path
import logging
from math import ceil

logger = logging.getLogger(__name__)


class PDFSplitter:
    def __init__(self, input_path: str | Path):
        self.input_path = Path(input_path).resolve()
        self._validate_input()
        self.base_filename = self.input_path.stem
        self._file = None
        self.pdf = None
        self.total_pages = 0
        self._load_pdf()

    def _validate_input(self):
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_path}")
        if self.input_path.suffix.lower() != '.pdf':
            raise ValueError(f"Input file must be a PDF: {self.input_path}")

    def _load_pdf(self):
        """Load the PDF file and keep it open"""
        self._file = open(self.input_path, 'rb')
        self.pdf = PyPDF2.PdfReader(self._file)
        self.total_pages = len(self.pdf.pages)
        logger.info(f"Loaded PDF with {self.total_pages} pages")

    def __del__(self):
        """Cleanup when object is destroyed"""
        pass
        # if self._file:
            # self._file.close()

    def split_by_ranges(self, output_dir: str | Path, ranges: list[str]) -> list[Path]:
        """Split PDF by page ranges (e.g., ['1-3', '4-6'])"""
        if not self.pdf:
            self._load_pdf()
            
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_files = []

        for i, page_range in enumerate(ranges):
            writer = PyPDF2.PdfWriter()
            start, end = map(int, page_range.split('-'))
            
            if start < 1 or end > self.total_pages:
                raise ValueError(f"Invalid page range {page_range}. Valid range is 1-{self.total_pages}")
            
            pages_in_range = 0
            for page_num in range(start - 1, min(end, self.total_pages)):
                writer.add_page(self.pdf.pages[page_num])
                pages_in_range += 1
            
            output_path = output_dir / f'{self.base_filename}_part_{i + 1}.pdf'
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            output_files.append(output_path)
            logger.info(f"Created part {i + 1} with {pages_in_range} pages ({start}-{end})")
        
        return output_files

    def split_by_parts(self, output_dir: str | Path, num_parts: int) -> list[Path]:
        """Split PDF into specified number of parts"""
        if not self.pdf:
            self._load_pdf()
            
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_files = []

        pages_per_split = ceil(self.total_pages / num_parts)
        logger.info(f"Splitting into {num_parts} parts with ~{pages_per_split} pages each")
        
        for i in range(num_parts):
            writer = PyPDF2.PdfWriter()
            start_page = i * pages_per_split
            end_page = min((i + 1) * pages_per_split, self.total_pages)
            
            if start_page >= self.total_pages:
                break
            
            pages_in_part = 0
            for page_num in range(start_page, end_page):
                writer.add_page(self.pdf.pages[page_num])
                pages_in_part += 1
            
            output_path = output_dir / f'{self.base_filename}_part_{i + 1}.pdf'
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            output_files.append(output_path)
            logger.info(f"Created part {i + 1} with {pages_in_part} pages ({start_page + 1}-{end_page})")
        
        return output_files

    def validate_output(self, output_files: list[Path]) -> tuple[int, int]:
        """Validate that all pages from input are present in output files"""
        # Close the input file before validation to avoid resource conflicts
        if self._file:
            self._file.close()
            self._file = None
            
        total_output_pages = 0
        for output_file in output_files:
            with open(output_file, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                total_output_pages += len(pdf.pages)
        
        if total_output_pages != self.total_pages:
            raise ValueError(f"Page count mismatch! Input: {self.total_pages}, Output total: {total_output_pages}")
        return self.total_pages, total_output_pages
