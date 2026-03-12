import uuid
from pathlib import Path

from pypdf import PdfReader

from contract_ai.domain.exceptions import DocumentTooLongError
from contract_ai.infrastructure.pdf.pdf_page_extractor import PDFPageExtractor

MAX_PAGES = 20

extractor = PDFPageExtractor()


def extract_pages_node(state):
    pdf_path = state["pdf_path"]
    temp_dir = f"/tmp/contract_pages_{uuid.uuid4()}"

    print(f"[DEBUG extract_pages] extracting: {pdf_path}")

    # Validate page count before any heavy work (convert_from_path is expensive).
    pdf_file = Path(pdf_path)
    if pdf_file.is_file():
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            num_pages = len(reader.pages)
        if num_pages > MAX_PAGES:
            raise DocumentTooLongError(num_pages, MAX_PAGES)

    try:
        page_images = extractor.extract(pdf_path, temp_dir)
    except FileNotFoundError as e:
        print(f"[ERROR extract_pages] PDF not found: {e}")
        raise

    print(f"[DEBUG extract_pages] pages extracted: {len(page_images)}")

    if len(page_images) > MAX_PAGES:
        raise DocumentTooLongError(len(page_images), MAX_PAGES)

    # raw_text is NOT set here — it will be set by reconstruct_clauses_node
    # using the vision LLM output, which is the single source of truth
    return {
        "page_images": page_images,
    }