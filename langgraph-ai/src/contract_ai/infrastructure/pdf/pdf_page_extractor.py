from pathlib import Path
from typing import List

from pdf2image import convert_from_path


class PDFPageExtractor:
    """
    Helper for converting a PDF into page images.

    This version is defensive: it ensures the PDF exists on disk before
    calling pdf2image so we fail fast with a clear error instead of a
    confusing poppler I/O error.
    """

    def extract(self, pdf_path: str, output_dir: str) -> List[str]:
        pdf = Path(pdf_path)
        if not pdf.is_file():
            raise FileNotFoundError(
                f"PDFPageExtractor: PDF not found at '{pdf_path}'. "
                "Ensure the backend saved the upload to the shared /app/uploads volume."
            )

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        images = convert_from_path(str(pdf))

        image_paths: List[str] = []

        for i, image in enumerate(images):
            path = Path(output_dir) / f"page_{i+1}.png"
            image.save(path, "PNG")
            image_paths.append(str(path))

        return image_paths