import argparse
from pathlib import Path
import logging
from pdf_splitter import PDFSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def split_pdf(input_path, output_dir='split_output', split_size=None, page_ranges=None):
    """
    Split PDF file either by page ranges or into number of equal parts
    """
    assert split_size or page_ranges, "Either split_size or page_ranges must be provided"
    
    splitter = PDFSplitter(input_path)
    
    try:
        if page_ranges:
            output_files = splitter.split_by_ranges(output_dir, page_ranges)
        else:
            output_files = splitter.split_by_parts(output_dir, split_size or 2)
            
        # Validate the split operation
        input_pages, output_pages = splitter.validate_output(output_files)
        logger.info(f"Split validation successful: {input_pages} input pages = {output_pages} output pages")
        return output_files

    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split PDF files into smaller parts')
    parser.add_argument('input_pdf', type=str, help='Path to input PDF file')
    parser.add_argument('--output-dir', default='split_output', help='Output directory for split files')
    parser.add_argument('--split-size', type=int, help='Number of pages per split')
    parser.add_argument('--ranges', nargs='+', help='Page ranges (e.g., 1-3 4-6)')
    
    args = parser.parse_args()
    print('args:', args)
    
    try:
        output_files = split_pdf(args.input_pdf, args.output_dir, args.split_size, args.ranges)
        print(f"PDF split successfully. Output files are in: {Path(args.output_dir).resolve()}")
        print(f"Created {len(output_files)} output files")
    except Exception as e:
        print(f"Error: {str(e)}")
