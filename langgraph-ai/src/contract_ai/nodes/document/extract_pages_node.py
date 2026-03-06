import uuid

from contract_ai.infrastructure.pdf.pdf_page_extractor import PDFPageExtractor

extractor = PDFPageExtractor()


def extract_pages_node(state):
    pdf_path = state["pdf_path"]
    temp_dir = f"/tmp/contract_pages_{uuid.uuid4()}"

    print(f"[DEBUG extract_pages] extracting: {pdf_path}")

    page_images = extractor.extract(pdf_path, temp_dir)

    print(f"[DEBUG extract_pages] pages extracted: {len(page_images)}")

    if len(page_images) > 20:
        raise ValueError("Document exceeds maximum page limit (20)")

    # raw_text is NOT set here — it will be set by reconstruct_clauses_node
    # using the vision LLM output, which is the single source of truth
    return {
        "page_images": page_images,
    }