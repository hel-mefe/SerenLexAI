from pdf2image import convert_from_path
from contract_ai.infrastructure.config.settings import settings
from contract_ai.domain.exceptions import DocumentTooLargeError

class PageExtractor:

    def extract(self, pdf_path: str):

        images = convert_from_path(pdf_path)

        page_count = len(images)

        if page_count > settings.MAX_PAGE_SIZE:
            raise DocumentTooLargeError(
                f"Document exceeds maximum allowed pages"
                f"{page_count} > {settings.MAX_PAGE_SIZE}"
            )

        paths = []

        for i, img in enumerate(images):
            path = f"/tmp/page_{i}.png"
            img.save(path)
            paths.append(path)

        return paths