from contract_ai.infrastructure.vision.ocr_service import OCRService


class DocumentValidator:

    MIN_TEXT_LENGTH = 50

    def __init__(self):
        self.ocr = OCRService()

    def validate(self, page_images):

        total_text = ""

        for image_path in page_images:

            text = self.ocr.extract_text(image_path)

            if text:
                total_text += text.strip()

        if len(total_text) < self.MIN_TEXT_LENGTH:
            raise ValueError(
                "Document appears to contain no readable text."
            )

        return True