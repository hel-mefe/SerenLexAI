class DocumentTooLargeError(Exception):
    pass


class DocumentTooLongError(ValueError):
    """Raised when the PDF exceeds the maximum allowed page count (e.g. 20 pages)."""

    def __init__(self, pages: int, max_pages: int) -> None:
        self.pages = pages
        self.max_pages = max_pages
        super().__init__(
            f"Document exceeds maximum allowed size ({max_pages} pages). "
            f"Your document has {pages} pages. We cannot process PDFs with more than {max_pages} pages."
        )