from pathlib import Path

import PyPDF2
import pytest
from pdf_splitter import PDFSplitter

# Constants
TEST_DATA_DIR = Path(__file__).parent / "data"
TEST_PDF = TEST_DATA_DIR / "data.pdf"
OUTPUT_DIR = Path(__file__).parent / "output"


@pytest.fixture(autouse=True)
def setup_teardown():
    """Setup and cleanup test directories"""
    TEST_DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    yield
    # Cleanup output files after tests
    for file in OUTPUT_DIR.glob("*.pdf"):
        file.unlink()


def test_split_by_parts():
    """Test splitting PDF into equal parts"""
    splitter = PDFSplitter(TEST_PDF)
    num_parts = 2
    output_files = splitter.split_by_parts(OUTPUT_DIR, num_parts)

    # Verify number of output files
    assert len(output_files) == num_parts

    # Verify all files exist
    assert all(file.exists() for file in output_files)

    # Verify total pages match
    total_pages = 0
    for file in output_files:
        with open(file, "rb") as f:
            pdf = PyPDF2.PdfReader(f)
            total_pages += len(pdf.pages)

    assert total_pages == splitter.total_pages


def test_split_by_ranges():
    """Test splitting PDF by page ranges"""
    splitter = PDFSplitter(TEST_PDF)
    ranges = ["1-2", "3-4"]  # Adjust based on your test PDF
    output_files = splitter.split_by_ranges(OUTPUT_DIR, ranges)

    # Verify number of output files
    assert len(output_files) == len(ranges)

    # Verify all files exist
    assert all(file.exists() for file in output_files)

    # Verify page counts in each part
    with open(output_files[0], "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        assert len(pdf.pages) == 2  # First range should have 2 pages

    with open(output_files[1], "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        assert len(pdf.pages) == 2  # Second range should have 2 pages


def test_invalid_ranges():
    """Test error handling for invalid page ranges"""
    splitter = PDFSplitter(TEST_PDF)
    with pytest.raises(ValueError):
        splitter.split_by_ranges(
            OUTPUT_DIR, ["1-100"]
        )  # Assuming test PDF has fewer pages


def test_invalid_parts():
    """Test error handling for invalid number of parts"""
    splitter = PDFSplitter(TEST_PDF)
    with pytest.raises(ZeroDivisionError):
        splitter.split_by_parts(OUTPUT_DIR, 0)


def test_invalid_input():
    """Test error handling for invalid input"""
    with pytest.raises(FileNotFoundError):
        PDFSplitter("nonexistent.pdf")
        