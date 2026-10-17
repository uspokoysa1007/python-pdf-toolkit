import sys
import re
import os
import argparse
from datetime import datetime

class StandalonePdfAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path, "rb") as f:
            self.content = f.read()

    def get_info(self):
        text = self.content.decode("latin1", errors="ignore")
        
        # Header version
        version_match = re.search(r"%PDF-(\d+\.\d+)", text)
        version = version_match.group(1) if version_match else "Unknown"

        # Count pages
        page_matches = re.findall(r"/Type\s*/Page", text)
        page_count = len(page_matches)

        # Count objects and streams
        objects = len(re.findall(r"\d+\s+\d+\s+obj", text))
        streams = len(re.findall(r"stream", text))
        fonts = len(re.findall(r"/Type\s*/Font", text))

        # Extract metadata
        meta = {}
        for key in ["Title", "Author", "Subject", "Creator", "Producer", "CreationDate"]:
            m = re.search(rf"/{key}\s*\((.*?)\)", text)
            if m:
                meta[key] = m.group(1)

        return {
            "version": version,
            "file_size": len(self.content),
            "pages": page_count,
            "objects": objects,
            "streams": streams,
            "fonts": fonts,
            "metadata": meta,
        }

def create_sample_pdf(out_path: str):
    """Generates a valid, readable PDF document using pure Python."""
    text_content = "Hello from Python PDF Toolkit!\nCreated purely with native Python without external libraries."
    
    # Simple valid 1-page PDF
    pdf_bytes = bytearray()
    pdf_bytes.extend(b"%PDF-1.4\n")
    
    # Object 1: Catalog
    o1 = len(pdf_bytes)
    pdf_bytes.extend(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    
    # Object 2: Pages
    o2 = len(pdf_bytes)
    pdf_bytes.extend(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    
    # Object 3: Page
    o3 = len(pdf_bytes)
    pdf_bytes.extend(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n")
    
    # Object 4: Stream (Content)
    stream_data = f"BT /F1 20 Tf 50 700 Td ({text_content}) Tj ET".encode("latin1")
    o4 = len(pdf_bytes)
    pdf_bytes.extend(f"4 0 obj\n<< /Length {len(stream_data)} >>\nstream\n".encode("latin1"))
    pdf_bytes.extend(stream_data)
    pdf_bytes.extend(b"\nendstream\nendobj\n")
    
    # Object 5: Font
    o5 = len(pdf_bytes)
    pdf_bytes.extend(b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    
    # Cross-reference table
    xref_pos = len(pdf_bytes)
    pdf_bytes.extend(b"xref\n0 6\n")
    pdf_bytes.extend(b"0000000000 65535 f \n")
    pdf_bytes.extend(f"{o1:010d} 00000 n \n".encode("latin1"))
    pdf_bytes.extend(f"{o2:010d} 00000 n \n".encode("latin1"))
    pdf_bytes.extend(f"{o3:010d} 00000 n \n".encode("latin1"))
    pdf_bytes.extend(f"{o4:010d} 00000 n \n".encode("latin1"))
    pdf_bytes.extend(f"{o5:010d} 00000 n \n".encode("latin1"))
    
    # Trailer
    pdf_bytes.extend(f"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("latin1"))
    
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    print(f"[+] Successfully generated valid PDF: {out_path} ({len(pdf_bytes)} bytes)")

def main():
    parser = argparse.ArgumentParser(description="Standalone Python PDF Inspector & Toolkit")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    info_parser = subparsers.add_parser("info", help="Inspect PDF file structure and metadata")
    info_parser.add_argument("file", help="Path to PDF file")

    sample_parser = subparsers.add_parser("create-sample", help="Create a sample PDF file")
    sample_parser.add_argument("output", default="sample.pdf", nargs="?", help="Output file path (default: sample.pdf)")

    args = parser.parse_args()

    if args.command == "create-sample":
        create_sample_pdf(args.output)
    elif args.command == "info":
        if not os.path.exists(args.file):
            print(f"[-] File not found: {args.file}")
            return
        analyzer = StandalonePdfAnalyzer(args.file)
        info = analyzer.get_info()

        print("=" * 64)
        print("                 PDF DOCUMENT INSPECTION REPORT                  ")
        print("=" * 64)
        print(f"File Path     : {args.file}")
        print(f"PDF Version   : {info['version']}")
        print(f"File Size     : {info['file_size']} bytes ({info['file_size'] / 1024:.2f} KB)")
        print(f"Page Count    : {info['pages']}")
        print(f"Total Objects : {info['objects']}")
        print(f"Streams Count : {info['streams']}")
        print(f"Fonts Count   : {info['fonts']}")
        print("-" * 64)
        print("[ METADATA DICTIONARY ]")
        if info["metadata"]:
            for k, v in info["metadata"].items():
                print(f"  {k:<14}: {v}")
        else:
            print("  (No document metadata embedded)")
        print("=" * 64)
    else:
        # Default action: create sample and analyze it
        sample_path = "sample_document.pdf"
        create_sample_pdf(sample_path)
        analyzer = StandalonePdfAnalyzer(sample_path)
        info = analyzer.get_info()
        print(f"[+] Verified generated document: PDF {info['version']}, {info['pages']} page(s), {info['objects']} objects.")

if __name__ == "__main__":
    main()
