from pathlib import Path
from pdf2image import convert_from_path


class PDFPageExtractor:

    def extract(self, pdf_path: str, output_dir: str):

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        images = convert_from_path(pdf_path)

        image_paths = []

        for i, image in enumerate(images):

            path = Path(output_dir) / f"page_{i+1}.png"

            image.save(path, "PNG")

            image_paths.append(str(path))

        return image_paths